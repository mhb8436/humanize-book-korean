---
description: AI가 쓴 한글 IT 책 원고를 한국 IT 책 톤으로 윤문 (humanize-book-korean 스킬 호출)
argument-hint: [윤문할 파일 경로 또는 텍스트]
---

# /humanize-book — 한국 IT 책 톤 윤문

`humanize-book-korean` 스킬(v0.1)을 발동해 인자로 전달된 원고를 한국 IT 책 톤으로 윤문합니다. im-not-ai(humanize-korean) v2.0의 A~J 카테고리에 한국 IT 책 특화 P~W 카테고리를 더해 적용합니다.

## 입력
$ARGUMENTS

## 동작

1. 인자가 비었으면: "윤문할 파일 경로 또는 텍스트를 전달해 주세요" 안내 후 종료.
2. 인자가 파일 경로(.md)면 Read로 본문을 불러옵니다.
3. 인자가 텍스트면 그대로 입력으로 사용합니다.
4. `humanize-book-korean` 스킬 SKILL.md 절차에 따라 실행:
   - 첫 응답 한 줄로 버전 출력 (`humanize-book-korean v0.1 — {fast|strict} 모드 / run_id: ...`)
   - cwd 기준 `_workspace/{YYYY-MM-DD-NNN}/`에 새 run_id 생성
   - 도메인 추정 (cwd가 책 프로젝트면 자동, 아니면 사용자에게 물음)
   - 룰북 + 도메인 용어집 + 페르소나 보존 규칙 로드
   - `humanize-monolith` (fast) 또는 5인 파이프라인 (strict) 실행
5. 최종 결과 사용자에게 전달:
   - 윤문본 본문 (마크다운)
   - 카테고리별 탐지 건수 (A~J·P~W) before/after 표
   - 점수 변화 + 품질 등급 (A/B/C/D)
   - 주요 변경 하이라이트 5건 (Before → After)
   - 도메인 용어 보존 점검 결과
   - 등급 B 이하면 `/humanize-book-redo`로 2차 윤문 안내

## 옵션 (인자 끝에 자연어로 명시)

- `--strict` 또는 "정밀 모드" — 5인 파이프라인 강제 (장문·정밀 검증)
- `--domain {도메인}` — 도메인 명시 (예: `--domain spring-ai-book`)
- `--preserve-persona` — 페르소나 정보 100% 보존 (기본 활성)
- "이 절만" / "이 단락만" — 일부 영역만 윤문

## 본 스킬이 보존하는 것 (Do-NOT)

원본 humanize-korean의 Do-NOT 외에 추가로:
- **도메인 표준 용어** (사업자/발주처/민원관/공문 형식 등 — domain-glossary.md 기준)
- **페르소나 정보** (이름/소속/경력/직급 — persona.md 기준)
- **사용자 자바책 reference 톤** (examples/{domain}/reference-style/ 의 비슷한 단락과 매치)

## 사용 예

```
/humanize-book manuscript/part1/ch03-first-chatbot.md
/humanize-book manuscript/part0-intro/ch02-environment.md --strict
/humanize-book 이 한 단락만 윤문해 주세요: 이 장은 김과장의 ...
```
