import subprocess
import openai
import os
from pathlib import Path
import sys
import json
import textwrap
import argparse

# -----------------------------
# CONFIGURATION
# -----------------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("ERROR: OPENAI_API_KEY not found in environment.")
    sys.exit(1)

DOCS_DIR = Path(__file__).parent.parent

COL_WIDTHS = {
    "before": 20,
    "after": 25,
    "vale": 60
}

# -----------------------------
# VALE
# -----------------------------
def run_vale(file_path):
    """Run Vale with JSON output."""
    result = subprocess.run(
        ["vale", "--output=JSON", str(file_path)],
        capture_output=True,
        text=True
    )
    if result.returncode not in (0, 1):  # 1 = issues found
        print(result.stderr)
        return {}
    return json.loads(result.stdout or "{}")

# -----------------------------
# AI
# -----------------------------
def ask_ai_for_suggestion(snippet, vale_message):
    prompt = f"""
You are a technical writing assistant. Follow the Microsoft Style Guide.

Flagged text:
\"\"\"{snippet}\"\"\"

Vale feedback:
\"\"\"{vale_message}\"\"\"

Rewrite the text to resolve the issue.
Return ONLY the rewritten Markdown text.
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# -----------------------------
# TABLE
# -----------------------------
def format_table(before, after, vale_comment):
    before_lines = textwrap.wrap(before, COL_WIDTHS["before"]) or [""]
    after_lines = textwrap.wrap(after, COL_WIDTHS["after"]) or [""]
    vale_lines = textwrap.wrap(vale_comment, COL_WIDTHS["vale"]) or [""]

    max_lines = max(len(before_lines), len(after_lines), len(vale_lines))
    before_lines += [""] * (max_lines - len(before_lines))
    after_lines += [""] * (max_lines - len(after_lines))
    vale_lines += [""] * (max_lines - len(vale_lines))

    sep = f"+{'-'*COL_WIDTHS['before']}+{'-'*COL_WIDTHS['after']}+{'-'*COL_WIDTHS['vale']}+"
    lines = [
        sep,
        f"| {'Before AI':<{COL_WIDTHS['before']}} | {'After AI':<{COL_WIDTHS['after']}} | {'Vale Comment':<{COL_WIDTHS['vale']}} |",
        sep.replace("-", "=")
    ]

    for b, a, v in zip(before_lines, after_lines, vale_lines):
        lines.append(
            f"| {b:<{COL_WIDTHS['before']}} | {a:<{COL_WIDTHS['after']}} | {v:<{COL_WIDTHS['vale']}} |"
        )

    lines.append(sep)
    return "\n".join(lines)

# -----------------------------
# APPLY CHANGE
# -----------------------------
def human_approval_and_apply(
    file_path,
    line_number,
    original_line,
    ai_suggestion,
    vale_comment,
    dry_run=False
):
    table = format_table(original_line.strip(), ai_suggestion, vale_comment)
    print("\n" + table)

    apply = input("Apply this change? (y/n): ").strip().lower()
    if apply != "y":
        print("Skipped.\n")
        return False

    if dry_run:
        print(
            f"🧪 Dry run — no changes written\n"
            f"   File: {file_path}\n"
            f"   Line {line_number}:\n"
            f"   BEFORE: {original_line}\n"
            f"   AFTER:  {ai_suggestion}\n"
        )
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    index = line_number - 1
    lines[index] = ai_suggestion + "\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(
        f"✅ Edits written to disk.\n"
        f"   File: {file_path}\n"
        f"   Line {line_number}:\n"
        f"   BEFORE: {original_line}\n"
        f"   AFTER:  {ai_suggestion}\n"
    )

    return True

# -----------------------------
# MAIN WORKFLOW
# -----------------------------
def process_docs(target_path=None, dry_run=False):
    if target_path:
        target = Path(target_path)
        if target.is_file() and target.suffix == ".md":
            md_files = [target]
        elif target.is_dir():
            md_files = list(target.rglob("*.md"))
        else:
            print("Invalid path.")
            return
    else:
        md_files = list(DOCS_DIR.rglob("*.md"))

    print(f"Found {len(md_files)} Markdown file(s).")

    changes_applied = False

    for md_file in md_files:
        print(f"\n📄 Processing {md_file}")
        vale_results = run_vale(md_file)
        issues = vale_results.get(str(md_file), [])

        if not issues:
            print("No issues flagged by Vale.")
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for issue in issues:
            line_number = issue["Line"]
            vale_message = issue["Message"]
            original_line = lines[line_number - 1].rstrip("\n")

            ai_suggestion = ask_ai_for_suggestion(
                original_line.strip(),
                vale_message
            )

            applied = human_approval_and_apply(
                md_file,
                line_number,
                original_line,
                ai_suggestion,
                vale_message,
                dry_run
            )

            if applied:
                changes_applied = True

    # -----------------------------
    # POST-RUN GUIDANCE
    # -----------------------------
    if changes_applied and not dry_run:
        print("\nNext step: verify style alignment by re-running Vale.")
        if target_path:
            print(f"  vale {target_path}")
        else:
            print(f"  vale {DOCS_DIR}")
    elif dry_run:
        print("\nDry run complete. No files were modified.")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI + Vale documentation workflow")
    parser.add_argument("--file", help="Path to a specific Markdown file")
    parser.add_argument("--folder", help="Path to a folder containing Markdown files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes but do not modify files"
    )

    args = parser.parse_args()
    target = args.file or args.folder

    process_docs(target, dry_run=args.dry_run)