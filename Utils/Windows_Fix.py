# utils/windows_fix.py
"""
Windows UTF-8 Encoding Fix

This module forces Windows terminals to use UTF-8 encoding instead of cp1252.
Import this ONCE at the very top of your main.py file to enable emoji support
and proper Unicode handling across your entire application.

Usage:
    import utils.windows_fix  # That's it. No function calls needed.

Why this works:
    The import statement executes all top-level code in the module exactly once.
    This sets up the UTF-8 wrapper before any other code runs.
"""

import sys
import io


def _apply_windows_utf8_fix():
    """
    Internal function that applies the UTF-8 encoding fix.
    The underscore prefix (_apply_windows_utf8_fix) is a Python convention
    that means "this is private, don't call it directly."
    """
    if sys.platform == "win32":
        # Force UTF-8 on standard output (print statements)
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding="utf-8",
            errors="replace",  # If a character still fails, show � instead of crashing
        )

        # Force UTF-8 on standard error (error messages and logging)
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )


# This runs automatically when the module is imported
_apply_windows_utf8_fix()
