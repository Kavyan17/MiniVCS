# MiniVCS

## 🧩 MiniVCS - A Minimal Version Control System
MiniVCS is a simplified version control tool implemented in Python, similar to Git. It supports basic commands like init, add, commit, log, status, remove, checkout, and diff.

## 📦 Setup
    git clone <your-repo-url>
    cd MiniVCS
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt 

## 🚀 Usage
All commands are run via:
    python cli.py <command>

## ✅ Features and Commands
1. 🔧 Initialize a Repository
    python cli.py init

Creates .minivcs/ with:
    - commits/ folder to store snapshots
    - index.json to manage staging area

2. ➕ Stage Files
    python cli.py add <filename>
Adds a file to the staging area (tracked in index.json).

3. ✅ Commit Changes
    python cli.py commit "<message>"
Creates a commit:
    - Copies staged files to .minivcs/commits/<commit-id>/
    - Stores metadata like ID, timestamp, message, and file list

4. 📋 Show Commit History
    python cli.py log
Displays all commits in reverse chronological order.

5. 🔍 Check Repository Status
    python cli.py status
Shows:
    - Staged Files (ready to commit)
    - Untracked Files (exist but not staged)

6. 🗑️ Remove from Staging
    python cli.py remove <filename>
Unstages a file (removes from index.json).

7. 📦 Checkout a Commit
    python cli.py checkout <commit-id>
    Restores all committed files from a specific commit to your working directory.

To get a commit ID:
    python cli.py log

8. 🔍 Show File Differences
    python cli.py diff
Shows the line-by-line difference between:
    - The staged file in your working directory
    - Its last committed version

📁 Project Structure
    MiniVCS/
    ├── cli.py          # CLI commands
    ├── minivcs/
    │   ├── __init__.py
    │   └── core.py     # Core logic
    ├── .minivcs/
    │   ├── commits/
    │   └── index.json
    └── README.md

🔮 Coming Soon (Ideas)
    - branch, merge, tag
    - file-level diff views
    - conflict resolution
    - file ignore rules (.minivcsignore)
    - CLI install: pip install -e .


