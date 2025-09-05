<# 
================================================================================
[과제2] 파워쉘을 이용한 랜섬웨어 동작 시뮬레이션 파일 생성
제작자 : 정하은
제작일 : 2025-09-05
설  명
  - 본 코드는 실제 악성 행위(실제 파일 훼손/MBR 조작/권한 변경)는 수행하지 않고 훈련 목적으로 작성했다.
  - 모든 동작은 TEMP 하위의 전용 샌드박스 폴더에서만 이뤄진다.
  - 출력 메시지와 가짜 파일/로그를 통해 랜섬웨어의 동작 "흉내"만 내도록 했다.
안전 장치
  - 시스템 민감 경로(C:\Windows\System32\config 등)에 접근 시도 시뮬레이션을 수행한다.
  - MBR/부트 관련 명령은 실행하지 않고, "차단" 메시지만 출력한다.
  - 실제 권한 변경은 하지 않으며, 시뮬레이션 메시지만 출력한다.
요구사항
  (1) AES-256 암호화 시뮬레이션 : .NET Aes(256bit)로 샘플 데이터 암호화 -> .locked 결과물 생성(샌드박스 내)
  (2) MBR 손상 모방 : bootrec /fixmbr "차단" 출력 + 가짜 MBR 백업 파일 생성
  (3) 관리자 권한 요청/확인 : whoami /priv 출력, SeTakeOwnershipPrivilege "활성화 시뮬레이션" 메시지
  (4) 훈련용 안전 설계 : 실제 시스템 변경 없음, "훈련용 랜섬웨어 파일입니다." 메시지 출력
================================================================================
#>

# 엄격 모드 + 예외 시 중단
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Windows 환경 확인 (교육 과제 특성상 Windows 가정)
if (-not $env:OS -or ($env:OS -notlike 'Windows*')) {
  Write-Host "[안내] 이 스크립트는 Windows 환경을 가정합니다. 현재 OS: $($env:OS)" -ForegroundColor Yellow
}

# 전역 경로(샌드박스)
$SimRoot   = Join-Path $env:TEMP 'RansomwareTrainingSim'
$InDir     = Join-Path $SimRoot 'input'
$OutDir    = Join-Path $SimRoot 'output'
$LogFile   = Join-Path $SimRoot 'sim_log.txt'
$KeyFile   = Join-Path $SimRoot 'keys.json'
$MBRBackup = Join-Path $SimRoot 'mbr_backup.bin'

# 공용 로깅 함수
function Write-Log {
  param([string]$Message)
  $timestamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
  $line = "[$timestamp] $Message"
  $line | Out-File -FilePath $LogFile -Encoding UTF8 -Append
  Write-Host $Message
}

# 샌드박스/샘플파일 준비
function Initialize-SimEnvironment {
<#
설명:
  - TEMP 하위에 전용 폴더 생성
  - 샘플 파일 3개 생성 (실제 민감 파일과 무관)
#>
  foreach ($d in @($SimRoot, $InDir, $OutDir)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
  }

  @(
    @{ Name='report1.txt'; Content='Quarterly sales report sample data...' }
    @{ Name='notes.docx';  Content='Meeting notes - nothing sensitive (training only).' }
    @{ Name='image.jpg';   Content='[FAKE JPEG BYTES] **** TRAINING ONLY ****' }
  ) | ForEach-Object {
      $p = Join-Path $InDir $_.Name
      $_.Content | Out-File -FilePath $p -Encoding UTF8
    }

  # 가짜 MBR 백업(시뮬레이션용 바이트)
  [byte[]] $fake = 0x45,0x44,0x55,0x5F,0x4D,0x42,0x52,0x5F,0x44,0x41,0x54,0x41  # "EDU_MBR_DATA"
  Set-Content -Path $MBRBackup -Value $fake -Encoding Byte

  Write-Log "샌드박스 초기화 완료: $SimRoot"
  Write-Log "샘플 파일 생성: $(Get-ChildItem $InDir | Select-Object -ExpandProperty Name -Join ', ')"
}

