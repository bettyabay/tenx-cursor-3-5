Write-Host "=== Project Chimera MCP Verification ===" -ForegroundColor Cyan
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

Write-Host "`n1. Checking MCP Sense connection..." -ForegroundColor Yellow
$healthCheck = Invoke-WebRequest -Uri "http://localhost:3000/health" -Method Get -TimeoutSec 2 -ErrorAction SilentlyContinue
if ($healthCheck -and $healthCheck.StatusCode -eq 200) {
    Write-Host "[OK] MCP Sense: ACTIVE on port 3000" -ForegroundColor Green
    
    $body = @{
        project = "project-chimera"
        event = "spec_kit_initialized"
        phase = "specification"
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    } | ConvertTo-Json
    
    $logRequest = Invoke-WebRequest -Uri "http://localhost:3000/log" -Method Post -Body $body -ContentType "application/json" -ErrorAction SilentlyContinue
    if ($logRequest) {
        Write-Host "  [OK] Logged initialization event to MCP Sense" -ForegroundColor Gray
    } else {
        Write-Host "  [WARN] Could not log to MCP Sense (non-critical)" -ForegroundColor Yellow
    }
} else {
    Write-Host "[FAIL] MCP Sense: INACTIVE" -ForegroundColor Red
    Write-Host "Please start Tenx MCP Sense before continuing" -ForegroundColor Yellow
    Write-Host "Typically: docker run -p 3000:3000 tenx/mcp-sense:latest" -ForegroundColor Gray
    exit 1
}

Write-Host "`n2. Checking spec-kit installation..." -ForegroundColor Yellow
$specifyCmd = Get-Command specify -ErrorAction SilentlyContinue
if ($specifyCmd) {
    Write-Host "[OK] Spec Kit: INSTALLED" -ForegroundColor Green
    $versionOutput = & specify --version 2>&1
    if ($versionOutput) {
        Write-Host "  $versionOutput" -ForegroundColor Gray
    }
} else {
    Write-Host "[FAIL] Spec Kit: NOT FOUND" -ForegroundColor Red
    Write-Host "Run: uvx --from git+https://github.com/github/spec-kit.git specify --help" -ForegroundColor Gray
}

Write-Host "`n3. Checking directory structure..." -ForegroundColor Yellow
$requiredDirs = @("specs", "tests", "skills", ".github\workflows")
$allExist = $true
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir -PathType Container) {
        Write-Host "[OK] Directory: $dir exists" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Missing: $dir" -ForegroundColor Red
        $allExist = $false
    }
}

Write-Host "`n=== Verification Complete ===" -ForegroundColor Cyan
if (-not $allExist) {
    Write-Host "[WARN] Some directories are missing. Please create them before proceeding." -ForegroundColor Yellow
}
