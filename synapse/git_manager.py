from math import ceil

from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError


NULL_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

try:
    repo = Repo(search_parent_directories=True)
except (InvalidGitRepositoryError, NoSuchPathError):
    print("please initialize a git repository and try again")


MAX_FILE_DIFF_SIZE = 10000
MAX_HUNK_DIFF_SIZE = 8000

commits_allowed = 50
file_changes_allowed = 50
lines_changes_allowed = 50000
max_diffs = 50


def get_last_processed_commit(metadata):
    return metadata.get("last_processed_commit")


def processing_strategy(left_boundary):
    head = repo.head.commit

    if left_boundary != head.hexsha:

        added = deleted = 0

        for lines in repo.git.diff(
            "--numstat",
            left_boundary,
            "HEAD"
        ).splitlines():
            a, d, _ = lines.split("\t")

            try:
                added += int(a)
            except ValueError:
                pass

            try:
                deleted += int(d)
            except ValueError:
                pass

        lines_changed = added + deleted

        commit_count = sum(
            1
            for _ in repo.iter_commits(f"{left_boundary}..HEAD")
        )

        files_changed = len(
            repo.git.diff(
                "--name-only",
                left_boundary,
                "HEAD"
            ).splitlines()
        )

        if commit_count <= commits_allowed:
            if files_changed <= file_changes_allowed:
                if lines_changed <= lines_changes_allowed:
                    return "log"

        if commit_count < 100000:
            return "evolution_diff"

        return "diff"

    return None


def get_repository_changes(metadata):

    last_processed_commit = get_last_processed_commit(metadata)

    if last_processed_commit:

        left_boundary = last_processed_commit

        commits = list(
            repo.iter_commits(f"{left_boundary}..HEAD")
        )

        commits.reverse()

    else:

        commits = list(repo.iter_commits("HEAD"))

        left_boundary = commits[-1].hexsha

        commits.reverse()

    strategy = processing_strategy(left_boundary)

    repo_changes = []

    head = repo.head.commit

    if not strategy:
        return repo_changes

    if strategy == "log":

        for commit in commits:

            if commit.parents:
                diffs = commit.parents[0].diff(
                    commit,
                    create_patch=True
                )
            else:
                diffs = commit.diff(
                    NULL_TREE,
                    create_patch=True
                )

            patch = ""

            for diff in diffs:

                try:
                    per_file_diff = diff.diff.decode("utf-8")
                except UnicodeDecodeError:
                    continue

                a_path = diff.a_path or diff.b_path
                b_path = diff.b_path or diff.a_path

                patch += f"diff --git a/{a_path} b/{b_path}\n"
                patch += f"--- a/{a_path}\n"
                patch += f"+++ b/{b_path}\n"
                patch += f"{per_file_diff}\n"

            repo_changes.append(
                {
                    "strategy": strategy,
                    "sha": commit.hexsha,
                    "message": commit.message,
                    "diff": patch,
                }
            )

        return repo_changes

    if strategy == "evolution_diff":

        commits = list(reversed(list(repo.iter_commits("HEAD"))))

        step = ceil(len(commits) / max_diffs)

        indices = list(
            range(step - 1, len(commits), step)
        )

        left_bound = (
            NULL_TREE
            if not last_processed_commit
            else last_processed_commit
        )

        if not indices or indices[-1] != len(commits) - 1:
            indices.append(len(commits) - 1)

        for index in indices:

            right_bound = commits[index]

            diffs = repo.commit(left_bound).diff(
                right_bound.hexsha,
                create_patch=True,
            )

            left_bound = right_bound.hexsha

            patch = ""

            for diff in diffs:

                try:
                    per_file_diff = diff.diff.decode("utf-8")
                except UnicodeDecodeError:
                    continue

                a_path = diff.a_path or diff.b_path
                b_path = diff.b_path or diff.a_path

                patch += f"diff --git a/{a_path} b/{b_path}\n"
                patch += f"--- a/{a_path}\n"
                patch += f"+++ b/{b_path}\n"
                patch += f"{per_file_diff}\n"

            repo_changes.append(
                {
                    "strategy": strategy,
                    "sha": right_bound.hexsha,
                    "message": right_bound.message,
                    "diff": patch,
                }
            )

        return repo_changes

    if last_processed_commit:
        diffs = repo.commit(left_boundary).diff(
            head,
            create_patch=True,
        )
    else:
        diffs = head.diff(
            NULL_TREE,
            create_patch=True,
        )

    patch = ""

    for diff in diffs:

        try:
            per_file_diff = diff.diff.decode("utf-8")
        except UnicodeDecodeError:
            continue

        a_path = diff.a_path or diff.b_path
        b_path = diff.b_path or diff.a_path

        patch += f"diff --git a/{a_path} b/{b_path}\n"
        patch += f"--- a/{a_path}\n"
        patch += f"+++ b/{b_path}\n"
        patch += f"{per_file_diff}\n"

    repo_changes.append(
        {
            "strategy": strategy,
            "sha": head.hexsha,
            "message": head.message,
            "diff": patch,
        }
    )

    return repo_changes


