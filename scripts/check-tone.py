#!/usr/bin/env python3
"""
check_korean_tone.py — 본 책의 한국식 톤 자동 점검기

영어식 직역체, LLM 정리체, 자기 마케팅, 한국 사람이 잘 안 쓰는 비유 등
사용자 자바책 톤과 어긋나는 표현을 모두 grep 정규식으로 검사한다.

사용법:
    python3 scripts/check_korean_tone.py                                  # manuscript/ 전체
    python3 scripts/check_korean_tone.py manuscript/part0-intro/          # 폴더
    python3 scripts/check_korean_tone.py path/to/file.md                  # 단일 파일

종료 코드:
    0: 위반 0건 (통과)
    1: 위반 1건 이상
    2: 사용법 오류

표준 라이브러리만 사용.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Rule:
    """톤 위반 패턴 하나."""
    category: str          # 카테고리 라벨 (A·B·... / strong / verb-ending 등)
    pattern: re.Pattern    # 검사 정규식
    message: str           # 사용자에게 보여줄 메시지 (한국식 대안 등)
    severity: str = "FAIL" # FAIL 또는 WARN


# ---------------- 카테고리별 패턴 ----------------

RULES: list[Rule] = [
    # ============ 강한 금지 (호칭·메타·정체성) ============
    Rule("strong-honorific", re.compile(r"본 서적|본 책의|본 책이|본 책은|본 책을"),
         "→ '이 책' 사용. '본 서적' / '본 책' 모두 금지."),
    Rule("strong-honorific", re.compile(r"본 챕터|본 장"),
         "→ '이 장' / '이 챕터' 사용. '본 챕터' / '본 장' 금지."),
    Rule("strong-honorific", re.compile(r"본 부록|본 절"),
         "→ '이 부록' / '이 절' 사용."),
    Rule("strong-honorific", re.compile(r"본 ~의|본 사실|본 도식|본 시퀀스|본 다이어그램"),
         "→ '본 ~' 패턴 금지. 동사로 풀어쓰기."),
    Rule("strong-meta", re.compile(r"한 줄 결론|한 줄로 줄이면|한 줄로 답"),
         "→ 메타 표현 제거. 사실로 진술."),
    Rule("strong-meta", re.compile(r"다른 말로 표현하면|한 문장으로 정리하면|한 마디로 말하면"),
         "→ 모두 제거. '즉' / '다시 말해' 또는 그냥 빼기."),
    Rule("strong-meta", re.compile(r"이 사실이 본"),
         "→ '이 사실' 메타 표현 제거."),
    Rule("strong-identity", re.compile(r"정체성이다|정체성입니다|의 정체성"),
         "→ '~의 정체성' 표현 금지. 사실로 진술."),
    Rule("strong-identity", re.compile(r"약속하는|이 책의 약속"),
         "→ '약속' 표현 금지. 동사로 풀어쓰기."),

    # ============ 자기 마케팅 (한국·일본 책 안 씀) ============
    Rule("self-marketing", re.compile(r"★"),
         "→ ★ 표시는 미국 IT 책 패턴. 모두 제거."),
    Rule("self-marketing", re.compile(r"차별화 장|차별화 1순위|차별화 가치|핵심 차별화"),
         "→ '차별화' 표현 제거. 한국·일본 책은 자기 평가 안 함."),
    Rule("self-marketing", re.compile(r"시중의 다른|시중에 다른|시중에 ~ 서적"),
         "→ 자기 마케팅. 책 표지·서평은 출판사 영역. 본문에서 안 함."),
    Rule("self-marketing", re.compile(r"가장 크게 다른|가장 큰 차별"),
         "→ 본문 안 자기 마케팅 금지."),
    Rule("self-marketing", re.compile(r"이 책의 가장 큰\s*\w+\s*(가치|장점|차별화)"),
         "→ 자기 평가 제거."),

    # ============ 종결어미: ~다체 ============
    Rule("verb-ending", re.compile(r"(한다\.|이다\.|된다\.|있다\.|없다\.|않다\.|온다\.|간다\.|아니다\.|아닐 것이다\.|것이다\.)(?!\s*[가-힣])"),
         "→ ~습니다체로 통일. '한다.' → '합니다.', '이다.' → '입니다.'",
         "FAIL"),

    # ============ A. 강조성 숫자·도구 비유 ============
    Rule("A-emphasis-metaphor", re.compile(r"화이트보드 한 장|한 페이지로|한 줄로 정리|한 자리에 모|손에 잡힐"),
         "→ 강조 비유 제거. 단순 사실로."),
    Rule("A-emphasis-metaphor", re.compile(r"30분 안에 머릿|30분의 추가 시간|N시간의 학습을 안정"),
         "→ 강조성 시간 거래 표현 제거."),

    # ============ B. 동작 비유 (개념의 사물화) ============
    Rule("B-action-metaphor", re.compile(r"머릿속에 잡|머릿속에 박|머릿속에 정리되어 있|머릿속에 떠올"),
         "→ '안다 / 이해한다 / 압니다'로 단순화."),
    Rule("B-action-metaphor", re.compile(r"매끄럽게 흐른|매끄럽게 흘러|매끄럽게 이어"),
         "→ '쉽게 공부할 수 있다 / 쉽게 이어진다'로."),
    Rule("B-action-metaphor", re.compile(r"손에 쥐는|손에 쥐고"),
         "→ '안다 / 배운다 / 만든 결과물'으로."),
    Rule("B-action-metaphor", re.compile(r"손을 코드 위에 올|손으로 만진|손으로 확인"),
         "→ '코드를 작성한다 / 다룬다 / 확인한다'로."),
    Rule("B-action-metaphor", re.compile(r"RFP가 떨어집니다|RFP가 떨어진다"),
         "→ 'RFP가 들어옵니다 / 도착합니다'로."),

    # ============ C. 화자·태도 강조 ============
    Rule("C-speaker-emphasis", re.compile(r"본인 입으로|본인의 입으로"),
         "→ '본인 입으로' 제거. 그냥 '안다 / 설명한다'."),

    # ============ D. 가치·평가 비유 ============
    Rule("D-value-metaphor", re.compile(r"유일한 자연스러운|유일한 적합한"),
         "→ '가장 적합한'으로."),
    Rule("D-value-metaphor", re.compile(r"결정적인|결정적으로 다"),
         "→ '중요한 / 크게 다'로."),
    Rule("D-value-metaphor", re.compile(r"정공법이다|정공법입니다"),
         "→ '기본 방법입니다'로."),

    # ============ E. 메타·요약체 ============
    Rule("E-meta-summary", re.compile(r"결론을 먼저 정리하면|결론부터 말하면"),
         "→ 메타 표현 제거."),
    Rule("E-meta-summary", re.compile(r"이 사실이.*본질|이 사실이.*핵심"),
         "→ '이 사실' 메타 표현 제거."),

    # ============ F. 시간 강조·시간 거래 ============
    Rule("F-time-trade", re.compile(r"\d+분의 추가 시간이.*\d+시간|\d+분이.*\d+시간"),
         "→ 시간 거래 비유 제거."),

    # ============ G. 추상 영어 명사 ============
    Rule("G-abstract-noun", re.compile(r"통제 표면|통신 표면|표면이 좁"),
         "→ '통제 범위 / 통신 부분 / 다루는 부분'으로."),
    Rule("G-abstract-noun", re.compile(r"골격을 잡|골격이 잡|이해의 골격"),
         "→ '구조를 잡 / 큰 구조'로."),

    # ============ H. 격려·권유체 과잉 ============
    Rule("H-encouragement", re.compile(r"시간을 들여 정확하게 읽기를 권"),
         "→ '차근차근 읽으면 좋습니다' 또는 제거."),
    Rule("H-encouragement", re.compile(r"한 번 더 읽기를 권"),
         "→ 강의 톤 과잉. 빼거나 단순화."),
    Rule("H-encouragement", re.compile(r"한 번의 투자|투자 가치가"),
         "→ '투자' 비유 제거."),

    # ============ I. 환영·결의 멘트 ============
    Rule("I-greeting", re.compile(r"함께 시작합시다|함께 시작해|함께 출발"),
         "→ 환영 멘트 제거. 한국 책 안 씀."),
    Rule("I-greeting", re.compile(r"다음 페이지에서 만난다|다음 페이지에서 만나|다음 페이지에서 보자|다음 페이지에서 봅시다"),
         "→ '본문이 시작됩니다' 같은 멘트도 제거. 그냥 본문으로."),
    Rule("I-greeting", re.compile(r"다음 챕터에서 만난다|다음 챕터에서 보자|다음 장에서 만난다"),
         "→ 환영 멘트 제거."),
    Rule("I-greeting", re.compile(r"다음 페이지부터 본문이 시작"),
         "→ 이 멘트 자체를 제거. 한국 책 안 씀."),

    # ============ J. 사물·개념의 영어식 가치 비유 ============
    Rule("J-value-metaphor", re.compile(r"책의 수명을|수명을 ~ 확보|수명을 \d+년"),
         "→ 책에 '수명' 표현 안 씀. '이어서 활용할 수 있도록 준비한다'로."),
    Rule("J-value-metaphor", re.compile(r"운영 현실을 정리"),
         "→ '운영 현장에서 필요한 사항을 정리'로."),
    Rule("J-value-metaphor", re.compile(r"디딤돌"),
         "→ '디딤돌' 비유 제거."),
    Rule("J-value-metaphor", re.compile(r"단단함이.*단단함|단단함의"),
         "→ '안정성'으로 풀어쓰기."),

    # ============ K. 한국 행정·SI 도메인 부적합 영어식 ============
    Rule("K-domain-term", re.compile(r"격식 회신|격식 답변|공문 격식체|격식체 회신문"),
         "→ '공문 형식의 답변 초안' 또는 '행정 답변 초안'으로."),
    Rule("K-domain-term", re.compile(r"양면 RAG|양면 챗봇|양면 답변|시민·민원관 양면"),
         "→ '두 가지 응답' 또는 풀어 쓰기."),
    Rule("K-domain-term", re.compile(r"갈래"),
         "→ '갈래' 단어 한국에서 거의 안 씀. '방법 / 선택지'로."),

    # ============ L. 자기 평가·차별화 강조 (위 self-marketing과 중복 일부) ============
    # (★, 차별화는 위에서 처리)

    # ============ M. 본문 자기 마케팅 (위 self-marketing과 중복) ============

    # ============ N. 모호한 한국 행정·SI 용어 ============
    Rule("N-vague-term", re.compile(r"시민 정보(?!보)|시민정보(?!보)"),
         "→ '민원인의 개인정보' 또는 '시민의 개인정보'로 구체화."),

    # ============ Q. 객체·시스템에 "책임" 부여 (영어 직역) ============
    # 사람/부서/팀이 책임지는 경우는 자연스러우므로 보존. 객체·코드·모듈에 책임 부여만 검출.
    Rule("Q-object-responsibility",
         re.compile(r"무엇을 책임지|책임지는지|책임에 맞게|클래스의 책임|모듈의 책임|빈의 책임|객체의 책임|이 (장|챕터)의 책임|흐름을 책임|시그니처를 책임"),
         "→ '역할' / '담당' / '하는 일' / '다룹니다'로. 객체에 '책임'은 영어 직역."),

    # ============ 외래어 직역 ============
    Rule("foreign-direct", re.compile(r"의 자리|한 자리에서|한 자리|자리에 떨어|자리이다|자리입니다|자리에 있는|자리 잡|자리 잡고"),
         "→ '자리' 비유 명사 제거. 동사로 풀어쓰기.", "WARN"),
    Rule("foreign-direct", re.compile(r"의 흐름이|의 흐름은|두 흐름|세 흐름|흐름의 교차"),
         "→ '흐름' 비유 제거. '두 가지 / 두 줄기'.", "WARN"),
    Rule("foreign-direct", re.compile(r"의 토대|토대 위에|토대로 한"),
         "→ '토대' 영어 'foundation' 직역. '기반 / 위에서'로.", "WARN"),
    Rule("foreign-direct", re.compile(r"의 교차점|교차점에"),
         "→ '교차점' 영어 'intersection' 직역. 다른 표현으로."),

    # ============ em-dash (도식 자리표시자 제외) ============
    Rule("em-dash-body",
         re.compile(r"^(?!>.*\(제작 필요)(?!>.*\(실 캡쳐 필요).*—",
                    re.MULTILINE),
         "→ 본문 em-dash(—) 제거. 한국어 쉼표·괄호·콜론으로.",
         "WARN"),
]


# ---------------- 점검 로직 ----------------

@dataclass
class Finding:
    file: str
    line: int
    category: str
    severity: str
    matched: str
    message: str

    def format(self) -> str:
        return (
            f"{self.severity}  {self.file}:{self.line}  "
            f"[{self.category}]  \"{self.matched}\"  {self.message}"
        )


def check_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return findings

    # 코드 블록 (``` ... ```) 안의 줄은 점검하지 않는다
    # — 영어 코드·주석에 한국식 톤 규칙을 강제하면 안 되므로.
    in_code = False
    lines = text.splitlines()
    code_mask = [False] * len(lines)
    for i, ln in enumerate(lines):
        if re.match(r"^```", ln.strip()):
            in_code = not in_code
            code_mask[i] = True  # 펜스 줄 자체도 점검 제외
            continue
        code_mask[i] = in_code

    for rule in RULES:
        for m in rule.pattern.finditer(text):
            start = m.start()
            line_num = text.count("\n", 0, start) + 1
            # 코드 블록 안이면 건너뜀
            if 0 <= line_num - 1 < len(code_mask) and code_mask[line_num - 1]:
                continue
            matched = m.group(0)[:50]
            # 같은 줄에 같은 카테고리의 같은 패턴이 여러 번이면 한 번만 보고
            findings.append(Finding(
                file=str(path),
                line=line_num,
                category=rule.category,
                severity=rule.severity,
                matched=matched,
                message=rule.message,
            ))
    return findings


def collect_md_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix == ".md" else []
    if target.is_dir():
        out: list[Path] = []
        for p in sorted(target.rglob("*.md")):
            # 검사 제외: conventions·assets·resources (집필 가이드, 작업 메모)
            rel = p.relative_to(target) if target.is_absolute() else p
            parts = set(rel.parts)
            if {"conventions", "assets", "resources"} & parts:
                continue
            out.append(p)
        return out
    return []


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        target = Path(__file__).resolve().parent.parent / "manuscript"
    else:
        target = Path(argv[1]).resolve()

    if not target.exists():
        print(f"path not found: {target}", file=sys.stderr)
        return 2

    files = collect_md_files(target)
    if not files:
        print(f"no .md files under: {target}", file=sys.stderr)
        return 2

    all_findings: list[Finding] = []
    for f in files:
        all_findings.extend(check_file(f))

    # 카테고리별 그룹화 출력
    fail_count = sum(1 for f in all_findings if f.severity == "FAIL")
    warn_count = sum(1 for f in all_findings if f.severity == "WARN")

    # 파일별 + 줄 번호 순으로 정렬
    all_findings.sort(key=lambda x: (x.file, x.line, x.category))

    for f in all_findings:
        print(f.format())

    print()
    print(f"검사 파일 {len(files)}개 / FAIL {fail_count} / WARN {warn_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
