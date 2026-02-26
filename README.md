🚀 Python Import Installer
Automatically detect and install missing third-party dependencies in your Python project.

📌 Overview
Python Import Installer is a lightweight automation tool that scans a project directory for Python files, detects imported modules, identifies missing third-party dependencies, and installs them automatically using pip.

It is designed to simplify dependency management when:
📥 You cloned a repository without a requirements.txt
🧩 You inherited legacy code
🔍 You are auditing a project structure
⚙️ You want a fast dependency sanity check
Instead of manually checking imports and installing packages one by one, this script analyzes Python files using AST parsing and installs only what’s missing.

🧠 How It Works
The script:
🔎 Scans .py files in the current directory
📂 Optionally scans subdirectories
🧾 Extracts import and from ... import ... statements using Python’s ast module
🚫 Filters out:
Standard library modules
Built-in modules
Local project modules

📦 Detects which third-party modules are not installed
⚡ Installs missing packages automatically using pip
🔄 Handles common module-to-pip mismatches (e.g. PIL → Pillow)

✨ Features
✅ AST-based import parsing (reliable and accurate)
✅ Standard library detection
✅ Local module detection
✅ Automatic pip installation
✅ Module → pip name mapping support
✅ Optional recursive scanning
✅ Clean and readable terminal output
✅ Cross-platform (Windows / Linux / macOS)

🖥 Requirements
Python 3.9+ (recommended)
pip installed
Internet connection (for package installation)

⚙️ Installation & Setup
🪟 Windows
Install Python from:
👉 https://www.python.org/downloads/
During installation:
✔ Check “Add Python to PATH”
Verify installation:
python --version
pip --version

Run the script:
python import_installer.py
🔐 Recommended: Use a Virtual Environment
python -m venv venv
venv\Scripts\activate
python import_installer.py

🐧 Linux
Check Python:
python3 --version
pip3 --version

If pip is missing:
Debian/Ubuntu
sudo apt install python3-pip
Fedora
sudo dnf install python3-pip

Run the script:
python3 import_installer.py
🔐 With Virtual Environment (Recommended)
python3 -m venv venv
source venv/bin/activate
python3 import_installer.py

🎯 Use Cases
This tool is especially useful for:
🛡 Security researchers auditing codebases
👨‍💻 Developers onboarding into unfamiliar projects
🎓 Students learning Python dependency management
⚙️ DevOps engineers validating environments
🧹 Cleaning up broken or incomplete setups

💪 Strengths
Uses AST parsing instead of naive string matching
Correctly distinguishes stdlib from third-party packages
Detects local modules to avoid false positives
Automatically maps common import/package name differences

Minimal external dependencies
Does not modify project files

⚠️ Limitations
Does not generate requirements.txt
Installs latest versions (no version pinning)
Does not resolve nested dependency conflicts
Assumes pip package name equals module name unless mapped

🔮 Future Improvements
Planned enhancements could include:
🏷 CLI arguments (--recursive, --dry-run, --auto-install)
📝 Optional requirements.txt generation
📊 Logging instead of print statements

🧾 Example Output
=== Python Import Installer ===
Folder: /home/user/project

Scan subdirectories as well? (Y/n): y
Found 12 Python files.
Imports: os, sys, requests, flask
Standard library: os, sys
Missing modules: requests, flask

Installing:
python -m pip install requests flask
🏁 Final Thoughts

This tool solves a real developer pain point: missing dependencies.

🚧 Status
Stable working version. Further improvements and refinements are planned.

⚠️ Responsible Use
Review detected dependencies before installation and ensure they come from trusted sources.

📄 License
MIT License
