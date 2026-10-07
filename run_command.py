#!/usr/bin/env python3
"""Run a command with arguments and forward its output to the terminal.
   for Windows Shell commands use: cmd /c <command> <args>"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence


def run_command(command: str, arguments: Sequence[str]) -> int:
    """Run an executable and return its exit code.

    Standard output and standard error are inherited from this script, so the
    command's output appears immediately in the calling terminal.
    """
    try:
        completed_process = subprocess.run(
            [command, *arguments],
            check=False,
        )
    except FileNotFoundError:
        print(f"Error: command not found: {command}", file=sys.stderr)
        return 127
    except OSError as error:
        print(f"Error: could not execute {command!r}: {error}", file=sys.stderr)
        return 126

    return completed_process.returncode


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a command and forward its output to the terminal."
    )
    parser.add_argument("command", help="Executable or command to run. For Windows Shell commands use: cmd /c <command> <args>")
    parser.add_argument(
        "parameters",
        nargs=argparse.REMAINDER,
        help="Parameters passed to the command",
    )
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> int:
    """Run the requested command and return its exit code."""
    parsed_arguments = parse_arguments(arguments)
    return run_command(parsed_arguments.command, parsed_arguments.parameters)


if __name__ == "__main__":
    raise SystemExit(main())
