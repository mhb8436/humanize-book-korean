#Requires -Version 5.1
<#
.SYNOPSIS
  humanize-book-korean 설치 (Windows 네이티브). bash install.sh 의 PowerShell 대응판.

.DESCRIPTION
  스킬·서브에이전트·슬래시 명령을 대상 책 프로젝트 또는 글로벌(%USERPROFILE%\.claude)에 설치합니다.
  도메인 자산(examples/)은 스킬 폴더 안에 포함되어 함께 설치됩니다 — 별도 처리 불필요.

  기본 모드는 -Copy(사본 복사)입니다. 윈도우에서 심볼릭 링크(-Link)는 '개발자 모드' 또는
  관리자 권한이 필요할 수 있어, 권한 문제가 없는 복사를 기본값으로 둡니다.

.EXAMPLE
  .\install.ps1 C:\Users\me\Workspaces\my-book
  # 특정 프로젝트에 사본 복사 설치 (기본)

.EXAMPLE
  .\install.ps1 -Global
  # ~/.claude 글로벌 사본 복사 설치 (모든 책 프로젝트에서 사용 가능)

.EXAMPLE
  .\install.ps1 -Global -Link
  # 글로벌 심볼릭 링크 설치 (개발용; 개발자 모드 또는 관리자 권한 필요)
#>
param(
    [Parameter(Position = 0)]
    [string]$Target,
    [switch]$Global,
    [switch]$Link,
    [switch]$Copy
)

$ErrorActionPreference = 'Stop'

# 저장소 루트 = 이 스크립트(scripts\install.ps1)의 부모의 부모
$SkillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

# --- 대상 결정 ---
if ($Global) {
    $TargetRoot = $env:USERPROFILE
    $Scope = 'global'
}
elseif ($Target) {
    if (-not (Test-Path -PathType Container $Target)) {
        Write-Error "대상 디렉토리가 없습니다: $Target"
        exit 1
    }
    $TargetRoot = (Resolve-Path $Target).Path
    $Scope = 'project'
}
else {
    Write-Host @"
사용법:
  .\install.ps1 <대상 책 프로젝트 경로> [-Link|-Copy]   # 프로젝트 설치
  .\install.ps1 -Global                  [-Link|-Copy]   # ~/.claude 글로벌 설치

모드: -Copy(기본, 사본 복사) | -Link(심볼릭 링크; 개발자 모드 또는 관리자 권한 필요)
"@
    exit 0
}

# --- 모드 결정 (윈도우 기본은 Copy 가 안전) ---
if ($Link) { $Mode = 'link' } else { $Mode = 'copy' }

$ClaudeDir = Join-Path $TargetRoot '.claude'
Write-Host "설치: $SkillRoot -> $ClaudeDir  ($Scope, $Mode)"

foreach ($sub in 'skills', 'commands', 'agents') {
    New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeDir $sub) | Out-Null
}

function Install-Item {
    param([string]$Src, [string]$Dest)
    if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
    if ($script:Mode -eq 'link') {
        try {
            New-Item -ItemType SymbolicLink -Path $Dest -Target $Src -ErrorAction Stop | Out-Null
        }
        catch {
            Write-Warning "심볼릭 링크 실패 ($Dest). '개발자 모드'를 켜거나 관리자 PowerShell에서 실행하거나 -Copy 를 사용하세요."
            throw
        }
    }
    else {
        if (Test-Path -PathType Container $Src) {
            Copy-Item -Recurse -Force $Src $Dest
        }
        else {
            Copy-Item -Force $Src $Dest
        }
    }
}

# 스킬 폴더 (examples/ 포함)
Install-Item -Src (Join-Path $SkillRoot '.claude\skills\humanize-book-korean') `
    -Dest (Join-Path $ClaudeDir 'skills\humanize-book-korean')

Get-ChildItem (Join-Path $SkillRoot '.claude\commands\*.md') | ForEach-Object {
    Install-Item -Src $_.FullName -Dest (Join-Path $ClaudeDir "commands\$($_.Name)")
}

Get-ChildItem (Join-Path $SkillRoot '.claude\agents\*.md') | ForEach-Object {
    Install-Item -Src $_.FullName -Dest (Join-Path $ClaudeDir "agents\$($_.Name)")
}

Write-Host "완료 ($Mode)."
if ($Mode -eq 'link') {
    Write-Host "  심볼릭 링크 — 저장소 변경이 즉시 반영됩니다."
}
Write-Host "  도메인 자산(examples/)은 스킬 폴더에 포함되어 함께 설치되었습니다."
Write-Host ""
Write-Host "다음 단계:"
if ($Scope -eq 'global') {
    Write-Host "  - 아무 책 프로젝트에서 'claude' 실행 후  /humanize-book {파일경로}"
    Write-Host "  - 공공 SI 책이면                        /humanize-book {파일경로} --domain spring-ai-book"
}
else {
    Write-Host "  - 대상 프로젝트에서 'claude' 실행 후     /humanize-book {파일경로}"
}
Write-Host "  - 새 도메인은  .claude\skills\humanize-book-korean\examples\{도메인}\  에 추가"
