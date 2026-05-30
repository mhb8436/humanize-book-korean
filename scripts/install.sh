#!/usr/bin/env bash
# humanize-book-korean install script (macOS / Linux)
#
# 사용법:
#   ./scripts/install.sh <대상 책 프로젝트 경로> [--link|--copy]   # 특정 프로젝트에 설치
#   ./scripts/install.sh --global              [--link|--copy]   # ~/.claude 글로벌 설치
#
# 모드:
#   --link  심볼릭 링크 (기본). 본 저장소 변경이 설치 대상에 즉시 반영. (개발용 권장)
#   --copy  사본 복사. 저장소와 무관하게 독립 동작. (배포·백업용)
#
# 윈도우(네이티브) 사용자는 scripts/install.ps1 (PowerShell)을 쓰세요.
# 도메인 자산(examples/)은 스킬 폴더 안에 포함되어 함께 설치됩니다 — 별도 처리 불필요.

set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
    cat <<'EOF'
사용법:
  install.sh <대상 책 프로젝트 경로> [--link|--copy]   # 프로젝트 설치
  install.sh --global              [--link|--copy]   # ~/.claude 글로벌 설치

모드: --link(기본, 심볼릭 링크) | --copy(사본 복사)
윈도우(네이티브): scripts/install.ps1 사용
EOF
}

# --- 인자 파싱 ---
if [ $# -eq 0 ] || [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    usage
    exit 0
fi

if [ "$1" = "--global" ]; then
    SCOPE="global"
    TARGET="$HOME"
    MODE="${2:---link}"
else
    SCOPE="project"
    TARGET="$1"
    MODE="${2:---link}"
    if [ ! -d "$TARGET" ]; then
        echo "오류: 대상 디렉토리가 없습니다: $TARGET" >&2
        exit 1
    fi
fi

if [ "$MODE" != "--link" ] && [ "$MODE" != "--copy" ]; then
    echo "오류: 알 수 없는 모드 '$MODE' (--link 또는 --copy)" >&2
    exit 1
fi

CLAUDE_DIR="$TARGET/.claude"
echo "설치: $SKILL_ROOT → $CLAUDE_DIR  ($SCOPE, $MODE)"

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/commands" "$CLAUDE_DIR/agents"

# 심볼릭 링크 또는 사본 복사 (공통 처리)
link_or_copy() {
    local src="$1" dest="$2"
    if [ "$MODE" = "--copy" ]; then
        rm -rf "$dest"
        cp -R "$src" "$dest"
    else
        ln -sfn "$src" "$dest"
    fi
}

# 스킬 폴더 — examples/ 가 이 안에 포함되어 함께 따라옵니다.
link_or_copy "$SKILL_ROOT/.claude/skills/humanize-book-korean" \
             "$CLAUDE_DIR/skills/humanize-book-korean"

for cmd in "$SKILL_ROOT"/.claude/commands/*.md; do
    link_or_copy "$cmd" "$CLAUDE_DIR/commands/$(basename "$cmd")"
done

for agent in "$SKILL_ROOT"/.claude/agents/*.md; do
    link_or_copy "$agent" "$CLAUDE_DIR/agents/$(basename "$agent")"
done

echo "완료 ($MODE)."
if [ "$MODE" = "--link" ]; then
    echo "  심볼릭 링크 — 저장소 변경이 즉시 반영됩니다."
fi
echo "  도메인 자산(examples/)은 스킬 폴더에 포함되어 함께 설치되었습니다."
echo
echo "다음 단계:"
if [ "$SCOPE" = "global" ]; then
    echo "  - 아무 책 프로젝트에서 'claude' 실행 후  /humanize-book {파일경로}"
    echo "  - 공공 SI 책이면                        /humanize-book {파일경로} --domain spring-ai-book"
else
    echo "  - 대상 프로젝트에서 'claude' 실행 후     /humanize-book {파일경로}"
fi
echo "  - 새 도메인은  .claude/skills/humanize-book-korean/examples/{도메인}/  에 추가"
