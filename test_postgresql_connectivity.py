import socket

host = "pgs-db-bor-001-t.postgres.database.azure.com"
port = 5432

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)  # Timeout in seconds
        s.connect((host, port))
        print(f"Connected to {host}:{port}")
except Exception as e:
    print(f"Could not connect to {host}:{port} - Error: {e}")
