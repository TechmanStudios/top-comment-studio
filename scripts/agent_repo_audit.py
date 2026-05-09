#!/usr/bin/env python3
"""
Lightweight repository audit for AI coding agents.

Run from the repository root:

    python scripts/agent_repo_audit.py

This script uses only the Python standard library. It scans common setup files,
detects likely commands, finds environment variable references, and writes
AI_REPO_AUDIT.md.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Iterable


ROOT = Path.cwd()
REPORT = ROOT / "AI_REPO_AUDIT.md"

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".next",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".env",
    ".example",
    ".sh",
    ".sql",
    ".html",
    ".css",
}


def exists(name: str) -> bool:
    return (ROOT / name).exists()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def iter_files(max_files: int = 1500) -> Iterable[Path]:
    count = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() in TEXT_EXTENSIONS or filename.startswith(".env"):
                count += 1
                if count > max_files:
                    return
                yield path


def detect_stack() -> list[str]:
    stack = []

    if exists("package.json"):
        pkg = read_json(ROOT / "package.json")
        deps = {}
        deps.update(pkg.get("dependencies", {}))
        deps.update(pkg.get("devDependencies", {}))

        if "next" in deps:
            stack.append("Next.js")
        if "react" in deps:
            stack.append("React")
        if "vite" in deps:
            stack.append("Vite")
        if "express" in deps:
            stack.append("Express")
        if "typescript" in deps:
            stack.append("TypeScript")
        if not stack:
            stack.append("Node.js / JavaScript")

    if exists("pyproject.toml") or exists("requirements.txt"):
        stack.append("Python")

    if exists("Dockerfile") or exists("docker-compose.yml") or exists("compose.yml"):
        stack.append("Docker")

    return stack or ["Unknown"]


def detect_package_manager() -> str:
    if exists("pnpm-lock.yaml"):
        return "pnpm"
    if exists("yarn.lock"):
        return "yarn"
    if exists("package-lock.json"):
        return "npm"
    if exists("uv.lock"):
        return "uv"
    if exists("poetry.lock"):
        return "poetry"
    if exists("requirements.txt"):
        return "pip"
    return "Unknown"


def detect_scripts() -> dict:
    scripts = {}

    package_json = ROOT / "package.json"
    if package_json.exists():
        pkg = read_json(package_json)
        scripts["package.json"] = pkg.get("scripts", {})

    pyproject = ROOT / "pyproject.toml"
    if pyproject.exists():
        scripts["pyproject.toml"] = "Present; inspect for tool-specific commands."

    if exists("Makefile"):
        scripts["Makefile"] = "Present; inspect make targets."

    if exists("docker-compose.yml") or exists("compose.yml"):
        scripts["Docker Compose"] = "Present."

    return scripts


def detect_env_vars() -> list[str]:
    patterns = [
        re.compile(r"os\.environ(?:\.get)?\([\"']([A-Z0-9_]+)[\"']"),
        re.compile(r"process\.env\.([A-Z0-9_]+)"),
        re.compile(r"import\.meta\.env\.([A-Z0-9_]+)"),
        re.compile(r"\b([A-Z][A-Z0-9_]{2,})\b"),
    ]

    env_vars = set()
    for path in iter_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for pattern in patterns[:3]:
            env_vars.update(pattern.findall(text))

    # Filter noisy all-caps names by checking common env-like suffixes/prefixes.
    likely = {
        item
        for item in env_vars
        if any(
            token in item
            for token in [
                "API",
                "KEY",
                "TOKEN",
                "SECRET",
                "URL",
                "URI",
                "DATABASE",
                "DB",
                "HOST",
                "PORT",
                "ENV",
                "AUTH",
            ]
        )
    }

    return sorted(likely)


def suggest_commands(package_manager: str, scripts: dict) -> list[str]:
    commands = []

    pkg_scripts = scripts.get("package.json")
    if isinstance(pkg_scripts, dict):
        for script in ["dev", "start", "build", "test", "lint", "typecheck"]:
            if script in pkg_scripts:
                if package_manager == "pnpm":
                    commands.append(f"pnpm {script}")
                elif package_manager == "yarn":
                    commands.append(f"yarn {script}")
                else:
                    commands.append(f"npm run {script}" if script not in ["start"] else "npm start")

    if package_manager == "uv":
        commands.append("uv sync")
    elif package_manager == "poetry":
        commands.append("poetry install")
    elif package_manager == "pip":
        commands.append("python -m pip install -r requirements.txt")

    if exists("pytest.ini") or exists("tests") or exists("test"):
        commands.append("python -m pytest")

    if exists("docker-compose.yml"):
        commands.append("docker compose up --build")

    return list(dict.fromkeys(commands))


def write_report() -> None:
    stack = detect_stack()
    package_manager = detect_package_manager()
    scripts = detect_scripts()
    env_vars = detect_env_vars()
    commands = suggest_commands(package_manager, scripts)

    lines = [
        "# AI Repo Audit",
        "",
        "Generated by `scripts/agent_repo_audit.py`.",
        "",
        "## Detected Stack",
        "",
    ]

    for item in stack:
        lines.append(f"- {item}")

    lines += [
        "",
        "## Detected Package Manager",
        "",
        f"- {package_manager}",
        "",
        "## Existing Scripts / Tooling",
        "",
    ]

    if scripts:
        for source, value in scripts.items():
            lines.append(f"### {source}")
            lines.append("")
            if isinstance(value, dict):
                if value:
                    for name, command in value.items():
                        lines.append(f"- `{name}`: `{command}`")
                else:
                    lines.append("- No scripts found.")
            else:
                lines.append(f"- {value}")
            lines.append("")
    else:
        lines.append("- No common script files detected.")
        lines.append("")

    lines += [
        "## Suggested Validation Commands",
        "",
    ]

    if commands:
        for command in commands:
            lines.append(f"- `{command}`")
    else:
        lines.append("- No obvious validation commands detected.")

    lines += [
        "",
        "## Likely Environment Variables",
        "",
    ]

    if env_vars:
        for var in env_vars:
            lines.append(f"- `{var}`")
    else:
        lines.append("- No obvious environment variables detected.")

    lines += [
        "",
        "## Recommended Next Steps",
        "",
        "1. Confirm the detected package manager.",
        "2. Confirm the local dev command.",
        "3. Update `README.md` with exact setup steps.",
        "4. Update `.env.example` with only variables actually used by the repo.",
        "5. Run at least one validation command.",
        "",
    ]

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    write_report()
