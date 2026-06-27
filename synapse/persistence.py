import json
import os


SYNAPSE_DIR = ".synapse"

METADATA_FILE = os.path.join(SYNAPSE_DIR, "metadata.json")
CONFIG_FILE = os.path.join(SYNAPSE_DIR, "config.json")
CONTEXT_FILE = os.path.join(SYNAPSE_DIR, "context.json")
COMPRESSED_CONTEXT_FILE = os.path.join(
    SYNAPSE_DIR,
    "compressed_context.json"
)


def initialize_synapse():

    files_created = []

    if not os.path.exists(".git"):
        raise Exception(
            "git repository not found, initialize one using 'git init'"
        )

    if os.path.exists(SYNAPSE_DIR):
        print("Synapse is already initialized.")
        return

    os.makedirs(SYNAPSE_DIR)

    try:

        save_metadata(
            {
                "context_name": None,
                "last_processed_commit": None,
            }
        )
        files_created.append(METADATA_FILE)

        save_context({})
        files_created.append(CONTEXT_FILE)

        save_config({})
        files_created.append(CONFIG_FILE)

        save_compressed_context({})
        files_created.append(COMPRESSED_CONTEXT_FILE)

        print("Successfully initialized Synapse repository.")

    except Exception:

        for path in files_created:
            if os.path.exists(path):
                os.remove(path)

        if os.path.exists(SYNAPSE_DIR):
            os.rmdir(SYNAPSE_DIR)

        raise


def save_metadata(metadata: dict):
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def save_config(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def save_context(context: dict):
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=4)


def save_compressed_context(compressed_context: dict):
    with open(COMPRESSED_CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(compressed_context, f, indent=4)


save = save_context


def load_context():

    try:
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {}


def load_compressed_context():

    try:
        with open(
            COMPRESSED_CONTEXT_FILE,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    except FileNotFoundError:
        return {}


def load_metadata():

    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {}


def load_config():

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {}


load_graph = load_context