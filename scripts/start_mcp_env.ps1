$token = [Environment]::GetEnvironmentVariable('github_api','Process')
if (-not $token) { $token = [Environment]::GetEnvironmentVariable('github_api','User') }
if (-not $token) { $token = [Environment]::GetEnvironmentVariable('github_api','Machine') }
if (-not $token) {
    Write-Error 'github_api environment variable not found (Process/User/Machine).'
    exit 2
}

$envFile = Join-Path $PSScriptRoot 'mcp_env.txt'
Set-Content -Path $envFile -Value ("GITHUB_PERSONAL_ACCESS_TOKEN=$token`nGITHUB_TOOLSETS=repos,issues,pull_requests,actions") -Force

try { docker rm -f github-mcp 2>$null } catch {}

Write-Output "Starting MCP container (host port 8085) using env-file: $envFile"
$cid = docker run -d --name github-mcp -p 8085:8080 --env-file $envFile ghcr.io/github/github-mcp-server
if ($LASTEXITCODE -ne 0) { Write-Error "docker run failed (exit $LASTEXITCODE)"; exit 3 }

Start-Sleep -Seconds 2
docker ps --filter name=github-mcp --format 'table {{.ID}}`t{{.Names}}`t{{.Status}}`t{{.Ports}}'

Write-Output "Recent container logs:"
docker logs --tail 200 github-mcp
