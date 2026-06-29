from .persistence import initialize_synapse, save_config
from .processor import build_repository_context
from .extractor import build_compressed_context
from .provider import get_ollama_model


def setup():
    models = get_ollama_model()

    for i,model in enumerate(models,start=1):
        print(f"{i}, {model}")
    choice = int(input("select a model"))
    selected_model = models[choice-1]
    save_config(
        {
            "provider":"ollama",
            "model": selected_model
        }
    )
    print("configuration saved")


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