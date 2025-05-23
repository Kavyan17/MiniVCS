import os
import json
import shutil
import time
import hashlib

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
