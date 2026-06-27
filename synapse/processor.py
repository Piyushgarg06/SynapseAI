from .git_manager import get_repository_changes, get_repository_context
from .persistence import load_metadata, save_context, load_context


def build_repository_context():
    metadata = load_metadata()

    repo_changes = get_repository_changes(metadata)
    if not repo_changes:
        return
    new_context = get_repository_context(repo_changes)
    existing_context = load_context()
    if not existing_context:
        save_context(new_context)
        return
    existing_sha = {
        item["sha"]
        for item in existing_context["data"]
    }
    for item in new_context["data"]:
        if item["sha"] not in existing_sha:
            existing_context["data"].append(item)

    save_context(existing_context)

    print("Successfully initialized repository context.")