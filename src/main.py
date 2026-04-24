"""Application entry point."""
import sys

from .core.database import Database
from .ui.app import PulsarApp
from .ui.main_window import MainWindow
from .ui.signals import signals


def main():
    app = PulsarApp(sys.argv)

    db = Database()

    window = MainWindow(db)
    window.show()

    signals.status_message.emit("Welcome to PulsarNote", 5000)

    try:
        sys.exit(app.exec())
    finally:
        db.close()


if __name__ == "__main__":
    main()
