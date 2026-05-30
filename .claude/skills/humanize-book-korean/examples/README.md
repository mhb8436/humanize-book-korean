# Examples — 도메인별 자산

본 폴더는 책마다 다른 **도메인 용어·페르소나·표준 톤 reference**를 분리해서 관리합니다.

## 현재 등록된 도메인

| 도메인 | 책 | 도메인 영역 |
|------|------|------|
| `spring-ai-book/` | 공공 SI 개발자를 위한 Spring AI | 공공 SI, eGovFrame, 행정 자동화 |

새 책 작업 시 본인 도메인을 추가하세요.

## 새 도메인 추가 방법

```bash
# 도메인 자산은 스킬 폴더 안 examples/ 에 둡니다 (저장소 루트 기준 경로).
mkdir -p .claude/skills/humanize-book-korean/examples/{your-book}/reference-style
cd .claude/skills/humanize-book-korean/examples/{your-book}
```

다음 파일을 작성합니다:

### 1. `domain-glossary.md` (필수)

도메인 표준 용어와 흔히 잘못 쓰는 표현 매핑.

```markdown
# {your-book} 도메인 용어집

## 1. 사업·계약 용어

| 잘못 쓴 표현 | 표준 | 의미 |
|------|------|------|
| ... | ... | ... |
```

### 2. `persona.md` (필수)

책의 가상 인물·페르소나 보존 규칙.

```markdown
# 페르소나 — {your-book}

## {페르소나 이름}

- 소속:
- 직급:
- 경력:
- ...

## 페르소나 보존 규칙

humanize 윤문 시 다음을 절대 변경하지 않습니다:
- 이름
- 소속
- 경력
```

### 3. `reference-style/` (선택)

한국 IT 책의 표준 톤을 보여 주는 reference. 보통 사용자가 직접 쓴 다른 책의 핵심 단락을 발췌합니다.

### 4. `book-tone-history.md` (선택)

본 책 작업 중 발견된 패턴을 누적 기록. 다음 작업이 이어가는 단일 진실 공급원.

## 사용 방법

설치된 책 프로젝트에서:

```bash
/humanize-book manuscript/ch01.md --domain {your-book}
```

`--domain {your-book}`이 지정되면 본 도메인 폴더의 모든 자산이 자동 로드됩니다.

## 도메인 자산이 윤문에 미치는 영향

1. **domain-glossary.md**: 표준 용어는 윤문 대상에서 제외 (다른 표현으로 변경 금지)
2. **persona.md**: 페르소나 정보는 100% 보존
3. **reference-style/**: 윤문된 단락의 톤이 이 reference와 매치되도록 검증
4. **book-tone-history.md**: 본 책 작업 중 누적된 패턴을 다음 작업에 적용

## 도메인 분리 원칙

- **공통 규칙**: A~W 카테고리는 모든 한국 IT 책에 공통. `references/`에 있음.
- **도메인 특화**: 사업자/발주처 같은 도메인 용어는 `examples/{domain}/`에. 다른 도메인 책에는 안 맞음.

이 분리 덕분에 본 스킬이 한국 IT 책 전반에 재사용 가능합니다.

## 기여 환영

본 저장소에 새 도메인 사례를 PR로 보내 주시면 다른 한국 IT 책 저자들도 활용할 수 있습니다.

- 데이터 엔지니어링 책
- DevOps · SRE 책
- 머신러닝 · 딥러닝 책
- 보안 책
- 모바일 앱 개발 책
- 클라우드 책 (AWS·Azure·GCP)

도메인 폴더에는 일반적으로 다음을 포함합니다:
- `domain-glossary.md` (표준 용어)
- `persona.md` (페르소나)
- `reference-style/` (선택)
- `book-tone-history.md` (선택)
