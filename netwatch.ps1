$interval = 1
$totalBytes = 0
$peakMbps = 0

# Automatically get the first active network adapter
$adapter = Get-NetAdapter |
    Where-Object { $_.Status -eq "Up" -and $_.MediaConnectionState -eq "Connected" } |
    Sort-Object -Property LinkSpeed -Descending |
    Select-Object -First 1

if (-not $adapter) {
    Write-Error "No active network adapter found."
    exit
}

$adapterName = $adapter.Name
Write-Host "Monitoring adapter: $adapterName"

try {
    $previous = (Get-NetAdapterStatistics -Name $adapterName).ReceivedBytes
} catch {
    Write-Error "Cannot read stats for adapter '$adapterName'."
    exit
}

while ($true) {
    Start-Sleep -Seconds $interval
    try {
        $current = (Get-NetAdapterStatistics -Name $adapterName).ReceivedBytes
        $delta = $current - $previous
        $previous = $current

        $speedMbps = [math]::Round(($delta * 8) / 1MB, 2)
        if ($speedMbps -gt $peakMbps) { $peakMbps = $speedMbps }
        $totalBytes += $delta
        $totalGB = [math]::Round($totalBytes / 1GB, 3)

        Write-Host "Speed: $speedMbps Mbps | Peak: $peakMbps Mbps | Total: $totalGB GB"
    } catch {
        Write-Error "Failed to retrieve stats."
        break
    }
}