def get_repository_context(repo_changes):

    if not repo_changes:
        return {
            "strategy": None,
            "data": [],
        }

    strategy = repo_changes[0]["strategy"]

    repo_context = {
        "strategy": strategy,
        "data": [],
    }

    for commit_context in repo_changes:

        repo_context["data"].append(
            {
                "sha": commit_context["sha"],
                "message": commit_context["message"],
                "diff": commit_context["diff"],
            }
        )

    return repo_context

def preprocess_readme_diff(file_diff: str) -> str:
    """
    Remove documentation sections that are not durable repository knowledge.
    """
    ignored_sections = [
        "# Installation",
        "## Installation",

        "# Quick Start",
        "## Quick Start",

        "# Getting Started",
        "## Getting Started",

        "# Setup",
        "## Setup",

        "# Requirements",
        "## Requirements",

        "# Prerequisites",
        "## Prerequisites",

        "# Usage",
        "## Usage",

        "# Example",
        "## Example",

        "# Examples",
        "## Examples",

        "# Demo",
        "## Demo",

        "# Screenshots",
        "## Screenshots",

        "# Benchmark",
        "## Benchmark",

        "# Benchmarks",
        "## Benchmarks",

        "# Performance",
        "## Performance",

        "# Testing",
        "## Testing",

        "# Troubleshooting",
        "## Troubleshooting",

        "# FAQ",
        "## FAQ",

        "# Changelog",
        "## Changelog",

        "# Release Notes",
        "## Release Notes",

        "# Version History",
        "## Version History",

        "# Contributing",
        "## Contributing",

        "# Authors",
        "## Authors",

        "# Author",
        "## Author",

        "# Credits",
        "## Credits",

        "# Acknowledgements",
        "## Acknowledgements",

        "# Citation",
        "## Citation",

        "# License",
        "## License",

        "# Contact",
        "## Contact",

        "# Support",
        "## Support"
    ]

    lines = file_diff.splitlines()

    result = []

    skip = False

    for line in lines:

        stripped = line.strip()

        if stripped.startswith("#"):
            skip = any(
                stripped.lower().startswith(section.lower())
                for section in ignored_sections
            )

        if not skip:
            result.append(line)

    return "\n".join(result)


def split_file_by_hunk(change, file_diff):

    split_changes = []

    lines = file_diff.splitlines(keepends=True)

    header = []
    hunks = []

    current_hunk = []

    for line in lines:

        if line.startswith("@@"):

            if current_hunk:
                hunks.append(current_hunk)

            current_hunk = [line]

        elif current_hunk:
            current_hunk.append(line)

        else:
            header.append(line)

    if current_hunk:
        hunks.append(current_hunk)

    header_text = "".join(header)

    current_diff = header_text

    for hunk in hunks:

        hunk_text = "".join(hunk)

        if (
            len(current_diff) + len(hunk_text)
            > MAX_HUNK_DIFF_SIZE
            and current_diff != header_text
        ):

            new_change = change.copy()
            new_change["diff"] = current_diff

            split_changes.append(new_change)

            current_diff = header_text + hunk_text

        else:
            current_diff += hunk_text

    if current_diff != header_text:

        new_change = change.copy()
        new_change["diff"] = current_diff

        split_changes.append(new_change)

    return split_changes


def split_commit_by_file(change):

    split_changes = []

    parts = change["diff"].split("diff --git ")

    for part in parts:

        part = part.strip()

        if not part:
            continue

        file_diff = "diff --git " + part
        if "README.md" in file_diff:
            file_diff = preprocess_readme_diff(file_diff)

        if len(file_diff) > MAX_FILE_DIFF_SIZE:

            split_changes.extend(
                split_file_by_hunk(
                    change,
                    file_diff,
                )
            )

            continue

        new_change = change.copy()
        new_change["diff"] = file_diff

        split_changes.append(new_change)

    return split_changes