# AGENTS.md

이 문서는 Nova Parts Calculator를 개발하거나 수정하는 사람과 자동화 에이전트가 따라야 할 작업 기준을 정리합니다.

## 프로젝트 개요

Nova Parts Calculator는 실시간 전략 게임 노바 1492의 부품 조합 능력치를 계산하는 Windows 전용 Python GUI 데스크톱 앱입니다.

주요 기술 스택은 다음과 같습니다.

- Python
- PyQt5
- Qt Designer `.ui` 파일
- JSON 기반 부품 데이터
- PyInstaller 기반 Windows 빌드

## 작업 원칙

- 기존 PyQt5 구조와 파일 배치를 우선 유지합니다.
- 계산 로직 변경 시 `assemble.py`, `utils.py`, `calculator.py`의 역할을 구분합니다.
- UI 배치 변경은 가능한 한 `.ui` 파일과 해당 Python 연결 코드의 책임을 분리해서 처리합니다.
- 부품 데이터는 `JSON` 디렉터리의 기존 스키마를 유지합니다.
- 빌드 산출물은 커밋하지 않습니다. `build`, `dist`, `.venv`, `__pycache__`, `*.spec`는 작업 산출물로 취급합니다.
- PyInstaller 리소스 경로는 `sys._MEIPASS` 환경에서도 동작해야 합니다.

## 주요 파일

| 파일 | 역할 |
| --- | --- |
| `calculator.py` | 메인 윈도우와 사용자 입력 처리 |
| `assemble.py` | 부품 조합 능력치 계산 |
| `utils.py` | 강화 수치 등 계산 보조 함수 |
| `constant.py` | 상수와 리소스 경로 |
| `partSelector.py` | 부품 선택 다이얼로그 |
| `typeSelector.py` | 타입 선택 다이얼로그 |
| `calculator.ui` | 메인 윈도우 UI |
| `partSelector.ui` | 부품 선택 UI |
| `typeSelector.ui` | 타입 선택 UI |
| `JSON/*.json` | 부품 및 서브코어 데이터 |
| `build.ps1` | Windows 빌드 스크립트 |

## 실행 및 빌드

개발 중 실행:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe calculator.py
```

Windows 빌드:

```powershell
.\build.ps1
```

배포 대상은 `dist\NovaPartsCalculator` 폴더 전체입니다. `build` 폴더 안의 파일은 임시 빌드 산출물이므로 실행하거나 배포하지 않습니다.

## 브랜치 전략

이 프로젝트는 단순한 `main - feature` 구조를 사용합니다.

| 브랜치 | 용도 |
| --- | --- |
| `main` | 출시 가능한 안정 버전. 직접 커밋하지 않고 PR을 통해 반영합니다. |
| `feature/[기능명]` | 개별 작업 브랜치. `main`에서 분기하고 PR 병합 후 삭제합니다. |

브랜치 예시:

```text
feature/build-docs
feature/part-data-update
feature/ui-polish
```

## 커밋 메시지 규칙

커밋 메시지는 아래 형식을 사용합니다.

```text
[태그]: [작업 내용 요약 50자 이내]

[상세 내용 선택]
- (수정/추가한 파일): (작업 내용)
- (수정/추가한 파일): (작업 내용)

[이슈 번호 선택] 예: Resolve #12
```

예시:

```text
Docs: 빌드 및 배포 문서 추가

- README.md: 실행 및 GitHub Release 배포 방법 정리
- AGENTS.md: 개발 작업 규칙 추가
```

### 태그 목록

| 태그 | 용도 |
| --- | --- |
| `Feat` | 새로운 기능 추가 |
| `Fix` | 버그 및 오류 수정 |
| `Design` | UI/UX 구조, 레이아웃, 시각적 변경 |
| `Refactor` | 기능 변화 없는 코드 구조 개선 |
| `Docs` | 문서 작성 및 수정 |
| `Chore` | 빌드, 패키징, 설정 등 기타 작업 |

## PR 기준

- PR은 `feature/[기능명]` 브랜치에서 `main`으로 생성합니다.
- PR 설명에는 변경 요약, 테스트 여부, 배포 영향이 있으면 함께 적습니다.
- 계산 로직, JSON 데이터, 빌드 스크립트 변경은 실행 또는 빌드 검증 결과를 남깁니다.
- GitHub Release 대상 변경이라면 릴리스 노트에 들어갈 내용을 PR에 정리합니다.

## 검증 체크리스트

변경 내용에 따라 아래 항목을 확인합니다.

- Python 문법 검사: `python -m py_compile assemble.py calculator.py constant.py partSelector.py typeSelector.py utils.py`
- 앱 실행 확인: `.\.venv\Scripts\python.exe calculator.py`
- Windows 빌드 확인: `.\build.ps1`
- 배포 폴더 확인: `dist\NovaPartsCalculator\NovaPartsCalculator.exe`

GUI 실행이나 빌드를 현재 환경에서 확인할 수 없는 경우, 문서나 PR에 그 이유를 명확히 남깁니다.
