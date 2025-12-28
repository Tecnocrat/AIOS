$source = 'Process'
$token = [Environment]::GetEnvironmentVariable('github_api','Process')
if (-not $token) { $token = [Environment]::GetEnvironmentVariable('github_api','User'); $source = 'User' }
if (-not $token) { $token = [Environment]::GetEnvironmentVariable('github_api','Machine'); $source = 'Machine' }
if (-not $token) {
    Write-Output "ERROR_ENV_MISSING"
    exit 2
}
try {
    Write-Output ("Using token from: " + $source)
    $headers = @{
        Authorization = "Bearer $token"
        'X-GitHub-Api-Version' = '2022-11-28'
        'User-Agent' = 'aios-test-agent'
    }
    $resp = Invoke-RestMethod -Uri 'https://api.github.com/user' -Headers $headers -ErrorAction Stop
    $resp | ConvertTo-Json -Depth 5
} catch {
    Write-Output ("ERROR: " + $_.Exception.Message)
    if ($_.Exception.Response -ne $null) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $body = $reader.ReadToEnd()
        Write-Output 'RESPONSE_BODY:'
        Write-Output $body
    }
    exit 3
}
