"""Application entry point - CRITICAL FIX: CORRECT IMPORT ORDER!
PyInstaller + PyQt6 BUG FIXES:
1. QWebEngineWidgets must be imported BEFORE QApplication
2. Qt.AA_ShareOpenGLContexts must be set BEFORE creating QApplication
3. Any QObject MUST be created AFTER QApplication exists
4. In windowed mode, sys.stdout is None - don't access buffer
"""
import sys

# Safe stdout encoding fix - ONLY when running in console mode
if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr is not None and hasattr(sys.stderr, 'buffer'):
    import io
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def safe_print(msg):
    if sys.stdout is not None:
        try:
            print(msg)
            sys.stdout.flush()
        except:
            pass

safe_print("Step 1: Starting...")

# ==================================================
# CRITICAL PYINSTALLER + PYQT6 BUG FIX #1
# QWebEngineWidgets MUST be imported BEFORE QApplication
# ==================================================
safe_print("Step 2: Importing QWebEngine FIRST...")
from PyQt6.QtWebEngineWidgets import QWebEngineView
safe_print("  QWebEngine imported OK")

# ==================================================
# CRITICAL PYINSTALLER + PYQT6 BUG FIX #2
# Set AA_ShareOpenGLContexts BEFORE creating QApplication
# ==================================================
safe_print("Step 3: Setting OpenGL context attribute...")
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
safe_print("  OpenGL attribute set OK")

# ==================================================
# CRITICAL PYINSTALLER + PYQT6 BUG FIX #3
# Create QApplication BEFORE any other QObject-derived class
# ==================================================
safe_print("Step 4: Creating QApplication NOW - BEFORE all other imports...")
_temp_app = QApplication(sys.argv)
safe_print("  QApplication created FIRST!")

# ==================================================
# FINALLY: Safe to import everything else
# ==================================================
safe_print("Step 5: Importing all other modules...")

from .core.database import Database
safe_print("  core.database OK")

from .ui.app import PulsarApp
safe_print("  ui.app OK")

from .ui.main_window import MainWindow
safe_print("  ui.main_window OK")

from .ui.signals import get_signals
safe_print("  signals module imported OK")

safe_print("======= ALL IMPORTS SUCCESS =======")


def main():
    global _temp_app
    safe_print("\nStarting PulsarNote...")
    
    _temp_app.quit()
    del _temp_app
    
    app = PulsarApp(sys.argv)
    signals = get_signals()

    safe_print("Initializing database...")
    db = Database()

    safe_print("Creating window...")
    window = MainWindow(db)
    window.show()

    safe_print("PulsarNote is RUNNING!")
    signals.status_message.emit("PulsarNote started successfully!", 4000)

    try:
        sys.exit(app.exec())
    finally:
        db.close()


if __name__ == "__main__":
    main()
