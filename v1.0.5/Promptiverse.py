import sqlite3
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from styles import STYLESHEET  # Import the styles from styles.py


class AddPromptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AddPromptDialog")  # Apply object name
        self.setWindowTitle("Add Prompt")
        self.layout = QVBoxLayout(self)
        self.prompt_label = QLabel("Enter Prompt Title:")
        self.prompt_input = QLineEdit()
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.prompt_input)
        self.layout.addWidget(self.buttons)

    def get_prompt_title(self):
        if self.exec_() == QDialog.Accepted:
            return self.prompt_input.text()
        return None


class CopyPromptDialog(QDialog):
    def __init__(self, prompt_text, parent=None):
        super().__init__(parent)
        self.setObjectName("CopyPromptDialog")  # Apply object name
        self.setWindowTitle("Copy Prompt")
        self.layout = QVBoxLayout(self)
        self.prompt_label = QLabel(f"The following prompt has been copied:\n\n''{prompt_text}''")
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttons.accepted.connect(self.accept)
        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.buttons)


class DeletePromptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DeletePromptDialog")  # Apply object name
        self.setWindowTitle("Delete Prompt")
        self.layout = QVBoxLayout(self)
        self.prompt_label = QLabel("Are you sure you want to delete the selected prompt?")
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.buttons)


class PromptManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_connection()
        self.create_table()
        self.update_statistics()  # Initialize statistics
        self.prompt_changed.connect(self.update_statistics)  # Connect signal to update method

    def initUI(self):
        self.setWindowTitle("Promptiverse")
        self.setGeometry(100, 100, 800, 600)  # Adjusted window size
        self.setWindowIcon(QIcon("../Images/promptiverse_window.png"))
        self.setStyleSheet(STYLESHEET)  # Apply styles from styles.py

        self.prompt_label = QLabel("Enter Prompt:")
        self.prompt_input = QLineEdit()
        self.prompt_input.setObjectName("prompt_input")  # Set object name for prompt input
        self.add_button = QPushButton("Add Prompt")
        self.add_button.clicked.connect(self.add_prompt)

        self.show_button = QPushButton("Show Prompts")
        self.show_button.clicked.connect(self.load_prompts)

        self.search_label = QLabel("Search Prompt:")
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")  # Set object name for search input
        self.search_input.textChanged.connect(self.search_prompt)

        self.prompt_list = QListWidget()
        self.prompt_list.itemDoubleClicked.connect(self.display_prompt)

        self.copy_button = QPushButton("Copy Prompt")
        self.copy_button.clicked.connect(self.copy_prompt)

        self.delete_button = QPushButton("Delete Prompt")
        self.delete_button.clicked.connect(self.delete_prompt)

        self.clear_display_button = QPushButton("Clear Display")
        self.clear_display_button.clicked.connect(self.clear_display)

        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.prompt_label)
        hbox.addWidget(self.prompt_input)
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.show_button)
        vbox.addLayout(hbox)

        search_hbox = QHBoxLayout()
        search_hbox.addWidget(self.search_label)
        search_hbox.addWidget(self.search_input)
        vbox.addLayout(search_hbox)

        vbox.addWidget(self.prompt_list)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.copy_button)
        button_hbox.addWidget(self.delete_button)
        button_hbox.addWidget(self.clear_display_button)
        vbox.addLayout(button_hbox)

        self.prompt_display = QTextEdit()
        vbox.addWidget(self.prompt_display)

        # Statistics label
        self.statistics_label = QLabel()
        vbox.addWidget(self.statistics_label)

    # Define a custom signal for prompt changes
    prompt_changed = pyqtSignal()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect("prompts.db")
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to connect to database: {e}")

    def create_table(self):
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS prompts (
                                id INTEGER PRIMARY KEY,
                                title TEXT,
                                prompt TEXT)""")
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to create table: {e}")

    def update_statistics(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM prompts")
            total_prompts = self.cursor.fetchone()[0]
            self.statistics_label.setText(f"Total Prompts: {total_prompts}")
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to fetch statistics: {e}")

    def add_prompt(self):
        dialog = AddPromptDialog(self)
        title = dialog.get_prompt_title()
        if title:
            prompt_text = self.prompt_input.text()
            if prompt_text:
                try:
                    self.cursor.execute(
                        "INSERT INTO prompts (title, prompt) VALUES (?, ?)",
                        (title, prompt_text),
                    )
                    self.connection.commit()
                    self.prompt_input.clear()
                    self.prompt_changed.emit()  # Emit signal after adding prompt
                except sqlite3.Error as e:
                    self.show_error_message(f"Failed to add prompt: {e}")

    def load_prompts(self):
        try:
            self.prompt_list.clear()
            self.cursor.execute("SELECT title FROM prompts")
            prompts = self.cursor.fetchall()
            for prompt in prompts:
                self.prompt_list.addItem(prompt[0])
            self.prompt_changed.emit()  # Emit signal after loading prompts
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to load prompts: {e}")

    def display_prompt(self, item):
        try:
            title = item.text()
            self.cursor.execute("SELECT prompt FROM prompts WHERE title=?", (title,))
            prompt = self.cursor.fetchone()
            if prompt:
                self.prompt_display.setPlainText(prompt[0])
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to display prompt: {e}")

    def copy_prompt(self):
        try:
            selected_items = self.prompt_list.selectedItems()
            if not selected_items:
                self.show_warning_message("No prompt selected to copy.")
                return
            prompt_text = self.prompt_display.toPlainText()
            clipboard = QApplication.clipboard()
            clipboard.setText(prompt_text)
            dialog = CopyPromptDialog(prompt_text, self)
            dialog.exec_()
        except Exception as e:
            self.show_error_message(f"Failed to copy prompt: {e}")

    def delete_prompt(self):
        try:
            selected_items = self.prompt_list.selectedItems()
            if not selected_items:
                self.show_warning_message("No prompt selected for deletion.")
                return
            dialog = DeletePromptDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                for item in selected_items:
                    title = item.text()
                    self.cursor.execute("DELETE FROM prompts WHERE title=?", (title,))
                    self.connection.commit()
                    self.prompt_list.takeItem(self.prompt_list.row(item))
                self.prompt_changed.emit()  # Emit signal after deleting prompt
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to delete prompt: {e}")

    def clear_display(self):
        self.prompt_display.clear()

    def search_prompt(self):
        try:
            search_text = self.search_input.text()
            if not search_text:
                self.load_prompts()
                return
            self.prompt_list.clear()
            self.cursor.execute(
                "SELECT title FROM prompts WHERE title LIKE ?",
                ("%" + search_text + "%",),
            )
            prompts = self.cursor.fetchall()
            for prompt in prompts:
                self.prompt_list.addItem(prompt[0])
            self.prompt_changed.emit()  # Emit signal after searching prompts
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to search prompt: {e}")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_warning_message(self, message):
        QMessageBox.warning(self, "Warning", message)

    def closeEvent(self, event):
        try:
            self.connection.close()
            event.accept()
        except Exception as e:
            self.show_error_message(f"Failed to close database connection: {e}")
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptManager()
    window.show()
    sys.exit(app.exec_())
