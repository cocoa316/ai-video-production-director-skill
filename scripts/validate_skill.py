#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


EXPECTED_NAME = "ai-video-production-director"
EXPECTED_VERSION = "1.4.1"
EXPECTED_UPSTREAM = "6.7.0"
REQUIRED_PATHS = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/project-director-method.md",
    "references/production-interaction-rules.md",
    "README.md",
    "references/project-state-policy.md",
    "references/host-capability-map.md",
    "references/installation-and-compatibility.md",
    "references/project-artifacts.md",
    "references/visual-storyboard-method.md",
    "references/storyboard-generation-contract.md",
    "references/directors-read.md",
    "references/dense-storyboard-mode.md",
    "references/sequence-project-state.md",
    "skills/visual-storyboard/MODULE.md",
    "scripts/extract_last_frame.py",
    "scripts/project_state_check.py",
    "scripts/schema_check.py",
    "scripts/prompt_architecture_stress.py",
    "scripts/behavior_contract_check.py",
    "scripts/lineage_contract.py",
    "scripts/strict_json.py",
    "data/generation-runs.example.jsonl",
    "examples/sequence-airport-arrival/project-state.json",
    "upstream.lock.json",
)
INVARIANTS = {
    "dialogue language is separate from prompt language": "提示词正文语言与成片对白语言分别处理",
    "prompt defaults to Chinese": "提示词正文必须默认使用中文",
    "Chinese and English switching": "模型提示词支持中文和英文切换",
    "no unsolicited translation": "不自行附加另一语言版本",
    "single professional delivery may remain lightweight": "单片专业交付仍可使用轻量项目记录",
    "platform-neutral creative route exists": "平台未确定的创意发展",
    "visual and dense storyboard modes are distinct": "视觉故事板图”和 Seedance 的",
    "one Seedance compiler is active": "一次任务不要混用两套 Seedance 规则",
    "visible workflow status is reported": "制作状态｜阶段：<当前阶段，可含 L0-L3 或 Scene/Cut>",
    "narrative and non-narrative maturity are distinct": "非叙事制作明确度",
    "storyboard handoff contract is required": "故事板生成与交接合同",
}
PROJECT_SPECIFIC_PATTERNS = (
    "C:/MyPC/",
    "wang.ting",
    "storyboard-demo",
    "codex-clipboard-",
)
STORYBOARD_INVARIANTS = {
    "panel and board aspect ratios are distinct": "目标视频画幅属于**每个分镜格**",
    "board aspect ratio is calculated": "整板宽高比 ≈ 列数 × 单格宽高比 ÷ 行数",
    "execution boards use identity-compatible low detail": "identity_compatible_low_detail + external_deterministic",
    "exact Cut labels are added deterministically": "生产版默认先生成无文字画面",
    "one panel maps to one real Cut": "panel_to_cut_map: one_panel_per_real_cut",
    "one board covers up to nine Cuts": "对1–9个真实 Cut，默认一次生成一张完整执行板",
    "compact layouts cover seven and eight Cuts": "7格：3＋2＋2",
    "color exclusions are conditional": "若使用严格灰阶",
    "single-panel repair is preferred": "只重绘该 Cut，再用确定性排版替换回原位置",
    "storyboard inheritance exclusions are explicit": "do_not_inherit:",
}


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read {path}: {exc}")
        return ""


def frontmatter(text: str, label: str, errors: list[str]) -> str:
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        errors.append(f"{label}: missing or malformed YAML frontmatter")
        return ""
    return match.group(1)


