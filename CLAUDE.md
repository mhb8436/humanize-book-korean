# humanize-book-korean — Claude Code 사용자 가이드

본 저장소는 Claude Code 스킬입니다. 새 세션이 이 저장소를 참조할 때 본 파일을 먼저 읽고 작업하세요.

## 본 저장소가 다루는 것

한국 IT 책 원고(특히 AI 도구로 1차 작성된 한글 텍스트)를 자연스러운 한국 IT 책 톤으로 윤문하는 Claude Code 스킬입니다. im-not-ai(humanize-korean) v2.0 fork에 한국 IT 책 특화 카테고리 P~W를 보강했습니다.

## 본 저장소 자체에 작업할 때 (스킬 자체 개선)

본 저장소 자체를 손볼 때 (예: 새 패턴 추가, 새 도메인 등록, 메트릭 보강):

1. **새 패턴 추가**:
   - `references/book-extra-rules.md`에 카테고리 ID 추가 (P-6, Q-5 등)
   - Before/After 1줄씩
   - `CHANGELOG.md`에 항목 추가

2. **새 도메인 등록**:
   - `examples/{domain}/` 폴더 신설
   - `domain-glossary.md` 작성 (도메인 용어 표준)
   - `persona.md` 작성 (책 페르소나 보존 규칙)
   - `reference-style/` 폴더에 한국 IT 책 표준 톤 reference (선택)
   - `examples/README.md`에 새 도메인 등록

3. **메트릭 보강**:
   - `references/metrics.py` 또는 `metrics_v2.py`에 측정 함수 추가
   - `references/baseline.json`에 새 메트릭 셀 추가 (보정값과 함께)

4. **테스트**:
   - `tests/fixtures/`에 AI 글 샘플 → 한국 IT 책 톤 샘플 쌍 추가
   - 회귀 테스트로 새 패턴이 정상 작동하는지 검증

## 본 저장소를 다른 책 프로젝트에서 사용할 때

다른 책 프로젝트(예: `~/Workspaces/your-book`)에 본 스킬을 적용하려면:

```bash
# 옵션 1: 심볼릭 링크 (개발 중)
cd ~/Workspaces/your-book
mkdir -p .claude/skills .claude/commands .claude/agents
ln -s ~/Workspaces/humanize-book-korean/.claude/skills/humanize-book-korean \
      .claude/skills/humanize-book-korean
ln -s ~/Workspaces/humanize-book-korean/.claude/commands/humanize-book.md \
      .claude/commands/humanize-book.md
ln -s ~/Workspaces/humanize-book-korean/.claude/commands/humanize-book-redo.md \
      .claude/commands/humanize-book-redo.md
for agent in ~/Workspaces/humanize-book-korean/.claude/agents/*.md; do
    ln -s "$agent" .claude/agents/
done

# 옵션 2: 사본 복사 (배포)
~/Workspaces/humanize-book-korean/scripts/install.sh ~/Workspaces/your-book
```

본인 책 도메인이 `examples/`에 없으면 새 폴더(`examples/your-book/`)를 만들고 `domain-glossary.md`·`persona.md`를 작성하세요. 그 후 `/humanize-book --domain your-book` 으로 호출하면 본인 책 도메인 자산이 자동 로드됩니다.

## 본 저장소의 정신

- **base는 im-not-ai**: A~J 카테고리는 원본 유지. 한국어 윤문의 학술 기반(이근희·김정우·Toral 2019)이 모두 base에 들어 있음.
- **보강은 한국 IT 책 작업에서만**: P~W 카테고리는 본 저장소가 추가한 영역. 일반 한국어 윤문에는 없는 패턴들 (자기 마케팅·학습 목표 마무리·도메인 용어 부정확 등).
- **도메인 분리**: 책마다 다른 도메인 용어는 examples/{domain}/로. 본 저장소가 다른 책 작업에도 그대로 사용 가능.
- **개선 누적**: 새 영어식 패턴 발견 시 references/ 또는 examples/에 즉시 등록. 다른 사용자가 PR로 기여 가능.

## 권장 작업 흐름

본 스킬 자체를 손볼 때:

```
1. 패턴 발견 (책 작업 중 또는 사용자 PR)
   ↓
2. references/book-extra-rules.md 에 카테고리 추가
   ↓
3. tests/fixtures/ 에 회귀 케이스 추가 (선택)
   ↓
4. CHANGELOG.md 갱신
   ↓
5. git commit + push
```

본 스킬을 다른 책 작업에 적용할 때:

```
1. 본 저장소 클론 또는 심볼릭 링크
   ↓
2. 본인 도메인 examples/ 폴더 신설 (또는 기존 사용)
   ↓
3. /humanize-book {파일경로} 실행
   ↓
4. 결과 검토 + 잔류 패턴 발견 시 본 저장소에 PR
```

## 관련 자료

- 본 저장소 `README.md` — 외부 사용자 안내
- `CHANGELOG.md` — 버전 이력
- `references/scholarship.md` — 한국 번역학계 학술 기초
- `references/ai-tell-taxonomy.md` — A~J 카테고리 본진 분류 (590줄)
- `references/book-extra-rules.md` — P~W 카테고리 (본 저장소 추가)
- `examples/{domain}/` — 책별 도메인 용어·페르소나
