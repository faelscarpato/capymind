param(
    [string]$SourceRoot = (Get-Location).Path,
    [string]$DestinationRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [string[]]$AllowedExtensions = @('.md')
)

$ErrorActionPreference = 'Stop'
$folders = @('knowledge','knowledge\\business','knowledge\\products','knowledge\\operations','knowledge\\technical','knowledge\\commercial','knowledge\\ai','knowledge\\branding','projects','prompts','prompts\\generation','prompts\\analysis','prompts\\coding','prompts\\image','prompts\\business','prompts\\marketing','datasets','datasets\\structured','datasets\\extracted','datasets\\candidates','docs','docs\\architecture','docs\\systems','docs\\flows','docs\\ui-ux','docs\\api','references','references\\technical','references\\commercial','references\\contracts','references\\inspirations','references\\external','assets','assets\\catalogs','assets\\visual-assets','assets\\product-assets','assets\\diagrams','archive','scripts')
$ignoredDirs = @('node_modules','.git','.next','dist','build','coverage','vendor','venv','.venv','target','out','.turbo','.cache')
$logDir = Join-Path $DestinationRoot 'scripts\\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logPath = Join-Path $logDir ('organize_repo_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
function Log([string]$m){$line='[' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + '] ' + $m; Add-Content -LiteralPath $logPath -Value $line; Write-Host $line}
function Ensure-Structure { foreach($folder in $folders){ New-Item -ItemType Directory -Force -Path (Join-Path $DestinationRoot $folder) | Out-Null } }
function Category([string]$relative){ $lower=$relative.ToLowerInvariant(); if($lower -match 'prompt'){return 'prompts'}; if($lower -match 'mercado livre|petala'){return 'knowledge\\commercial'}; if($lower -match 'dataset|csv|xlsx|json'){return 'datasets\\candidates'}; return 'archive' }
function UniquePath([string]$candidate){ if(-not (Test-Path -LiteralPath $candidate)){ return $candidate }; $dir=Split-Path -Parent $candidate; $stem=[IO.Path]::GetFileNameWithoutExtension($candidate); $ext=[IO.Path]::GetExtension($candidate); $i=1; do { $next=Join-Path $dir ($stem + '-' + $i.ToString('000') + $ext); $i++ } while(Test-Path -LiteralPath $next); return $next }
Ensure-Structure
Log ('organization started | source=' + $SourceRoot + ' | destination=' + $DestinationRoot)
Get-ChildItem -LiteralPath $SourceRoot -File -Recurse -Force | ForEach-Object {
    $full=$_.FullName
    if($full.StartsWith($DestinationRoot,[StringComparison]::OrdinalIgnoreCase)){ Log ('ignored destination self-scan | source=' + $full); return }
    foreach($ignored in $ignoredDirs){ if($full -match ([regex]::Escape('\\' + $ignored + '\\'))){ Log ('ignored by directory rule | source=' + $full); return } }
    if($AllowedExtensions -notcontains $_.Extension.ToLowerInvariant()){ Log ('ignored by extension | source=' + $full); return }
    $relative = Resolve-Path -LiteralPath $full | ForEach-Object { $_.Path.Substring((Resolve-Path $SourceRoot).Path.Length).TrimStart('\\') }
    $category = Category $relative
    $targetDir = Join-Path $DestinationRoot $category
    $target = UniquePath (Join-Path $targetDir $_.Name)
    Copy-Item -LiteralPath $full -Destination $target -Force:$false
    Log ('copied | source=' + $full + ' | target=' + $target)
}
Log 'organization finished'
