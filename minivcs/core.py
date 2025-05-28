import os
import json
import shutil
import time
import hashlib
import difflib

def init_repo():
    vcs_dir = ".minivcs"
    commits_dir = os.path.join(vcs_dir, "commits")
    index_file = os.path.join(vcs_dir, "index.json")

    if os.path.exists(vcs_dir):
        print("Repository already initialized.")
        return

    os.makedirs(commits_dir)
    with open(index_file, "w") as f:
        json.dump({"staged": []}, f, indent=4)

    print("Initialized empty MiniVCS repository.")

def add_file(filename):
    vcs_dir = ".minivcs"
    index_file = os.path.join(vcs_dir, "index.json")

    if not os.path.exists(index_file):
        print("Repository not initialized. Run `minivcs init` first.")
        return

    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return

    with open(index_file, "r") as f:
        index = json.load(f)

    if filename in index["staged"]:
        print(f"File '{filename}' already staged.")
        return

    index["staged"].append(filename)

    with open(index_file, "w") as f:
        json.dump(index, f, indent=4)

    print(f"Added '{filename}' to staging area.")

def commit_changes(message):
    vcs_dir = ".minivcs"
    commits_dir = os.path.join(vcs_dir, "commits")
    index_file = os.path.join(vcs_dir, "index.json")

    if not os.path.exists(index_file):
        print("Repository not initialized.")
        return

    with open(index_file, "r") as f:
        index = json.load(f)

    staged_files = index.get("staged", [])
    if not staged_files:
        print("No files staged to commit.")
        return

    # Create a unique commit ID
    commit_id = hashlib.sha1(str(time.time()).encode()).hexdigest()[:7]
    commit_path = os.path.join(commits_dir, commit_id)
    os.makedirs(commit_path)

    # Copy each staged file into the commit folder
    for file in staged_files:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(commit_path, os.path.basename(file)))

    # Create commit metadata
    commit_log = {
        "id": commit_id,
        "timestamp": time.ctime(),
        "message": message,
        "files": staged_files
    }

    with open(os.path.join(commit_path, "meta.json"), "w") as f:
        json.dump(commit_log, f, indent=4)

    # Clear staged files
    with open(index_file, "w") as f:
        json.dump({"staged": []}, f, indent=4)

    print(f"Committed as {commit_id}: \"{message}\"")

def show_log():
    commits_dir = os.path.join(".minivcs", "commits")

    if not os.path.exists(commits_dir):
        print("No commits found.")
        return

    commit_ids = sorted(os.listdir(commits_dir), reverse=True)

    for cid in commit_ids:
        meta_path = os.path.join(commits_dir, cid, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                data = json.load(f)
                print(f"Commit: {data['id']}")
                print(f"Date:   {data['timestamp']}")
                print(f"Message:{data['message']}")
                print(f"Files:  {', '.join(data['files'])}")
                print("-" * 40)

def show_status():
    index_file = os.path.join(".minivcs", "index.json")

    if not os.path.exists(index_file):
        print("Repository not initialized.")
        return

    with open(index_file, "r") as f:
        index = json.load(f)

    staged = index.get("staged", [])

    print("=== Staged Files ===")
    if staged:
        for f in staged:
            print(f"  {f}")
    else:
        print("  (none)")

    # Detect untracked files
    tracked = set(staged)
    all_files = set([
        f for f in os.listdir(".")
        if os.path.isfile(f) and not f.startswith(".")
    ])

    untracked = all_files - tracked

    print("\n=== Untracked Files ===")
    if untracked:
        for f in untracked:
            print(f"  {f}")
    else:
        print("  (none)")

def remove_file(filename):
    index_file = os.path.join(".minivcs", "index.json")

    if not os.path.exists(index_file):
        print("Repository not initialized.")
        return

    with open(index_file, "r") as f:
        index = json.load(f)

    if filename not in index["staged"]:
        print(f"File '{filename}' is not staged.")
        return

    index["staged"].remove(filename)

    with open(index_file, "w") as f:
        json.dump(index, f, indent=4)

    print(f"Removed '{filename}' from staging area.")

def checkout_commit(commit_id):
    commit_path = os.path.join(".minivcs", "commits", commit_id)

    if not os.path.exists(commit_path):
        print(f"No commit found with ID '{commit_id}'.")
        return

    for file in os.listdir(commit_path):
        if file == "meta.json":
            continue
        src = os.path.join(commit_path, file)
        dst = file
        shutil.copy(src, dst)

    print(f"Checked out files from commit {commit_id}.")

def show_diff():
    index_file = os.path.join(".minivcs", "index.json")
    commits_dir = os.path.join(".minivcs", "commits")

    if not os.path.exists(index_file) or not os.path.exists(commits_dir):
        print("Repository not initialized.")
        return

    with open(index_file, "r") as f:
        index = json.load(f)

    staged = index.get("staged", [])
    if not staged:
        print("No files staged.")
        return

    commit_ids = sorted(os.listdir(commits_dir), reverse=True)

    for file in staged:
        found = False
        for commit_id in commit_ids:
            committed_path = os.path.join(commits_dir, commit_id, os.path.basename(file))
            if os.path.exists(committed_path):
                with open(committed_path, "r") as f1, open(file, "r") as f2:
                    committed_lines = f1.readlines()
                    current_lines = f2.readlines()
                    diff = difflib.unified_diff(
                        committed_lines,
                        current_lines,
                        fromfile=f"commit:{commit_id}",
                        tofile="working copy"
                    )
                    print(f"\n--- Diff for {file} ---")
                    diff_output = ''.join(diff)
                    if diff_output:
                        print(diff_output)
                    else:
                        print("No changes.")
                found = True
                break
        if not found:
            print(f"No previous commit found for {file}.")

