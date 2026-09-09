"""DUB.SAR 1.0 — CLI entry point when invoked as a module: python -m dubsar."""

import sys
from dubsar.cli import main

if __name__ == "__main__":
    sys.exit(main())
