#!/usr/bin/env bash
# humanize-book-korean install script
#
# 사용법:
#   ./scripts/install.sh /path/to/your-book-project [--link|--copy]
#
# 옵션:
#   --link  심볼릭 링크 (기본). 본 저장소 변경이 책 프로젝트에 즉시 반영.
#   --copy  사본 복사. 본 저장소와 무관하게 책 프로젝트에서 동작.

set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"
MODE="${2:---link}"

if [ -z "$TARGET" ]; then
    echo "사용법: $0 <대상 책 프로젝트 경로> [--link|--copy]"
    echo "예: $0 ~/Workspaces/my-book --link"
    exit 1
fi

if [ ! -d "$TARGET" ]; then
    echo "오류: 대상 디렉토리가 없습니다: $TARGET"
    exit 1
fi

echo "설치: $SKILL_ROOT → $TARGET ($MODE)"

mkdir -p "$TARGET/.claude/skills" "$TARGET/.claude/commands" "$TARGET/.claude/agents"

if [ "$MODE" = "--link" ]; then
    # 심볼릭 링크
    ln -sf "$SKILL_ROOT/.claude/skills/humanize-book-korean" \
           "$TARGET/.claude/skills/humanize-book-korean"

    for cmd in "$SKILL_ROOT"/.claude/commands/*.md; do
        ln -sf "$cmd" "$TARGET/.claude/commands/$(basename "$cmd")"
    done

    for agent in "$SKILL_ROOT"/.claude/agents/*.md; do
        ln -sf "$agent" "$TARGET/.claude/agents/$(basename "$agent")"
    done

    echo "심볼릭 링크 완료. 본 저장소 변경이 대상 프로젝트에 즉시 반영됩니다."
else
    # 사본 복사
    cp -r "$SKILL_ROOT/.claude/skills/humanize-book-korean" "$TARGET/.claude/skills/"
    cp "$SKILL_ROOT"/.claude/commands/*.md "$TARGET/.claude/commands/"
    cp "$SKILL_ROOT"/.claude/agents/*.md "$TARGET/.claude/agents/"
    echo "사본 복사 완료."
fi

echo
echo "다음 단계:"
echo "  1. 대상 프로젝트의 examples/{your-book}/ 폴더 신설 (또는 기존 사용)"
echo "  2. examples/{your-book}/domain-glossary.md 작성 (도메인 표준 용어)"
echo "  3. examples/{your-book}/persona.md 작성 (페르소나 보존 규칙)"
echo "  4. Claude Code 세션에서 /humanize-book {파일경로} 실행"
