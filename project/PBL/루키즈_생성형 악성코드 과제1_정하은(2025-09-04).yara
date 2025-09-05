import "pe"

rule Ransomware_A1 {
    meta:
        assignment   = "루키즈_생성형 악성코드 과제1"
        description  = "랜섬웨어 탐지"
        author       = "정하은"
        date         = "2025-09-04"
        version      = "A1"
        notes        = "AES/OpenSSL + MBR경로+저수준API + 권한문자열을 동시 충족. VSS/임포트는 보조 신호"

    strings:
        // [1] 암호화 관련
        $enc.aes256 = "AES-256" ascii wide nocase fullword
        $enc.evp1   = "EVP_EncryptInit_ex" ascii wide
        $enc.evp2   = "EVP_CipherInit_ex"  ascii wide

        // [2] MBR 훼손/저수준 디스크 접근
        $mbr.path1 = "\\\\PhysicalDrive0" ascii wide
        $mbr.path2 = "\\\\Device\\\\Harddisk0\\\\DR0" ascii wide
        $mbr.api.wf  = "WriteFile" ascii wide        // 실제 덮어쓰기 시도
        $mbr.api.dio = "DeviceIoControl" ascii wide  // 장치 제어 코드 호출

        // [3] 관리자 권한 획득 시도
        $priv.sedebug = "SeDebugPrivilege" ascii wide
        $priv.seshut  = "SeShutdownPrivilege" ascii wide
        $priv.token   = "TokenPrivileges" ascii wide

        // [4] (보조) 권한 API 임포트 흔적
        $priv.api.adj = "AdjustTokenPrivileges" ascii wide
        $priv.api.opt = "OpenProcessToken" ascii wide

        // [5] (보조) 백업/복구/로그 무력화 흔적
        $vss.1 = "vssadmin Delete Shadows" ascii wide nocase
        $vss.2 = "wbadmin delete catalog" ascii wide nocase
        $vss.3 = "wevtutil cl" ascii wide nocase
        $vss.4 = "bcdedit /set {default} recoveryenabled No" ascii wide nocase

    condition:
        // [A] 실행 파일 제한 + 파일 크기 제한
        pe.is_pe and filesize in (100KB..5MB)

        // [B] 암호화 지표: AES-256 또는 EVP 초기화(≥1)
        and ( $enc.aes256 or $enc.evp1 or $enc.evp2 )

        // [C] MBR 훼손 시도: 경로(≥1) AND 저수준 API(≥1)
        and ( ( $mbr.path1 or $mbr.path2 ) and ( $mbr.api.wf or $mbr.api.dio ) )

        // [D] 권한 상승 시도: 권한 문자열(≥1)
        and ( $priv.sedebug or $priv.seshut or $priv.token )

        // [E] (보조) VSS/임포트 흔적
        and ( 1 of ($vss*) or 1 of ($priv.api*) )
}
