import os
import json

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
