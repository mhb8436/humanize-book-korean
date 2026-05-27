# Changelog

본 스킬의 모든 변경 사항을 기록합니다. [Keep a Changelog](https://keepachangelog.com/) 형식을 따릅니다.

## [Unreleased]

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
