# Humanize Book Korean — 한국 IT 책 톤 윤문 스킬

AI(ChatGPT · Claude · Gemini 등)가 쓴 한글 IT 책 원고를 **자연스러운 한국 IT 책 톤**으로 윤문하는 Claude Code 스킬입니다.

[im-not-ai (humanize-korean)](https://github.com/epoko77-ai/im-not-ai) v2.0을 base로, 한국 IT 책 특유의 영어식 패턴(자기 마케팅 · 학습 목표 마무리 · 객체에 책임 부여 · 당연한 사실 강조 · 도메인 용어 부정확)을 카테고리 **P ~ W**로 보강했습니다.

## 왜 한국 IT 책 특화인가

일반 한국어 윤문 도구(humanize-korean 포함)는 AI 글의 일반적인 번역투 · 관용구를 잘 잡지만, **한국 IT 책 특유의 영어식 패턴**은 못 잡습니다:

- 영어 IT 책의 "Why this chapter matters" → 본문 안 자기 마케팅 ("★ 핵심 차별화 장")
- "What this chapter creates is not X, but Y" → "이 장이 만드는 것은 코드가 아니라 ~ 골격입니다"
- "is responsible for" → 객체에 "책임" 부여 ("이 클래스의 책임을 한 줄씩 보자")
- "is pulled in / swap out / dropped" → "끌려 들어와 / 갈아끼우다 / RFP가 떨어진다"
- 미국 IT 책의 환영 멘트 → "함께 시작해 보시죠 / 다음 페이지에서 만난다"

본 스킬은 한국 IT 책 19권 분석(사용자 자바책 등) 기준으로 위 패턴을 모두 잡습니다.

## 주요 기능

| 기능 | 내용 |
|------|------|
| **A~J 카테고리** (원본) | 일반 한국어 AI 티 패턴 (번역투 · 영어 과다 · 기계 패턴 · AI 관용구 등) |
| **P~W 카테고리** (보강) | 한국 IT 책 특화 (학습 목표 마무리 · 책임 · 한국 IT 동사 · 자기 마케팅 · 당연한 사실 · 도메인 용어 · 책 마무리 · 공저 노트) |
| **모드** | Fast (5천자 이하, ~3분, monolith 한 콜) / Strict (8천자+, 5단계 파이프라인) |
| **품질 등급** | A~D 등급 + 카테고리별 before/after 카운트 |
| **도메인 분리** | examples/{domain}/ 폴더로 책마다 다른 도메인 용어집·페르소나 분리 |
| **4대 철칙** | 의미 불변 / 근거 기반 / 장르 유지 / 과윤문 금지 (50% 초과 중단) |

## 보강된 카테고리 (P~W)

| ID | 패턴 | Before | After |
|---|---|---|---|
| P-1 | 학습 목표 완성 | 이 N 가지가 완성되면 | N 가지를 학습하면 |
| Q-1 | 객체 책임 | 이 클래스의 책임을 보자 | 이 클래스가 하는 일을 보자 |
| R-1 | 영어 IT 동사 | 끌려 들어와 있고 | 의존성에 자동으로 추가되어 있고 |
| S-1 | ★ 표시 | ★ 핵심 차별화 장 | (제거) |
| T-1 | 당연한 사실 | 한국어 존댓말의 행정 안내문 | 행정 안내문 |
| U-1 | 도메인 용어 | 사업소 | 사업자 (공공 SI 표준) |
| V-1 | 책 마무리 멘트 | 다음 페이지에서 만난다 | (제거) |
| W-1 | 공저 노트 | "한국식 톤 재작성 적용" | (제거. git log·메모리에 두기) |

전체 패턴은 `references/book-extra-rules.md` 참조.

## 설치

```bash
git clone https://github.com/{user}/humanize-book-korean.git ~/Workspaces/humanize-book-korean

# 본인 책 프로젝트에 심볼릭 링크
cd ~/Workspaces/your-book
ln -s ~/Workspaces/humanize-book-korean/.claude/skills/humanize-book-korean \
      .claude/skills/humanize-book-korean
ln -s ~/Workspaces/humanize-book-korean/.claude/commands/humanize-book.md \
      .claude/commands/humanize-book.md
```

또는 install 스크립트:

```bash
~/Workspaces/humanize-book-korean/scripts/install.sh ~/Workspaces/your-book
```

## 사용법

```bash
# 한 챕터 윤문
/humanize-book manuscript/part1/ch03-first-chatbot.md

# 단락만 윤문 (텍스트 직접)
/humanize-book 이 장은 김과장의 자동 매핑 위에 Spring AI를 자연스럽게 얹는 작업입니다...

# 정밀 모드 (장문·5단계 파이프라인)
/humanize-book manuscript/part1/ch03.md --strict

# 도메인 명시
/humanize-book manuscript/part1/ch03.md --domain spring-ai-book
```

## 도메인 분리

본 스킬은 책마다 다른 **도메인 용어집 · 페르소나**를 `examples/{domain}/`에 분리합니다. 본 저장소에는 한 가지 도메인 예시가 들어 있습니다:

- `examples/spring-ai-book/` — 공공 SI · eGovFrame · Spring AI 책 사례
  - `domain-glossary.md` — 사업자 / 발주처 / 민원관 / 공문 형식 / 망분리 등 표준 용어
  - `persona.md` — 김과장 (공공 SI 10년 차 개발자)
  - `reference-style/` — 한국 IT 책 표준 톤의 reference (자바책 4개 장 발췌)
  - `book-tone-history.md` — 본 책 작업 중 발견된 패턴 누적

다른 책 작업 시 `examples/{your-book}/` 폴더를 만들고 자기 도메인에 맞게 수정하세요.

## 4대 철칙

원본 im-not-ai와 동일:

1. **의미 불변** — 사실 · 수치 · 고유명사 · 인용은 100% 보존
2. **근거 기반** — quick-rules에 매핑되지 않는 구간은 건드리지 않음
3. **장르 유지** — 한국 IT 실무서 톤 유지
4. **과윤문 금지** — 변경률 30% 초과 경고, 50% 초과 중단

추가:
5. **도메인 용어 보존** — examples/{domain}/domain-glossary.md 에 명시된 표준 용어 변경 금지
6. **페르소나 보존** — examples/{domain}/persona.md 의 인물 정보(이름 · 소속 · 경력) 100% 보존

## 디렉토리 구조

```
humanize-book-korean/
├── README.md (이 파일)
├── LICENSE (MIT)
├── CHANGELOG.md
├── CLAUDE.md                       # Claude Code 사용자 가이드
│
├── .claude/
│   ├── skills/humanize-book-korean/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── quick-rules.md      # A~J (im-not-ai 원본)
│   │       ├── book-extra-rules.md # P~W (한국 IT 책 보강)
│   │       ├── user-style-traits.md # 한국 IT 책 톤 8가지 특징
│   │       ├── ai-tell-taxonomy.md
│   │       ├── rewriting-playbook.md
│   │       ├── scholarship.md
│   │       ├── metrics.py
│   │       ├── metrics_v2.py
│   │       └── baseline.json
│   ├── agents/                     # 11개 에이전트 (im-not-ai 자산)
│   └── commands/
│       ├── humanize.md             # /humanize (원본)
│       ├── humanize-redo.md
│       └── humanize-book.md        # /humanize-book (본 스킬)
│
├── examples/                        # 도메인별 자산
│   ├── README.md
│   └── spring-ai-book/             # 공공 SI · Spring AI 책
│       ├── domain-glossary.md
│       ├── persona.md
│       ├── book-tone-history.md
│       └── reference-style/        # 한국 IT 책 표준 톤 reference
│
├── scripts/                         # 빠른 정규식 도구
│   ├── apply-tone-fast.py          # sed 일괄 변환 (수 초)
│   ├── check-tone.py               # 위반 자동 점검
│   └── install.sh                  # 다른 책 프로젝트에 설치
│
└── tests/                           # 회귀 테스트
    └── fixtures/
```

## 3-Stage 작업 흐름 (권장)

본 스킬은 다른 도구와 함께 다음 3단계로 사용하면 효율적입니다:

```
[Stage 1] scripts/apply-tone-fast.py
   - 300+ sed 패턴 일괄 변환 (수 초)
   - 결정적, 70~80% 처리

[Stage 2] scripts/check-tone.py
   - 잔류 위반 자동 점검 (수 초)
   - 15+ 카테고리

[Stage 3] /humanize-book (스킬)
   - 깊은 윤문 (LLM 호출, ~3분)
   - 의미 보존 + 톤 자연화 + 페르소나·도메인 용어 보존
   - 5단계 파이프라인
```

## 기여

본 스킬은 한국 IT 책 작업을 통해 계속 발전합니다.

- **새 패턴 발견**: `references/book-extra-rules.md`에 카테고리 ID 추가 + PR
- **새 도메인**: `examples/{your-domain}/` 폴더 추가 + PR
- **메트릭 보강**: `references/metrics.py`에 측정 함수 추가 + PR

## 라이선스

MIT License. 원본 [im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 자산을 base로 합니다 (Attribution 포함).

## 감사

- [im-not-ai (epoko77-ai)](https://github.com/epoko77-ai/im-not-ai) — base 스킬 v2.0
- [이오덕 「우리글 바로쓰기」](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=5980421) — 영어 번역투 비판의 학술 기초
- 한국 번역학계 8유형 (이근희·김정우 등) — Toral 2019 simplification/normalisation/interference 매핑
- 사용자 자바책 19권 — 한국 IT 책 톤의 reference 코퍼스
