#!/usr/bin/env python3

from __future__ import annotations

import ast
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Set, Dict, List

MODULE_TO_PIP: Dict[str, str] = {
    "PIL": "Pillow",
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "Crypto": "pycryptodome",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "jwt": "PyJWT",
    "dateutil": "python-dateutil",
    "dotenv": "python-dotenv",
}

SKIP_DIRS = {
    ".git", "__pycache__", "venv", ".venv", "env",
    "build", "dist", "node_modules"
}


def find_imports(code: str) -> Set[str]:
    tree = ast.parse(code)
    modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                modules.add(node.module.split(".")[0])

    return modules


def is_stdlib(module: str) -> bool:
    if module in sys.builtin_module_names:
        return True

    std = getattr(sys, "stdlib_module_names", set())
    if module in std:
        return True

    try:
        import importlib.util
        spec = importlib.util.find_spec(module)
        if spec and spec.origin:
            origin = Path(spec.origin)
            stdlib = Path(sysconfig.get_paths()["stdlib"])
            return stdlib in origin.parents
    except Exception:
        pass

    return False


def is_local_module(root: Path, module: str) -> bool:
    if (root / f"{module}.py").exists():
        return True
    if (root / module / "__init__.py").exists():
        return True
    return False


def scan_files(root: Path, recursive: bool) -> List[Path]:
    if recursive:
        return [
            p for p in root.rglob("*.py")
            if not any(part in SKIP_DIRS for part in p.parts)
        ]
    return list(root.glob("*.py"))


def module_to_pip(module: str) -> str:
    return MODULE_TO_PIP.get(module, module)


def is_importable(module: str) -> bool:
    try:
        import importlib.util
        return importlib.util.find_spec(module) is not None
    except Exception:
        return False


def install_packages(packages: List[str]):
    if not packages:
        print("\n✔ All dependencies are already installed.")
        return

    cmd = [sys.executable, "-m", "pip", "install", *packages]
    print("\nInstalling:\n", " ".join(cmd), "\n")
    subprocess.call(cmd)


def run_scan(root: Path):
    recursive = input("\nScan subdirectories as well? (Y/n): ").lower() != "n"

    files = scan_files(root, recursive)
    print(f"\nFound {len(files)} Python files.")

    imports = set()

    for file in files:
        try:
            code = file.read_text(encoding="utf-8", errors="ignore")
            imports |= find_imports(code)
        except Exception:
            print(f"Skipped: {file}")

    local_modules = {m for m in imports if is_local_module(root, m)}
    stdlib_modules = {m for m in imports if is_stdlib(m)}

    candidates = imports - local_modules - stdlib_modules
    missing = [m for m in sorted(candidates) if not is_importable(m)]

    print("\nImports:", ", ".join(sorted(imports)))
    if local_modules:
        print("Local modules:", ", ".join(sorted(local_modules)))
    if stdlib_modules:
        print("Standard library:", ", ".join(sorted(stdlib_modules)))

    if not missing:
        print("\n✔ No missing modules.")
        return

    pip_packages = [module_to_pip(m) for m in missing]

    print("\nMissing modules:", ", ".join(missing))
    install_packages(pip_packages)


def main():
    root = Path(__file__).resolve().parent
    print("=== Python Import Installer ===")
    print(f"Folder: {root}")

    while True:
        run_scan(root)

        exit_choice = input("\nDo you want to exit? (Y/n): ").lower()

        if exit_choice == "y" or exit_choice == "":
            print("Closing...")
            sys.exit()

        print("\nStarting new scan...")


if __name__ == "__main__":
    main()