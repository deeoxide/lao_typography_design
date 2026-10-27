[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $projectRoot 'Package/manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

$inventory = @(foreach ($entry in $manifest.files) {
    $filePath = Join-Path $projectRoot $entry.path
    $present = Test-Path -LiteralPath $filePath -PathType Leaf
    $size = if ($present) { (Get-Item -LiteralPath $filePath).Length } else { $null }
    [pscustomobject]@{
        Path = $entry.path
        Present = $present
        Bytes = $size
    }
})

Write-Output "Project: $($manifest.name)"
Write-Output "Root: $projectRoot"
$inventory | Format-Table -AutoSize

Write-Output 'File references absent when the inventory was created (current status):'
foreach ($reference in $manifest.referencedFilesAbsentAtInventory) {
    $present = Test-Path -LiteralPath (Join-Path $projectRoot $reference) -PathType Leaf
    $status = if ($present) { 'present' } else { 'missing' }
    Write-Output "  ${reference}: $status"
}

Write-Output 'Knowledge document titles not included at inventory time:'
foreach ($title in $manifest.referencedDocumentsNotIncluded) {
    Write-Output "  $title"
}

$missing = @($inventory | Where-Object { -not $_.Present })
if ($missing.Count -gt 0) {
    throw "$($missing.Count) inventoried source file(s) are missing."
}
Write-Output "Verified $($inventory.Count) inventoried source files."