# AES-256 암호화 시뮬레이션 (샘플 데이터 -> .locked 파일 생성)
function Invoke-Aes256EncryptionSimulation {
<#
설명
  - .NET System.Security.Cryptography.Aes 사용 (256bit)
  - 샌드박스 input 내 파일만 대상으로 "암호화본"을 output에 생성
  - 원본은 유지, 결과물 확장자는 .locked
  - 실제 사용자 파일/시스템 파일은 처리하지 않음
#>
  Add-Type -AssemblyName System.Security
  $aes = [System.Security.Cryptography.Aes]::Create()
  $aes.KeySize   = 256
  $aes.BlockSize = 128
  $aes.Mode      = [System.Security.Cryptography.CipherMode]::CBC
  $aes.Padding   = [System.Security.Cryptography.PaddingMode]::PKCS7

  # 난수 Key/IV 생성 & 보관
  $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
  $key = New-Object byte[] 32
  $iv  = New-Object byte[] 16
  $rng.GetBytes($key)
  $rng.GetBytes($iv)

  $meta = [pscustomobject]@{
    key_base64 = [Convert]::ToBase64String($key)
    iv_base64  = [Convert]::ToBase64String($iv)
    created_at = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
    note       = 'Training only. Not used to damage real files.'
  }
  $meta | ConvertTo-Json | Out-File -FilePath $KeyFile -Encoding UTF8

  $count = 0
  Get-ChildItem -Path $InDir -File | ForEach-Object {
    $src = $_.FullName
    $dst = Join-Path $OutDir ($_.Name + '.locked')

    # 파일 바이트 로드
    [byte[]]$plain = [System.IO.File]::ReadAllBytes($src)

    # 암호화 수행
    $encryptor = $aes.CreateEncryptor($key, $iv)
    $cipher = $encryptor.TransformFinalBlock($plain, 0, $plain.Length)
    [System.IO.File]::WriteAllBytes($dst, $cipher)

    $count++
    Write-Log "암호화 시뮬레이션 완료 -> $dst"
  }

  Write-Log "AES-256 암호화 시뮬레이션 총 $count 개 파일 처리(.locked)"
}

# MBR 손상 모방 (실제 명령 차단/미실행)
function Simulate-MBRTamper {
<#
설명
  - 'bootrec /fixmbr'는 실행하지 않음
  - 가짜 MBR 백업 파일을 생성해둔 상태에서, "손상 시뮬레이션/차단" 로그만 남김
  - 시스템 민감 경로 접근은 "시도 메시지"만 출력
#>
  Write-Log "MBR 손상 시뮬레이션 시작"
  Write-Log "위험 명령 차단: 'bootrec /fixmbr' 실행은 허용되지 않는다."
  if (Test-Path $MBRBackup) {
    Write-Log "가짜 MBR 백업 존재: $MBRBackup (실제 MBR과 무관)"
  } else {
    Write-Log "MBR 백업이 없어 새로 생성"
    [byte[]] $fake = 0x45,0x44,0x55,0x5F,0x4D,0x42,0x52,0x5F,0x44,0x41,0x54,0x41
    Set-Content -Path $MBRBackup -Value $fake -Encoding Byte
  }

  # 시스템 드라이브 민감 파일 접근 "시도" 시뮬레이션 (실제 읽기/변경 없음)
  $samPath = 'C:\Windows\System32\config\SAM'
  if (Test-Path $samPath) {
    Write-Log "민감 파일 접근 시뮬레이션: $samPath"
    Write-Log "접근 결과: 차단됨"
  } else {
    Write-Log "민감 파일 경로가 존재하지 않거나 접근 불가: $samPath"
  }

  Write-Log "MBR 손상 모방 완료"
}

# 권한 확인 및 'SeTakeOwnershipPrivilege 활성화' 시뮬레이션
function Simulate-PrivilegeElevation {
<#
설명
  - whoami /priv 로 현재 토큰 권한 나열
  - 'SeTakeOwnershipPrivilege' 활성화를 "시뮬레이션"으로만 처리 (실제 변경 없음)
  - icacls/takeown 사용 예시 커맨드는 문자열로만 출력하고 실행하지 않음
#>
  Write-Log "권한 상태 확인: whoami /priv"
  try {
    $privOut = (whoami /priv) 2>$null
    if ($privOut) { $privOut | ForEach-Object { Write-Host $_ } }
  } catch {
    Write-Log "whoami 실행 실패(환경에 따라 다를 수 있음): $($_.Exception.Message)"
  }

  # 실제 권한 변경 금지. 아래는 시뮬레이션 메시지/예시만 출력.
  Write-Log "권한 상승 시뮬레이션: SeTakeOwnershipPrivilege -> 활성화"

  $ex1 = 'takeown /F C:\TrainingOnly\dummy.txt'
  $ex2 = 'icacls C:\TrainingOnly\dummy.txt /grant Administrators:F'
  Write-Log "참고(시뮬레이션 명령 예시): $ex1"
  Write-Log "참고(시뮬레이션 명령 예시): $ex2"
}

# 메인
Write-Host "훈련용 랜섬웨어 파일" -ForegroundColor Cyan
Write-Log  "=== 시뮬레이션 시작 ==="

Initialize-SimEnvironment
Invoke-Aes256EncryptionSimulation
Simulate-MBRTamper
Simulate-PrivilegeElevation

Write-Log  "=== 시뮬레이션 종료 ==="
Write-Host "시뮬레이션 완료. 로그: $LogFile" -ForegroundColor Green

# 요약 출력
Write-Host "`n[요약]" -ForegroundColor White
Write-Host " - 샌드박스  : $SimRoot"
Write-Host " - 입력 폴더 : $InDir"
Write-Host " - 출력 폴더 : $OutDir (.locked 생성)"
Write-Host " - 키 메타   : $KeyFile"
Write-Host " - MBR 백업  : $MBRBackup"
Write-Host " - 로그 파일 : $LogFile"
