# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

본 저장소는 **앱이 아니라 Claude Code 스킬 패키지**입니다. 여기서 하는 작업의 대부분은
코드 디버깅이 아니라 **규칙 마크다운(references/·book-extra-rules) 편집과 정규식 스크립트 보강**입니다.

## 이 저장소가 하는 일

AI(ChatGPT·Claude·Gemini)로 1차 작성된 한글 IT 책 원고를 자연스러운 한국 IT 책 톤으로 윤문하는
스킬입니다. [im-not-ai (humanize-korean)](https://github.com/epoko77-ai/im-not-ai) v2.0을 base로
하고, 한국 IT 책 특유의 영어식 패턴(자기 마케팅·학습 목표 마무리·객체에 "책임" 부여·당연한 사실
강조·도메인 용어 부정확)을 카테고리 **P~Z**로 보강했습니다.

이 저장소는 **규칙의 단일 진실 공급원(SSOT)** 입니다. 실제 원고는 별도 책 프로젝트(예:
`~/Workspaces/your-book/manuscript/`)에 있고, 그 프로젝트가 이 저장소를 심볼릭 링크해서 씁니다.

## 자주 쓰는 명령

자동화된 테스트 러너·빌드·린트는 **없습니다**. 핵심 도구는 두 개의 표준 라이브러리 파이썬
스크립트이며, 둘 다 **책 원고 프로젝트 안에서** 실행하도록 설계됐습니다(이 저장소에는 `manuscript/`가
없으므로 항상 경로를 명시).

```bash
# 1단계 — 안전한 패턴 일괄 정규식 치환 (수 초, 결정적)
python3 scripts/apply-tone-fast.py path/to/file.md          # 단일 파일
python3 scripts/apply-tone-fast.py manuscript/              # 디렉토리 재귀
python3 scripts/apply-tone-fast.py --dry-run manuscript/    # 미리보기(파일 안 씀)

# 2단계 — 잔류 위반 점검 (수 초). 종료코드 0=위반없음 / 1=위반있음 / 2=사용법오류
python3 scripts/check-tone.py path/to/file.md
python3 scripts/check-tone.py manuscript/part0-intro/
#   ⚠️ 인자 없이 실행하면 <repo>/manuscript 를 찾는데, 이 저장소엔 없으므로 항상 경로를 줄 것.

# 스킬 설치 — macOS/Linux. examples/ 도 스킬 폴더에 포함돼 함께 설치됨.
scripts/install.sh --global                 # ~/.claude 글로벌 (터미널·Desktop·모든 책에서 인식)
scripts/install.sh ~/Workspaces/your-book   # 특정 프로젝트만 (기본 --link, 독립 사본은 --copy)
# Windows 네이티브:  .\scripts\install.ps1 -Global   (기본 -Copy, 심볼릭 링크는 -Link)

# 메트릭(스킬 fast-path 전처리기) — 단독으로도 실행 가능
python3 .claude/skills/humanize-book-korean/references/metrics.py \
    --input run/01_input.txt --genre essay --output run/00_metrics.json
```

> 회귀 테스트: `tests/fixtures/`는 현재 **비어 있습니다**. README·SKILL.md가 회귀 fixture를
> 언급하지만 아직 구현되지 않았습니다. 새 패턴을 추가하면 검증은 보통 `check-tone.py`를
> reference-style 코퍼스에 돌려 0건 매치를 확인하는 수동 방식입니다.

## 아키텍처 — 큰 그림

여러 파일을 동시에 읽어야 이해되는 핵심 구조는 다음 4가지입니다.

### 1. 2층 규칙 체계 (base 보존 / 보강 누적)

- **A~J (im-not-ai 원본, 절대 임의 수정 금지)** — 일반 한국어 AI 티 패턴.
  `references/quick-rules.md`(fast 슬림본)·`references/ai-tell-taxonomy.md`(strict 전수본)에 있음.
  학술 기반(이근희·김정우·Toral 2019)은 `references/scholarship.md`.
- **P~Z (이 저장소가 추가, 누적식)** — 한국 IT 책 특화 패턴.
  전부 `references/book-extra-rules.md` 한 파일에 있음. **append-only**: 새 패턴은 기존 ID를
  고치지 말고 `X-32`, `Q-5`처럼 다음 번호로 추가. X 카테고리는 사용자가 책 작업 중 짚은
  영어 직역체가 라운드마다 쌓인 결과(현재 X-31까지).

### 2. 2개 실행 경로 — 결정적 스크립트 vs LLM 스킬

같은 패턴을 두 가지 방식으로 잡습니다. 의도된 3단계 분업:

```
[1단계] scripts/apply-tone-fast.py  — 300+ 정규식 일괄 치환, 결정적, 70~80% 처리 (수 초)
[2단계] scripts/check-tone.py       — 15+ 카테고리 잔류 점검, 사람이 손볼 목록 출력 (수 초)
[3단계] /humanize-book (스킬)        — LLM 깊은 윤문, 의미 보존·페르소나·도메인 용어 검증 (~3분)
```

스크립트의 정규식과 스킬의 룰북은 **같은 카테고리를 공유**합니다. 그래서 새 패턴을 추가할 때
양쪽(book-extra-rules.md **그리고** check-tone.py/apply-tone-fast.py)을 함께 갱신해야 자동
검출 사이클이 다음 챕터에서 동작합니다(CHANGELOG v0.11.0 참조).

> 두 스크립트의 철칙: **코드 블록(` ``` … ``` `) 안은 절대 건드리지 않음.** 표준 라이브러리만 사용.

### 3. 스킬 내부 — Fast(기본) vs Strict 모드

스킬 진입점은 `.claude/skills/humanize-book-korean/SKILL.md`. 두 경로가 있습니다.

- **Fast(기본)** — `humanize-monolith` 에이전트를 **한 번** 호출해 탐지·윤문·자체검증을 일괄
  수행. 5,000자 이하 2~3분 목표. 8,000자 초과 또는 `--strict` 명시면 strict로 자동 승급.
- **Strict** — 5인 파이프라인: `ai-tell-detector` → `korean-style-rewriter` →
  (`content-fidelity-auditor` ∥ `naturalness-reviewer`) → 종합 판정 → 최대 3회 재윤문.

에이전트 정의는 `.claude/agents/*.md`(12개). 모두 `model: opus`. 산출물은 cwd 기준
`_workspace/{YYYY-MM-DD-NNN}/`에 `01_input.txt`·`final.md`·`summary.md` 등으로 떨어집니다.

> **알려진 결함의 교훈 (v0.10.0):** SKILL.md는 "필수 참조 자료 5건"(quick-rules·
> book-extra-rules·user-style-traits·domain-glossary·persona)을 monolith에 넘기라고 규정합니다.
> 한때 `quick_rules_path` 하나만 넘겨서 P~Z 패턴·도메인 어휘가 적용되지 않았습니다. SKILL.md
> Phase 2의 입력 경로 목록을 손볼 때 5건이 전부 전달되는지 반드시 확인하세요.

### 4. 도메인 분리 — examples/{domain}/

책마다 다른 용어·인물은 공통 규칙과 분리해 **스킬 폴더 안** `examples/{domain}/`(`.claude/skills/humanize-book-korean/examples/`)에 둡니다. 스킬 폴더 내부에 두는 이유는 install이 스킬을 통째로 복사·링크할 때 도메인 자산이 함께 따라오고, 향후 플러그인 패키징(자기 디렉토리 밖 참조 불가) 시에도 호환되기 때문입니다.

- `domain-glossary.md` — 표준 용어. **윤문 대상에서 제외**(다른 표현으로 바꾸지 않음).
- `persona.md` — 가상 인물 정보(이름·소속·경력). **100% 보존**.
- `reference-style/` — 한국 IT 책 표준 톤 reference. 윤문 톤이 여기 맞는지 검증.
- `book-tone-history.md` — 책 작업 중 누적된 패턴(다음 작업의 SSOT).

현재 예시는 `examples/spring-ai-book/`(공공 SI·eGovFrame·Spring AI) 하나. 카테고리 **U**
(사업자/발주처/민원인 등)는 이 도메인에 한정되며, 다른 도메인 책은 자기 glossary로 분리합니다.

## 불변 규칙 (윤문 작업 시 반드시 지킬 것)

1. **의미 불변** — 사실·수치·고유명사·직접 인용·법률 조문·영어 약어는 100% 보존, 탐지/윤문 대상 아님.
2. **근거 기반** — 룰북에 매핑되지 않는 구간은 건드리지 않음.
3. **장르·register 유지** — 격식체 입력 → 격식체 출력. AI 티는 문법·수사이지 격식 자체가 아님.
4. **과윤문 금지** — 변경률 **30% 초과 경고, 50% 초과 강제 중단/롤백**.
5. **도메인 용어 보존** — `examples/{domain}/domain-glossary.md`의 표준 용어 변경 금지.
6. **페르소나 보존** — `examples/{domain}/persona.md`의 인물 정보 변경 금지.
7. **자동 로드 금지** — 프로젝트 CLAUDE.md 등 다른 파일을 자동 파싱해 옵션을 추론하지 않음.

## 저장소 자체를 수정할 때

**새 패턴 추가:** `references/book-extra-rules.md`에 다음 ID로 추가(Before/After 각 1줄) →
`scripts/check-tone.py`(+ 자동 치환이 안전하면 `apply-tone-fast.py`)에 정규식 추가 →
`examples/{domain}/playbook-*.md`에 사례 → `CHANGELOG.md` 항목.

**새 도메인 등록:** `examples/{domain}/` 폴더 신설 → `domain-glossary.md`·`persona.md` 작성 →
`examples/README.md`에 등록.

**메트릭 보강:** `references/metrics.py`/`metrics_v2.py`에 측정 함수 추가 →
`references/baseline.json`/`baseline_v2.json`에 보정값 셀 추가. **표준 라이브러리만**
(konlpy·mecab·spaCy 금지 — 형태소 분석은 정규식+접미사 사전으로 근사).

**버전 관리:** SKILL.md frontmatter `version` + `CHANGELOG.md`(Keep a Changelog 형식)를
함께 갱신. 커밋 메시지에 `vX.Y.Z — 한 줄 요약`. push는 사용자 승인 후.

> SKILL.md 본문에는 아직 "v0.1"이라는 표기가 곳곳에 남아 있지만, 정식 버전은 frontmatter의
> `version`(현재 0.12.0)과 CHANGELOG가 기준입니다.

## 다른 책 프로젝트에서 사용할 때

```bash
# macOS / Linux — 글로벌(모든 책에서 인식) 또는 특정 프로젝트
scripts/install.sh --global
scripts/install.sh ~/Workspaces/your-book          # --link(기본) | --copy
```
```powershell
# Windows (네이티브, WSL 불필요)
.\scripts\install.ps1 -Global                       # -Copy(기본) | -Link
.\scripts\install.ps1 C:\path\to\your-book
```

스킬·에이전트·명령·도메인 자산이 한 번에 설치됩니다. 새 도메인은 스킬 폴더의
`examples/your-book/`에 `domain-glossary.md`·`persona.md`를 만든 뒤
`/humanize-book --domain your-book`으로 호출합니다.

## 핵심 파일 지도

- `README.md` — 외부 사용자 안내 / `CHANGELOG.md` — 버전 이력(패턴 추가 근거가 여기 쌓임)
- `.claude/skills/humanize-book-korean/SKILL.md` — 스킬 절차(Fast/Strict, run_id, 입력 경로)
- `references/quick-rules.md` — A~J 슬림 룰북(Fast 전용)
- `references/ai-tell-taxonomy.md` — A~J 전수 분류(Strict 전용)
- `references/book-extra-rules.md` — **P~Z 보강 카테고리(이 저장소의 핵심 자산)**
- `references/rewriting-playbook.md` — 카테고리별 치환 레시피
- `references/scholarship.md` — 한국 번역학계 학술 기초
- `scripts/{apply-tone-fast,check-tone}.py` — 결정적 정규식 도구 / `scripts/install.{sh,ps1}` — 설치(mac·Linux / Windows)
- `.claude/skills/humanize-book-korean/examples/spring-ai-book/` — 도메인 자산 예시(용어·페르소나·reference 톤)
