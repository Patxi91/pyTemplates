import asyncio
import aiohttp
import time
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm.asyncio import tqdm
from collections import deque
from urllib.parse import urlparse, unquote
from pathlib import Path
import threading

# Config
URL = "https://proof.ovh.net/files/10Gb.dat"
DOWNLOAD_PATH = str(Path.home() / "Downloads" / "downloaded_file.dat")
CHUNK_SIZE = 1024 * 1024  # 1MB
MAX_CONNECTIONS = 16
RETRY_DELAY = 3
MAX_RETRIES = 5

# Shared data
speeds = deque(maxlen=60)
elapsed_times = deque(maxlen=60)
total_downloaded = 0
start_time = time.time()
lock = threading.Lock()

# Plot setup
plt.style.use('ggplot')
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_title("Download Speed (MB/s)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Speed (MB/s)")
ax.set_xlim(0, 60)
ax.set_ylim(0, 100)


def animate(_):
    with lock:
        if elapsed_times and speeds:
            x_data = list(elapsed_times)
            y_data = list(speeds)
            line.set_data(x_data, y_data)
            ax.set_xlim(max(0, x_data[0]), x_data[-1] + 1)
            ax.set_ylim(0, max(y_data) * 1.2)
    return line,


ani = animation.FuncAnimation(fig, animate, interval=1000)


def get_filename_from_url(url):
    path = urlparse(url).path
    return unquote(path.split('/')[-1]) or "downloaded_file.dat"


async def monitor_speed():
    global total_downloaded, start_time
    last_downloaded = 0
    while True:
        await asyncio.sleep(1)
        now = time.time()
        with lock:
            interval = now - start_time
            downloaded_now = total_downloaded
            speed = (downloaded_now - last_downloaded) / 1024 / 1024  # MB/s
            elapsed_times.append(interval)
            speeds.append(speed)
            last_downloaded = downloaded_now


async def download_chunk(session, url, start, end, index, results):
    global total_downloaded
    headers = {'Range': f'bytes={start}-{end}'}
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(url, headers=headers, timeout=60) as resp:
                resp.raise_for_status()
                data = await resp.read()
                results[index] = data
                with lock:
                    total_downloaded += len(data)
                return len(data)
        except Exception as e:
            print(f"[Chunk {index} - Retry {attempt + 1}] Error downloading chunk: {e}")
            await asyncio.sleep(RETRY_DELAY)
    raise RuntimeError(f"Failed to download chunk {index} after {MAX_RETRIES} attempts")


async def download_file():
    global start_time, total_downloaded
    start_time = time.time()
    total_downloaded = 0
    file_name = get_filename_from_url(URL)
    temp_path = DOWNLOAD_PATH + ".part"

    for attempt in range(MAX_RETRIES):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(URL, timeout=10) as resp:
                    resp.raise_for_status()
                    total_size = int(resp.headers['Content-Length'])
                if total_size <= 0:
                    raise ValueError("Invalid file size.")

                print(f"Total file size: {total_size / (1024 ** 3):.2f} GB")

                chunk_ranges = [(i, min(i + CHUNK_SIZE - 1, total_size - 1))
                                for i in range(0, total_size, CHUNK_SIZE)]

                results = [None] * len(chunk_ranges)
                sem = asyncio.Semaphore(MAX_CONNECTIONS)

                async def bounded_download(i, start, end):
                    async with sem:
                        return await download_chunk(session, URL, start, end, i, results)

                # Start monitoring speed in background
                monitor_task = asyncio.create_task(monitor_speed())

                pbar = tqdm(total=total_size, unit='B', unit_scale=True)
                tasks = [bounded_download(i, start, end) for i, (start, end) in enumerate(chunk_ranges)]

                for coro in asyncio.as_completed(tasks):
                    size = await coro
                    pbar.update(size)

                pbar.close()
                monitor_task.cancel()

                with open(temp_path, "wb") as f:
                    for chunk in results:
                        f.write(chunk)
                os.replace(temp_path, DOWNLOAD_PATH)
                print("✅ Download complete.")
                return

        except Exception as e:
            print(f"[Attempt {attempt + 1}] Error during download: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                print("❌ Failed after max retries.")
                raise


async def main():
    while True:
        try:
            await download_file()
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Restarting...")


def start_asyncio_download():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


if __name__ == "__main__":
    threading.Thread(target=start_asyncio_download, daemon=True).start()
    plt.show()
