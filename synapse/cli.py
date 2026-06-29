import sys
from . import commands


def main():

    if len(sys.argv) < 2:
        print("Usage: synapse <command>")
        print()
        print("Available commands:")
        print("  init")
        print("  knowledge")
        print("  setup")
        return

    command = sys.argv[1].lower()

    if command == "init":
        commands.init()

    elif command == "knowledge":
        commands.knowledge()
    
    elif command == "setup":
        commands.setup()

    else:
        print(f"Unknown command: {command}")