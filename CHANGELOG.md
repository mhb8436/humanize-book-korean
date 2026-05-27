# Changelog

본 스킬의 모든 변경 사항을 기록합니다. [Keep a Changelog](https://keepachangelog.com/) 형식을 따릅니다.

## [Unreleased]

### Planned
- v0.4.0: `metrics_v2.py`에 신규 측정 함수 3개 (`count_emphatic_numerals`, `count_align_verbs`, `count_abstract_subj_with_control_verb`) + `baseline_v2.json` 보정값

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
