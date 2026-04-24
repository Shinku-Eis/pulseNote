"""Application entry point - CRITICAL FIX: QApplication FIRST!"""
import sys
print("Step 1: Starting...")
sys.stdout.flush()

# ==========================================
# CRITICAL PYINSTALLER FIX
# QApplication MUST BE CREATED BEFORE ANY 
# QObject-derived class is instantiated!
# ==========================================
from PyQt6.QtWidgets import QApplication
print("Step 2: QApplication base imported")
sys.stdout.flush()

_temp_app = QApplication(sys.argv)
print("Step 3: QApplication created FIRST - this prevents stack overflow!")
sys.stdout.flush()

# NOW it's SAFE to import everything else!
print("Step 4: Importing modules...")
sys.stdout.flush()

from .core.database import Database
print("  core.database OK")
sys.stdout.flush()

from .ui.app import PulsarApp
print("  ui.app OK")
sys.stdout.flush()

from .ui.main_window import MainWindow
print("  ui.main_window OK")
sys.stdout.flush()

from .ui.signals import get_signals
print("  signals module imported")
sys.stdout.flush()

print("\n======= ALL IMPORTS SUCCESS =======")
sys.stdout.flush()


def main():
    global _temp_app
    print("Starting PulsarApp...")
    sys.stdout.flush()
    
    # Clean up temp app
    _temp_app.quit()
    del _temp_app
    
    app = PulsarApp(sys.argv)
    signals = get_signals()

    print("Initializing database...")
    sys.stdout.flush()
    db = Database()

    print("Creating window...")
    sys.stdout.flush()
    window = MainWindow(db)
    window.show()

    print("Ready!")
    sys.stdout.flush()
    signals.status_message.emit("PulsarNote started successfully!", 4000)

    try:
        sys.exit(app.exec())
    finally:
        db.close()


if __name__ == "__main__":
    main()
