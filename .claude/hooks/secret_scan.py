#!/usr/bin/env python3
"""コミットに機微情報が含まれていないかを、パターンで機械的に調べる。

使い方:
  secret_scan.py --hook            PreToolUse フック。stdin の JSON から Bash コマンドを読み、
                                   git commit / git push のときだけ調べる。見つかれば exit 2 で止める
  secret_scan.py --staged          ステージ済みの変更を調べる
  secret_scan.py --worktree        HEAD からの変更（ステージ済み・未ステージ・未追跡）を調べる
  secret_scan.py --range <A..B>    コミット範囲の変更を調べる

見つからなければ exit 0、見つかれば exit 1（--hook のときは 2）。
誤検知は .claude/secret-allowlist に正規表現を1行ずつ書いて除外する。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

# このファイル自身と、パターンを説明するスキルは、パターンの文字列を含むので調べない
SELF_PATHS = {".claude/hooks/secret_scan.py", ".claude/skills/secret-check/SKILL.md"}

# (種類, 正規表現)。値そのものを出力しないよう、報告では種類と場所だけを出す
PATTERNS = [
    ("Anthropic API キー", r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    ("OpenAI 形式の API キー", r"\bsk-(?:proj-)?[A-Za-z0-9]{20,}"),
    ("AWS アクセスキー", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("GitHub トークン", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}"),
    ("Slack トークン", r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"),
    ("Google API キー", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("秘密鍵", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("Bearer トークン", r"(?i)\bbearer\s+[A-Za-z0-9_\-\.=]{20,}"),
    ("パスワード・シークレットの代入", r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*[:=]\s*['\"]?[^\s'\"<>]{6,}"),
    ("メールアドレス", r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    ("電話番号", r"(?<!\d)0\d{1,4}-\d{1,4}-\d{4}(?!\d)"),
    ("受験者・認定の識別番号", r"(?i)(?:受験者\s*ID|受験番号|受験票番号|認定番号|candidate\s*id|registration\s*(?:id|number)|certification\s*(?:id|number)|credential\s*id)\s*[:：]?\s*[A-Za-z0-9\-]{4,}"),
    ("バウチャー・割引コード", r"(?i)(?:バウチャー|voucher|クーポン|coupon|割引コード|promo\s*code)\s*(?:コード|code)?\s*[:：]\s*[A-Za-z0-9\-]{4,}"),
]

# 例示用として許可するもの（既定）
DEFAULT_ALLOW = [
    r"noreply@anthropic\.com",
    r"@example\.(?:com|org|net)",
    r"@users\.noreply\.github\.com",
    r"[:=]\s*['\"]?<[^>]+>",  # password: <your-password> のようなプレースホルダ
]

# 中身に関わらず、コミットしてはいけないファイル名
BAD_FILES = [
    (r"(?:^|/)\.env(?:\.|$)", ".env ファイル"),
    (r"\.(?:pem|key|p12|pfx)$", "鍵・証明書ファイル"),
    (r"(?:^|/)(?:credentials|secrets?)\.(?:json|ya?ml|toml)$", "認証情報ファイル"),
    (r"(?:^|/)id_(?:rsa|ed25519|ecdsa)$", "SSH 鍵"),
    (r"(?i)(?:score.?report|スコアレポート|成績|合格証|certificate)[^/]*\.(?:pdf|png|jpe?g)$", "スコアレポート・認定証の画像や PDF"),
]


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def repo_root():
    return Path(git("rev-parse", "--show-toplevel").strip() or ".")


def load_allow(root):
    allow = list(DEFAULT_ALLOW)
    f = root / ".claude" / "secret-allowlist"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                allow.append(line)
    return [re.compile(a) for a in allow]


def parse_diff(diff):
    """unified diff から (ファイル, 行番号, 追加された行) を返す。"""
    path, lineno = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            p = line[4:]
            path = None if p == "/dev/null" else p[2:] if p.startswith("b/") else p
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            lineno = int(m.group(1)) if m else 0
        elif line.startswith("+") and not line.startswith("+++"):
            yield path, lineno, line[1:]
            lineno += 1
        elif not line.startswith("-"):
            lineno += 1


def collect(mode, rng=None):
    """調べる (ファイル, 行番号, 行) と、対象のファイル名の一覧を返す。"""
    if mode == "staged":
        diff = git("diff", "--cached", "-U0", "--no-color")
        names = git("diff", "--cached", "--name-only").split()
    elif mode == "range":
        diff = git("diff", "-U0", "--no-color", rng)
        names = git("diff", "--name-only", rng).split()
    else:  # worktree: ステージ済み・未ステージ・未追跡をまとめて見る（多めに拾う）
        has_head = subprocess.run(["git", "rev-parse", "--verify", "-q", "HEAD"], capture_output=True).returncode == 0
        base = ["HEAD"] if has_head else ["--cached"]
        diff = git("diff", "-U0", "--no-color", *base)
        names = git("diff", "--name-only", *base).split()
        for f in git("ls-files", "--others", "--exclude-standard").split():
            names.append(f)
            try:
                text = Path(f).read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            diff += f"\n+++ b/{f}\n@@ -0,0 +1 @@\n" + "".join("+" + l + "\n" for l in text.splitlines())
    return list(parse_diff(diff)), names


def scan(lines, names, allow):
    findings = []
    for name in names:
        for pat, kind in BAD_FILES:
            if re.search(pat, name):
                findings.append((name, 0, kind))
    for path, lineno, text in lines:
        if path is None or path in SELF_PATHS:
            continue
        for kind, pat in PATTERNS:
            for m in re.finditer(pat, text):
                window = text[max(0, m.start() - 20): m.end() + 20]
                if any(a.search(m.group(0)) or a.search(window) for a in allow):
                    continue
                findings.append((path, lineno, kind))
    return findings


def report(findings, out):
    print("機微情報の可能性があるものが見つかりました（値は表示しません）:", file=out)
    for path, lineno, kind in sorted(set(findings)):
        loc = f"{path}:{lineno}" if lineno else path
        print(f"  - {loc}  {kind}", file=out)
    print(
        "対処: 該当箇所を消すかプレースホルダ（<YOUR_API_KEY> など）に置き換える。"
        "誤検知なら .claude/secret-allowlist に除外の正規表現を足す。詳しくは /secret-check。",
        file=out,
    )


def main():
    args = sys.argv[1:]
    root = repo_root()
    allow = load_allow(root)

    if "--hook" in args:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError:
            return 0
        cmd = (data.get("tool_input") or {}).get("command", "")
        if not re.search(r"\bgit\b[^|;&]*\b(?:commit|push)\b", cmd):
            return 0
        if re.search(r"\bgit\b[^|;&]*\bpush\b", cmd) and not re.search(r"\bcommit\b", cmd):
            upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}").strip()
            base = upstream or ("origin/main" if git("rev-parse", "--verify", "-q", "origin/main").strip() else "")
            if not base:
                return 0
            lines, names = collect("range", f"{base}..HEAD")
        else:
            lines, names = collect("worktree")
        findings = scan(lines, names, allow)
        if findings:
            report(findings, sys.stderr)
            return 2
        return 0

    if "--range" in args:
        lines, names = collect("range", args[args.index("--range") + 1])
    elif "--staged" in args:
        lines, names = collect("staged")
    else:
        lines, names = collect("worktree")
    findings = scan(lines, names, allow)
    if findings:
        report(findings, sys.stdout)
        return 1
    print("機微情報のパターンは見つかりませんでした。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
