# Nova Parts Calculator

Nova Parts Calculator는 실시간 전략 게임 노바 1492의 부품 조합 능력치를 계산하는 Python 기반 GUI 데스크톱 앱입니다.

## 주요 기능

- 다리, 몸통, 무기, 액세서리 부품 선택
- 부품별 강화 수치 입력
- 서브코어와 보너스 수치를 반영한 능력치 계산
- 조합 결과의 무게, 와트, 체력, 공격력, 방어력 등 확인

## 지원 환경

- Windows 전용
- Python 3
- PyQt5

일반 사용자는 GitHub Release에서 배포용 압축 파일을 내려받아 사용할 수 있습니다. 개발자는 Python 환경에서 직접 실행하거나 PyInstaller로 Windows 실행 파일을 빌드할 수 있습니다.

## 실행 방법

소스에서 직접 실행하려면 프로젝트 루트에서 아래 명령을 실행합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe calculator.py
```

## 빌드 방법

Windows 실행 파일은 아래 명령으로 빌드합니다.

```powershell
.\build.ps1
```

빌드 결과는 아래 경로에 생성됩니다.

```text
dist\NovaPartsCalculator\NovaPartsCalculator.exe
```

현재 빌드는 PyInstaller의 폴더형 배포 방식입니다. 실행 파일 하나만 옮기지 말고 `dist\NovaPartsCalculator` 폴더 전체를 배포해야 합니다.

`build` 폴더는 PyInstaller 임시 작업 폴더입니다. 이 폴더 안의 실행 파일은 배포용이 아니며 DLL 오류가 발생할 수 있습니다.

## GitHub Release 배포

릴리스 배포 시에는 아래 흐름을 권장합니다.

1. `.\build.ps1`로 새 빌드를 생성합니다.
2. `dist\NovaPartsCalculator` 폴더를 압축합니다.
3. GitHub Release를 생성하고 압축 파일을 첨부합니다.
4. 릴리스 노트에는 변경된 기능, 수정된 버그, 알려진 문제를 정리합니다.

## 프로젝트 구조

```text
.
|-- calculator.py          # 메인 GUI 진입점
|-- assemble.py            # 조합 능력치 계산 로직
|-- partSelector.py        # 부품 선택 다이얼로그
|-- typeSelector.py        # 타입 선택 다이얼로그
|-- constant.py            # 공통 상수와 리소스 경로
|-- utils.py               # 계산 보조 함수
|-- *.ui                   # Qt Designer UI 파일
|-- JSON/                  # 부품 및 서브코어 데이터
|-- build.ps1              # Windows 빌드 스크립트
|-- BUILD.md               # 빌드 상세 문서
`-- requirements.txt       # Python 의존성
```

## 제작자

- 제작자: [ThunderVolt_45](https://www.youtube.com/@ThunderVolt45/)

## 라이선스

이 프로젝트는 [LICENSE](LICENSE)를 따릅니다.
