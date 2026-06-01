param(
  [Parameter(Mandatory=$true)][string]$InputPath,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [string]$Series = "series",
  [string]$VoiceName = "Microsoft Kangkang",
  [int]$Rate = -1,
  [int]$Volume = 100,
  [int]$TargetChars = 420
)

$ErrorActionPreference = "Stop"

$skillDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$segmentScript = Join-Path $skillDir "scripts\prepare_tts_segments.py"
$csvPath = Join-Path $OutDir "$Series`_segments.csv"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

python $segmentScript $InputPath --series $Series --target-chars $TargetChars --out $csvPath | Out-Null

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice($VoiceName)
$synth.Rate = $Rate
$synth.Volume = $Volume

$rows = Import-Csv -Path $csvPath
$generated = @()

foreach ($row in $rows) {
  $wavName = [System.IO.Path]::ChangeExtension($row.filename, ".wav")
  $wavPath = Join-Path $OutDir $wavName
  $text = $row.text -replace "`r?`n", " "
  $synth.SetOutputToWaveFile($wavPath)
  $synth.Speak($text)
  $synth.SetOutputToNull()
  $generated += [PSCustomObject]@{
    file = $wavPath
    episode = $row.episode
    part = $row.part
    estimated_seconds = $row.estimated_seconds
  }
}

$generated | Format-Table -AutoSize
Write-Output "csv=$csvPath"
