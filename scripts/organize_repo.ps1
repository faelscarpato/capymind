param(
    [string]$SourceRoot = (Get-Location).Path,
    [string]$DestinationRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [int]$MaxFileSizeKB = 1024
)

$ErrorActionPreference = 'Stop'

$folders = @('knowledge','docs','prompts','datasets','data','schemas','references','indexes','projects','scripts','archive')
$allowedExtensions = @('.md','.txt','.json','.jsonl','.csv')
$ignoredDirs = @('node_modules','.git','.next','dist','build','coverage','release','out','bin','obj','.wrangler','.turbo','.cache','vendor','target')
$logDir = Join-Path $DestinationRoot 'scripts\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logPath = Join-Path $logDir ("organize_repo_{0}.log" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))

function Write-Log {
    param([string]$Message)
    $line = "[{0}] {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $logPath -Value $line
    Write-Host $line
}

function Ensure-Structure {
    foreach ($folder in $folders) {
        New-Item -ItemType Directory -Force -Path (Join-Path $DestinationRoot $folder) | Out-Null
    }
}

function Get-RelativePath {
    param([string]$BasePath, [string]$FullPath)
    $baseUri = [System.Uri]((Resolve-Path $BasePath).Path.TrimEnd('\') + '\')
    $targetUri = [System.Uri](Resolve-Path $FullPath).Path
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', '\')
}

function Resolve-Category {
    param([string]$RelativePath)
    $lower = $RelativePath.ToLowerInvariant()
    if ($lower -match '(^|\\)prompts(\\|$)') { return 'prompts' }
    if ($lower -match '(^|\\)datasets(\\|$)') { return 'datasets' }
    if ($lower -match '(^|\\)schemas(\\|$)') { return 'schemas' }
    if ($lower -match '(^|\\)references(\\|$)') { return 'references' }
    if ($lower -match '(^|\\)knowledge(\\|$)') { return 'knowledge' }
    if ($lower -match '(^|\\)docs(\\|$)') { return 'docs' }
    if ($lower -match '(^|\\)data(\\|$)' -or $lower -match '(^|\\)json(\\|$)' -or $lower -match '(^|\\)sql(\\|$)') { return 'data' }
    return 'docs'
}

function Get-UniquePath {
    param([string]$PathCandidate)
    if (-not (Test-Path -LiteralPath $PathCandidate)) { return $PathCandidate }
    $directory = Split-Path -Parent $PathCandidate
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($PathCandidate)
    $extension = [System.IO.Path]::GetExtension($PathCandidate)
    $counter = 1
    do {
        $next = Join-Path $directory ("{0}-{1:D3}{2}" -f $stem, $counter, $extension)
        $counter++
    } while (Test-Path -LiteralPath $next)
    return $next
}

function Copy-Safely {
    param([System.IO.FileInfo]$File)
    $relativePath = Get-RelativePath -BasePath $SourceRoot -FullPath $File.FullName
    $category = Resolve-Category -RelativePath $relativePath
    $targetDir = Join-Path $DestinationRoot $category
    $targetFile = Join-Path $targetDir $File.Name
    $uniqueTarget = Get-UniquePath -PathCandidate $targetFile
    Copy-Item -LiteralPath $File.FullName -Destination $uniqueTarget -Force:$false
    if ($uniqueTarget -ne $targetFile) {
        Write-Log "copied with rename | source=$($File.FullName) | target=$uniqueTarget"
    } else {
        Write-Log "copied | source=$($File.FullName) | target=$uniqueTarget"
    }
}

Ensure-Structure
Write-Log "organization started | source=$SourceRoot | destination=$DestinationRoot"

Get-ChildItem -LiteralPath $SourceRoot -File -Recurse -Force | ForEach-Object {
    $fullPath = $_.FullName
    foreach ($ignored in $ignoredDirs) {
        if ($fullPath -match ([regex]::Escape("\$ignored\"))) {
            Write-Log "ignored by directory rule | source=$fullPath"
            return
        }
    }
    if ($allowedExtensions -notcontains $_.Extension.ToLowerInvariant()) {
        Write-Log "ignored by extension | source=$fullPath"
        return
    }
    if ($_.Length -gt ($MaxFileSizeKB * 1KB)) {
        Write-Log "ignored by size | source=$fullPath | size=$($_.Length)"
        return
    }
    if ($fullPath.StartsWith($DestinationRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        Write-Log "ignored destination self-scan | source=$fullPath"
        return
    }
    Copy-Safely -File $_
}

Write-Log 'organization finished'
