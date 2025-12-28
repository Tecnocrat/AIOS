$token = [Environment]::GetEnvironmentVariable('github_api','Process')
if (-not $token) { $token = [Environment]::GetEnvironmentVariable('github_api','User') }
if (-not $token) { $token = [Environment]::GetEnvironmentVariable('github_api','Machine') }
if (-not $token) { Write-Output 'ERROR_ENV_MISSING'; exit 2 }

function Do-Request($withVersion) {
    Write-Output "\n=== Request (withVersion=$withVersion) ==="
    $headers = @{ Authorization = "Bearer $token"; 'User-Agent' = 'aios-test-agent' }
    if ($withVersion) { $headers['X-GitHub-Api-Version'] = '2022-11-28' }
    try {
        $resp = Invoke-WebRequest -Uri 'http://localhost:8085/' -Method Get -Headers $headers -ErrorAction Stop
        Write-Output "Status: $($resp.StatusCode.value__)"
        Write-Output "Body:"
        Write-Output $resp.Content
    } catch {
        Write-Output "ERROR: $($_.Exception.Message)"
        if ($_.Exception.Response -ne $null) {
            $respObj = $_.Exception.Response
            try {
                if ($respObj -is [System.Net.Http.HttpResponseMessage]) {
                    $body = $respObj.Content.ReadAsStringAsync().Result
                    Write-Output 'RESPONSE_BODY:'
                    Write-Output $body
                } else {
                    $stream = $respObj.GetResponseStream()
                    $reader = New-Object System.IO.StreamReader($stream)
                    $body = $reader.ReadToEnd()
                    Write-Output 'RESPONSE_BODY:'
                    Write-Output $body
                }
            } catch {
                Write-Output 'Failed to read response body.'
            }
        }
    }
}

Do-Request $true
Do-Request $false
