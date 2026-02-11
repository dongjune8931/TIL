# TIL in AWS CLOUD SCHOOL 13th

매일 배운 것을 기록하고, 자동으로 정리해서 발행하는 프로젝트입니다.

## 동작 방식그리고 

```
Notion (작성) → OpenAI (정제) → GitHub (발행)
```

1. **Notion**에 오늘 배운 내용을 작성하고 상태를 `작성완료`로 변경
2. **GitHub Actions**가 매일 23:30(KST)에 자동 실행
3. **OpenAI GPT-4**가 내용을 구조화하고 보완
4. 정제된 마크다운 파일이 `docs/YYYY/MM/YYYY-MM-DD.md`로 저장
5. Notion 페이지 상태가 `발행완료`로 자동 업데이트

## 최근 학습 기록

| 날짜 | 제목 | 카테고리 | 한줄요약 |
|------|------|----------|----------|
| 2026-02-10 | [네트워크 기본 ( 02 )](docs/2026/02/2026-02-10.md) | `네트워크` | - 네트워크 서브네팅과 라우팅의 기본 개념 학습.
| 2026-02-11 | [네트워크 기본(03)](docs/2026/02/2026-02-11.md) | `네트워크` | - OSPF는 최단 경로 계산, DHCP는 IP 자동 할당 프로토콜입니다.
| 2026-02-09 | [네트워크 기본 01](docs/2026/02/2026-02-09.md) | `네트워크` | - 네트워크 통신을 위한 OSI 7계층과 IP 주소 체계 이해.

## 프로젝트 구조

```
TIL/
├── .github/workflows/
│   └── til-automation.yml    # GitHub Actions 워크플로우
├── scripts/
│   ├── process-til.py        # 메인 실행 스크립트
│   ├── notion_handler.py     # Notion API 연동
│   ├── openai_handler.py     # OpenAI API 연동
│   └── github_handler.py     # 파일 저장 및 README 관리
├── docs/                     # 발행된 TIL 저장소
│   └── YYYY/MM/YYYY-MM-DD.md
└── README.md
```

## Notion DB 설정

| 프로퍼티 | 타입 | 설명 |
|---------|------|------|
| 제목 | Title | TIL 제목 |
| 카테고리 | Select | Python, JavaScript, Algorithm, Database, DevOps, ETC |
| 태그 | Multi-select | 세부 키워드 |
| 날짜 | Date | 작성 날짜 |
| 상태 | Select | `작성완료` → `발행완료` |

## 설정 방법

### 1. Notion Integration

- [Notion Integrations](https://www.notion.so/my-integrations)에서 Integration 생성
- Notion DB에 해당 Integration 커넥션 추가

### 2. GitHub Secrets

Repository **Settings → Secrets and variables → Actions**에서 추가:

| Secret | 설명 |
|--------|------|
| `NOTION_TOKEN` | Notion Integration 토큰 |
| `NOTION_DATABASE_ID` | Notion 데이터베이스 ID |
| `OPENAI_API_KEY` | OpenAI API 키 |

### 3. 실행

- **자동**: 매일 23:30(KST) GitHub Actions 실행
- **수동**: Actions 탭 → TIL Automation → Run workflow

## 기술 스택

- **Python 3.11**
- **Notion API** - 콘텐츠 소스
- **OpenAI GPT-4** - 내용 정제
- **GitHub Actions** - 자동화 스케줄링