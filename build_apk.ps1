# Build Android di Date the Dignitas.
#
# Uso:
#   .\build_apk.ps1              APK in ..\DateTheDig-dists
#   .\build_apk.ps1 -Bundle      AAB per Google Play
#   .\build_apk.ps1 -Installa    APK + installazione sul telefono collegato via USB
#
# Richiede in tools\ (ignorata da git): renpy-8.3.7-sdk con rapt e Android SDK
# installati, e il JDK 21 in tools\jdk. Le chiavi android.keystore e
# bundle.keystore devono stare nella cartella del progetto.
param(
    [switch]$Bundle,
    [switch]$Installa
)

$ErrorActionPreference = "Stop"

$sdk = Join-Path $PSScriptRoot "tools\renpy-8.3.7-sdk"
$jdk = Get-ChildItem (Join-Path $PSScriptRoot "tools\jdk") -Directory -Filter "jdk-21*" | Select-Object -First 1
if ($null -eq $jdk) { throw "JDK 21 non trovato in tools\jdk" }
if (-not (Test-Path (Join-Path $sdk "rapt\Sdk"))) { throw "Android SDK non installato in $sdk\rapt\Sdk" }
foreach ($k in "android.keystore", "bundle.keystore") {
    if (-not (Test-Path (Join-Path $PSScriptRoot $k))) { throw "Manca $k nella cartella del progetto" }
}

$env:JAVA_HOME = $jdk.FullName
$env:PATH = (Join-Path $jdk.FullName "bin") + ";" + $env:PATH

$dest = Join-Path (Split-Path $PSScriptRoot -Parent) "DateTheDig-dists"
New-Item -ItemType Directory -Force $dest | Out-Null

$argomenti = @((Join-Path $sdk "renpy.py"), (Join-Path $sdk "launcher"), "android_build", $PSScriptRoot, "--dest", $dest)
if ($Bundle) { $argomenti += "--bundle" }
if ($Installa) { $argomenti += "--install" }

& (Join-Path $sdk "lib\py3-windows-x86_64\python.exe") @argomenti
if ($LASTEXITCODE -ne 0) { throw "Build fallita (codice $LASTEXITCODE)" }

Get-ChildItem $dest -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1 Name, @{n="MB"; e={[math]::Round($_.Length / 1MB, 1)}}
