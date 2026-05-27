# Changelog

본 스킬의 모든 변경 사항을 기록합니다. [Keep a Changelog](https://keepachangelog.com/) 형식을 따릅니다.

## [Unreleased]

### Planned
- v1.0.0: `metrics_v2.py`에 신규 측정 함수 3개 (`count_emphatic_numerals`, `count_align_verbs`, `count_abstract_subj_with_control_verb`) + `baseline_v2.json` 보정값
- v1.0.0: 표준국어대사전 OpenAPI 연동 (도메인 용어 자동 검증)

## [0.10.0] — 2026-05-27 (에이전트 컨텍스트 누락 fix — 핵심 결함 수정)

### Fixed — 에이전트가 도메인 글로서리·book-extra-rules를 안 읽던 버그

**증상**: SKILL.md `Phase 0`에는 "필수 참조 자료 5건"(quick-rules·book-extra-rules·user-style-traits·domain-glossary·persona)이 명시되어 있지만, 실제 `humanize-monolith` 에이전트는 `quick_rules_path` 한 개만 입력으로 받아 그것만 Read했다. 결과적으로 한국 IT 책 특화 패턴(P~Z 카테고리·X-1~X-28)과 도메인 표준 어휘(시민→민원인, 민원관→민원 공무원)가 자동으로 적용되지 않았다.

사용자 코멘트: "스킬에 분명히 먹였는데 말을 안듣는 이유가 뭘까?" — 정확한 진단. SKILL.md의 문구는 사람용 문서, 에이전트는 입력 인자로 받은 파일만 Read하는 구조였다.

### Changed — humanize-monolith.md (에이전트 정의)

- **입력 인자 확장**:
  - 기존: `input_path`, `quick_rules_path`, `genre_hint` (3개)
  - 신규: `book_extra_rules_path`, `user_style_traits_path`, `domain_glossary_path`(선택), `persona_path`(선택) 추가 (총 7개)
- **단계 1 컨텍스트 로드 확장**: Read 횟수 2회 → 3~5회. quick-rules.md 하나가 아니라 book-extra-rules·user-style-traits·domain-glossary·persona를 모두 Read.
- **단계 2 탐지 확장**: 도메인 어휘 탐지를 **최우선**으로 추가. P~Z 카테고리 탐지 명시.
- **단계 3 윤문 순서 변경**: **0순위로 도메인 어휘 치환** 추가 (domain-glossary 매핑 일괄 적용). 일반 명사 의미(일반 시민·조례 본문 등) 보존 규칙 명시.
- **단계 4 자체검증 강화**: domain-glossary의 비표준 용어 0건 검증·페르소나 정보 보존 검증 추가.
- **총 도구 호출**: 3회 → 5~8회 (Read만 늘고 Write는 그대로 1회)

### Changed — SKILL.md

- Phase 2 monolith 호출부에 4개 추가 경로(book_extra_rules·user_style_traits·domain_glossary·persona) 전달 명시.
- "domain은 cwd의 book-context.yaml에서 결정. 없으면 사용자 인자 또는 cwd 기준 가장 가까운 glossary 자동 탐색" 명시.
- "book_extra_rules_path와 domain_glossary_path를 빠뜨리면 P~Z 카테고리·도메인 어휘 치환이 적용되지 않는다" 경고 추가.

### Impact

v0.10.0 이후 humanize를 호출하면:
1. book-extra-rules의 X-1~X-28 한국 IT 책 패턴이 자동 탐지·치환됨
2. domain-glossary의 도메인 표준 어휘가 일반 패턴 처리보다 **우선적으로** 적용됨
3. persona.md의 페르소나 정보가 자체검증 단계에서 보존 확인됨
4. v0.9 이전 윤문 결과에서 잔류했던 "시민(페르소나 의미)"·"민원관"·"표면"·"본질" 등이 자동으로 잡힘

이전까지는 사용자가 매번 수동으로 패턴 발견 → CLAUDE.md/check_korean_tone.py에 등록 → 다음 챕터에 적용하는 사이클이 필요했다. v0.10.0부터는 humanize 한 콜에서 끝난다.

## [0.9.0] — 2026-05-27 (책 전체 어휘 정비)

### Changed — 도메인 페르소나 어휘 표준화

본 책 사례(spring-ai-book)에서 두 가지 핵심 도메인 어휘를 한국 표준 (민원처리법 + 표준국어대사전)에 맞게 일괄 정비.

- **"민원관" → "민원 공무원"** (책 전체 49건 일괄 치환)
  - 사유: "민원관"은 표준국어대사전 미등재 비표준어. 한국 민원처리법은 "민원 공무원"을 표준 용어로 정의.
  - 영향 범위: 본 책 16장 + 5 부록 + 도식 spec 파일 전체
- **"시민" (페르소나 의미) → "민원인"** (책 전체 약 200건 일괄 치환)
  - 사유: 챗봇·자동화 시스템의 응대 대상을 가리킬 때 "시민"보다 "민원인"이 한국 행정 표준에 부합 (민원처리법 정의: "행정 서비스를 신청·요청하는 사람").
  - 일반 명사 의미 보존: "일반 시민", "○○시민의 자전거 이용을 활성화"(조례 본문 인용), "시민의 권리", "시민 사회" 등은 그대로.
  - sed 마커 치환 기법으로 페르소나 vs 일반 명사 구분 처리.

### Updated
- `examples/spring-ai-book/domain-glossary.md` 섹션 2·3·5·7 어휘 표 갱신, v0.9 변경 이력 명시
- `examples/spring-ai-book/persona.md` "v0.9 챗봇 사용자 페르소나" 절 신설, "민원관"·"시민(페르소나 의미)" 금지 명시

### Workflow Established

도메인 어휘를 책 전체에 안전하게 치환하는 sed 기법:

```bash
# 1) 보존 패턴을 마커로 임시 치환
sed -i '' -e 's/일반 시민/__일반시민__/g' -e 's/시민 사회/__시민사회__/g' "$f"

# 2) 페르소나 의미 일괄 치환
sed -i '' 's/시민/민원인/g' "$f"

# 3) 마커 복원
sed -i '' -e 's/__일반시민__/일반 시민/g' -e 's/__시민사회__/시민 사회/g' "$f"
```

조례 본문, 인용문, 고유명사가 섞인 도메인 어휘 정비 시 유용한 패턴.

## [0.3.0] — 2026-05-27 (ch03 점검 누적)

### Added — X 카테고리 3개 확장

- **X-11** "결승점 / 마침점 / 종착점" 비유 명사 — 영어 "the finish line of this chapter" 직역. 본 책 전체에서 10건 발견 (ch03 3건, ch06 2건, ch07 1건, ch16 4건).
- **X-12** "의도된 단순화 / 의도된 간소화" — X-1 "is a design" 변형. 정규식 `의도된\s*(설계|단순화|간소화|복잡화|구조)`.
- **X-13** "X의 본질입니다 / 본질적으로" — D-3 변형. 정규식 `의 본질(이다|입니다)` 추가.

### Added — ch03 사례

- `examples/spring-ai-book/playbook-ch03.md` 신설
  - 변경 단락 38개 / 변경률 15~18% / 등급 A-
  - 대표 사례 5건 (X-6+X-8·R-7·P-1·Q-1·X-1+R-7)
  - 신규 패턴 X-11·X-12·X-13 발견

### Fixed
- ch02 점검 후 추가된 X 카테고리(v0.2.0)가 ch03에서 효과 검증: X-1·X-5·X-6·X-7·X-8·X-10·R-7·Q-1·P-1·V-6 모두 자동 탐지 성공
- ch03 ~다 잔류 0건 (I-4 카테고리로 25+건 일괄 처리)

## [0.2.0] — 2026-05-27

### Added — Spring AI 책 ch02 점검 결과 누적

- **X 카테고리 신설** (영어 구문 직역) 10개 ID
  - X-1: "묶는 것은 의도한 설계입니다" (is a design / by design)
  - X-2: "두 가지 이유는 ~ 입니다" 매 절 도입부 (미국 IT 책 "There are two reasons" 직역)
  - X-3: "일관 사용 / 일관 유지" (consistently uses)
  - X-4: "본문에서 흐름을 빠르게 잡고 싶다면" (for quick understanding)
  - X-5: "한 번 풀어쓰고 가는 편이 안전합니다" (for safety / once you ~)
  - X-6: 강조성 숫자 "한 줄도 / 한 줄이 / 두 줄이" (not a single line / this one line is key) — 가장 강한 신호 (ch02 10+회)
  - X-7: "어떻게 X 어떻게 Y / 어디인지 알면 어디에 ~" 반복 의문 구조
  - X-8: 무생물 주어 + 단정 동사 "X가 통제합니다 / 차단합니다 / 전환됩니다"
  - X-9: "활성화되도록 통제합니다" (피동 + 통제 동사 결합, A-9 잔류 보강)
  - X-10: "한 번 ~해 두면" (once you've grasped, P-5 잔류 보강)

- **R 카테고리 확장**
  - R-4: 정규식 강화 (`정렬(됩니다|된\s*채|되어|한다|합니다)` — ch02 6건 검출)
  - R-7 신규: "이 한 줄이 통제합니다 / 원천 차단합니다" (controls / blocks 직역, 무생물 주어 + 단정 동사)

- **Y 카테고리 신설** (기존 정규식 강화)
  - A-15, A-9, A-10, H-3, I-3, R-4, S-4 정규식 보강안 명시

- **examples/spring-ai-book/playbook-ch02.md 신설**
  - ch02 점검 통계 (134개 단락 / 17,242자 / 잔류 약 50건)
  - 대표 사례 8건 Before/After (X-1·X-2·X-3·X-5·X-6·X-7·R-4·R-7)

### Fixed
- ch02 본문 line 117·163·1037 등 R-4(정렬) 잔류가 1차 윤문에서 미검출되던 문제 식별 (v0.3.0에서 detection 강화 예정)
- 사용자 자바책 reference 4편(1·5·6·11장) 기반 톤 매치 검증 통과

## [0.1.0] — 2026-05-27

### 초기 릴리스

- **base**: [im-not-ai (humanize-korean) v2.0](https://github.com/epoko77-ai/im-not-ai) MIT 라이선스 fork
- **유지**: A~J 카테고리 (번역투·영어 과다·기계 패턴·AI 관용구 등), 4대 철칙, Fast/Strict 모드, 11개 agent, metrics.py·metrics_v2.py
- **보강**: 한국 IT 책 특화 카테고리 P~W 추가
  - **P** (학습 목표 마무리): 영어식 "이 N 가지가 완성되면 ~ 동작한다" 패턴 5개
  - **Q** (객체에 책임 부여): "is responsible for" 직역 4개 (단 사람·부서 책임은 보존)
  - **R** (영어 IT 동사 직역): "is pulled in", "swap out", "is dropped" 등 6개
  - **S** (자기 마케팅): ★ 표시·차별화·시중의 다른 5개 (한국·일본 책 안 씀)
  - **T** (당연한 사실 강조): "한국어 존댓말의 ~", "한 줄의 응답" 등 5개
  - **U** (도메인 용어): 사업소→사업자, 격식 회신→공문 형식, 갈래→방법 등 6개
  - **V** (책 마무리 멘트): "다음 페이지에서 만난다", "함께 시작" 등 6개
  - **W** (공저 노트): 작업 이력을 본문 옆에 안 적기
- **새 슬래시 명령**: `/humanize-book`, `/humanize-book-redo`
- **새 reference 파일**:
  - `book-extra-rules.md` — P~W 카테고리
  - `user-style-traits.md` — 한국 IT 책 톤 8가지 특징
- **도메인 분리 구조**: `examples/{domain}/` 폴더로 책마다 다른 도메인 용어집·페르소나 분리
- **첫 도메인 사례**: `examples/spring-ai-book/` — 공공 SI · eGovFrame · Spring AI 책

### 알려진 한계

- ~다체 자동 변환은 90% 처리, 10% 잔류 (인용문·코드 주석 보호로 인한 제한)
- examples/ 도메인이 1개 (spring-ai-book)만 있음. 더 많은 도메인 사례는 PR로 환영
- metrics.py에 P~W 카테고리 정량 측정 함수 미추가 (다음 버전에서 보강 예정)
