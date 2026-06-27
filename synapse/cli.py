import sys

from . import commands


def main():

    if len(sys.argv) < 2:
        print("Usage: synapse <command>")
        print()
        print("Available commands:")
        print("  init")
        print("  knowledge")
        return

    command = sys.argv[1].lower()

    if command == "init":
        commands.init()

    elif command == "knowledge":
        commands.knowledge()

    else:
        print(f"Unknown command: {command}")