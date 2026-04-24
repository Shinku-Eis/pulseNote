# -*- coding: utf-8 -*-
"""Minimal test to find which import causes crash."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import traceback

print("Step 0: Starting test...")
sys.stdout.flush()

test_modules = [
    ("PyQt6.QtWidgets", "from PyQt6 import QtWidgets; print('QtWidgets imported')"),
    ("src.core.database", "from src.core.database import Database; print('Database imported')"),
    ("src.ui.app", "from src.ui.app import PulsarApp; print('PulsarApp imported')"),
    ("src.ui.signals", "from src.ui.signals import signals; print('signals imported')"),
    ("src.ui.navigation.folder_tree", "from src.ui.navigation.folder_tree import FolderTree; print('FolderTree imported')"),
]

for name, code in test_modules:
    print(f"\nTesting: {name}")
    sys.stdout.flush()
    try:
        exec(code)
        print(f"  [OK]")
        sys.stdout.flush()
    except Exception as e:
        print(f"  [FAILED]: {e}")
        traceback.print_exc()
        sys.stdout.flush()

print("\n=== All tests done ===")
