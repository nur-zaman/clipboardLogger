import sys
import os
import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QMessageBox,
    QCheckBox,
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5 import QtCore
import clipboard
from PyQt5.QtCore import Qt


class ClipboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.clipList = self.load_last_10_logs()  # Load last 10 logs on app start

        self.notice = QLabel("Click an item to copy")

        self.setWindowTitle("Clipboard Logger")
        self.setWindowIcon(QIcon("clipboard.ico"))
        self.setMinimumSize(200, 100)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        label_font = QFont("Arial", 18)
        # label = QLabel("Clipboard")
        # label.setFont(label_font)
        # layout.addWidget(label)

        help_button = QPushButton("Help")
        help_button.setToolTip(
            "Press Log to store your clipboard data\nPress Clear to clear the list\nPress Exit to close the clipboard"
        )
        help_button.clicked.connect(self.show_help)

        log_button = QPushButton("Log")
        log_button.clicked.connect(self.log_clipboard)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_clip_list)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(help_button)
        button_layout.addWidget(log_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(exit_button)

        # Create a checkbox for theme selection
        theme_checkbox = QCheckBox("Dark Theme")
        theme_checkbox.setChecked(True)
        theme_checkbox.stateChanged.connect(self.switch_theme)

        button_layout.addWidget(theme_checkbox)

        layout.addLayout(button_layout)
        layout.addWidget(self.notice)

        self.clip_list_widget = QListWidget()
        self.clip_list_widget.addItems(self.clipList)
        self.clip_list_widget.currentItemChanged.connect(self.copy_item)
        layout.addWidget(self.clip_list_widget)

        self.setLayout(layout)

        self.set_theme("dark")  # Set the initial theme to dark

    def load_last_10_logs(self):
        now = datetime.datetime.now()
        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = f"logs/clipboard_{today}.txt"
        logs = []

        if os.path.isfile(filename):
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        log_parts = line.split(" - ")
                        if len(log_parts) == 2:
                            log_timestamp = log_parts[0]
                            log_value = log_parts[1]
                            try:
                                log_datetime = datetime.datetime.strptime(
                                    log_timestamp, "%Y-%m-%d %H:%M:%S.%f"
                                )
                                if (
                                    log_datetime.date() == now.date()
                                    and log_datetime <= now
                                ):
                                    logs.append(line)
                            except ValueError:
                                pass

        last_10_logs = logs[-10:] if len(logs) >= 10 else logs
        return last_10_logs if logs else ["empty"]

    def update_clip_list(self, value):
        if "\n" in value:
            value = value.replace("\n", " ")

        self.clipList.insert(0, value)
        self.clip_list_widget.clear()
        self.clip_list_widget.addItems(
            self.clipList[:10]
        )  # Keep only the last 10 entries
        self.clip_list_widget.setCurrentRow(0)  # Set the current row to the first item

    def clear_clip_list(self):
        self.clipList = ["empty"]
        self.update_clip_list("empty")

    def log_clipboard(self):
        value = clipboard.paste()
        self.update_clip_list(value)
        self.save_to_file(value)

    def save_to_file(self, value):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = f"logs/clipboard_{today}.txt"
        with open(filename, "a") as file:
            file.write(f"{datetime.datetime.now()} - {value}\n")

    def copy_item(self, item):
        if item:
            self.notice.setText("Copied")
            clipboard.copy(item.text())

    def show_help(self):
        QMessageBox.information(
            self,
            "Help",
            "Press Log to store your clipboard data\nPress Clear to clear the list\nPress Exit to close the clipboard",
        )

    def switch_theme(self, checked):
        if checked:
            self.set_theme("dark")
        else:
            self.set_theme("light")

    def set_theme(self, theme):
        if theme == "dark":
            app.setStyle("Fusion")
            palette = app.palette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
        elif theme == "light":
            app.setStyle("Fusion")
            palette = app.palette()
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            app.setPalette(palette)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardApp()
    window.show()
    sys.exit(app.exec_())
