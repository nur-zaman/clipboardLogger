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
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore
import clipboard


class ClipboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.clipList = self.load_last_10_logs()  # Load last 10 logs on app start

        self.notice = QLabel("Click an item to copy")

        self.setWindowTitle("Clipboard")
        self.setWindowIcon(QIcon("clipboard.ico"))
        self.setMinimumSize(200, 300)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        label_font = QFont("Arial", 18)
        label = QLabel("Clipboard")
        label.setFont(label_font)
        layout.addWidget(label)

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

        layout.addLayout(button_layout)
        layout.addWidget(self.notice)

        self.clip_list_widget = QListWidget()
        self.clip_list_widget.addItems(self.clipList)
        self.clip_list_widget.currentItemChanged.connect(self.copy_item)
        layout.addWidget(self.clip_list_widget)

        self.setLayout(layout)

    def load_last_10_logs(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = f"logs/clipboard_{today}.txt"

        if os.path.isfile(filename):
            with open(filename, "r") as file:
                lines = file.readlines()
                last_10_logs = [line.strip() for line in lines[-10:]]
                return last_10_logs

        return ["empty"]

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardApp()
    window.show()
    sys.exit(app.exec_())
