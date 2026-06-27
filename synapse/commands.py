from .persistence import initialize_synapse
from .processor import build_repository_context
from .extractor import build_compressed_context


def init():
    initialize_synapse()


def knowledge():
    print("Initializing repository context...")

    build_repository_context()

    print(
        "Repository context initialized.\n"
        "Building compressed repository context..."
    )

    build_compressed_context()

    print("Successfully initialized compressed repository context.")