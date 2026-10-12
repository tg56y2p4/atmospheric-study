#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Automation Module for Atmospheric Physics Study Pipeline
Author: Antigravity
"""

import subprocess
import sys
import logging
from pathlib import Path

logger = logging.getLogger("GitSync")

def run_git(args, cwd=None, check=True):
    cmd = ["git"] + args
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(cmd)}\nStderr: {result.stderr.strip()}")
    return result

def has_changes(repo_root):
    res = run_git(["status", "--porcelain"], cwd=repo_root, check=False)
    return bool(res.stdout.strip())

def git_commit_and_push(repo_root, commit_msg="feat(study): auto-sync course notes", branch="main", remote="origin"):
    repo_root = Path(repo_root).resolve()
    logger.info(f"Checking git status in {repo_root}...")

    # 1. Stage changes
    run_git(["add", "."], cwd=repo_root)

    # 2. Check if there are changes to commit
    status = run_git(["status", "--porcelain"], cwd=repo_root, check=False)
    if not status.stdout.strip():
        logger.info("No changes to commit. Working tree clean.")
        return True, "No changes to commit"

    # 3. Commit
    logger.info(f"Committing with message: {commit_msg}")
    commit_res = run_git(["commit", "-m", commit_msg], cwd=repo_root, check=False)
    if commit_res.returncode != 0:
        logger.warning(f"Git commit returned: {commit_res.stderr.strip()}")
        return False, commit_res.stderr.strip()

    # 4. Check remote
    remotes = run_git(["remote"], cwd=repo_root, check=False).stdout.strip().split()
    if remote not in remotes:
        msg = f"Remote '{remote}' not configured yet. Changes committed locally. Run: git remote add origin <github-repo-url>"
        logger.warning(msg)
        return True, msg

    # 5. Push
    logger.info(f"Pushing to {remote}/{branch}...")
    push_res = run_git(["push", remote, branch], cwd=repo_root, check=False)
    if push_res.returncode != 0:
        err_msg = f"Git push failed (possibly network or auth issue): {push_res.stderr.strip()}"
        logger.error(err_msg)
        return False, err_msg

    logger.info("Git push completed successfully!")
    return True, "Pushed successfully"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    repo = Path(__file__).resolve().parent.parent
    msg = sys.argv[1] if len(sys.argv) > 1 else "feat(study): auto-sync course notes"
    success, info = git_commit_and_push(repo, commit_msg=msg)
    print(f"Result: success={success}, info={info}")
