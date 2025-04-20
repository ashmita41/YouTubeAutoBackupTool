#!/usr/bin/env python3
"""
YouTubeAutoBackupTool - Main Entry Point
"""

import sys
from PySide6.QtWidgets import QApplication

from src.ui import YouTubeDownloaderApp


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 