def scalar(block: str, key: str) -> str | None:
    match = re.search(rf"(?m)^[ \t]*{re.escape(key)}:[ \t]*[\"']?([^\r\n\"']+)", block)
    return match.group(1).strip() if match else None


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()

    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_text = read_text(root / "SKILL.md", errors)
    fm = frontmatter(skill_text, "SKILL.md", errors)
    if scalar(fm, "name") != EXPECTED_NAME:
        errors.append(f"SKILL.md: name must be {EXPECTED_NAME}")
    description = scalar(fm, "description")
    if not description or "TODO" in description:
        errors.append("SKILL.md: description is missing or unfinished")
    if scalar(fm, "version") != EXPECTED_VERSION:
        errors.append(
            f"SKILL.md: version must be {EXPECTED_VERSION}"
        )

    for label, phrase in INVARIANTS.items():
        if phrase not in skill_text:
            errors.append(f"missing routing invariant: {label}")

    state_text = read_text(root / "references/project-state-policy.md", errors)
    if "storyboard_status:" not in state_text or "needs_review" not in state_text:
        errors.append("project state: storyboard needs_review state is missing")
    if "active_modules:" not in state_text or "workflow_status: concise|hidden" not in state_text:
        errors.append("project state: visible workflow status fields are missing")

    storyboard_text = read_text(root / "references/storyboard-generation-contract.md", errors)
    for label, phrase in STORYBOARD_INVARIANTS.items():
        if phrase not in storyboard_text:
            errors.append(f"missing storyboard invariant: {label}")

    ui_text = read_text(root / "agents/openai.yaml", errors)
    if "allow_implicit_invocation: true" not in ui_text:
        errors.append("agents/openai.yaml: implicit invocation must remain enabled")
    if "$ai-video-production-director" not in ui_text:
        errors.append("agents/openai.yaml: default prompt must name the skill")

    try:
        lock = json.loads((root / "upstream.lock.json").read_text(encoding="utf-8"))
        if lock.get("skill") != EXPECTED_NAME:
            errors.append("upstream.lock.json: wrong skill")
        if lock.get("version") != EXPECTED_VERSION:
            errors.append("upstream.lock.json: version drift")
        if lock.get("upstream_release") != f"v{EXPECTED_UPSTREAM}":
            errors.append("upstream.lock.json: unexpected upstream release")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"upstream.lock.json: {exc}")

    skills_dir = root / "skills"
    for child in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        module = child / "MODULE.md"
        if not module.is_file():
            errors.append(f"{child.relative_to(root)}: MODULE.md is missing")
            continue
        if (child / "SKILL.md").exists():
            errors.append(f"{child.relative_to(root)}: nested SKILL.md would create duplicate discovery")
        module_text = read_text(module, errors)
        module_fm = frontmatter(module_text, str(module.relative_to(root)), errors)
        if child.name.startswith("seedance-"):
            if scalar(module_fm, "parent") != EXPECTED_NAME:
                errors.append(f"{module.relative_to(root)}: wrong embedded parent")
            if scalar(module_fm, "version") != EXPECTED_UPSTREAM:
                errors.append(f"{module.relative_to(root)}: upstream version drift")

    markdown_files = [root / "SKILL.md"]
    markdown_files.extend((root / "references").rglob("*.md"))
    markdown_files.extend((root / "skills").rglob("*.md"))
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in markdown_files:
        body = read_text(path, errors)
        for match in link_pattern.finditer(body):
            target = unquote(match.group(1).split("#", 1)[0].strip())
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes skill root: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken link: {target}")

    dependency_files = list(markdown_files)
    dependency_files.extend((root / "validation").rglob("*.json"))
    dependency_files.append(root / "agents/openai.yaml")
    dependency_pattern = re.compile(
        r"(?<![A-Za-z0-9_.-])"
        r"((?:scripts|data|schemas|validation|evals)/"
        r"[A-Za-z0-9_./-]+\.(?:py|ps1|sh|js|jsonl?|ya?ml|md|txt))"
        r"(?![A-Za-z0-9_.-])"
    )
    for path in dependency_files:
        body = read_text(path, errors)
        for target in dependency_pattern.findall(body):
            if not (root / target).is_file():
                errors.append(
                    f"{path.relative_to(root)}: missing referenced local artifact: {target}"
                )

    active_text = "\n".join(read_text(path, errors) for path in markdown_files)
    for pattern in PROJECT_SPECIFIC_PATTERNS:
        if pattern in active_text:
            errors.append(f"project-specific example leaked into reusable skill: {pattern}")
    if "[TODO:" in active_text:
        errors.append("unfinished TODO placeholder found")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the AI video production director skill.")
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: skill metadata, routes, modules, links, and invariants are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
