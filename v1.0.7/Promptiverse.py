import sqlite3
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
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
        layout = QVBoxLayout(self)
        prompt_label = QLabel("Enter Prompt Title:")
        self.prompt_input = QLineEdit()
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(buttons)

    def get_prompt_title(self):
        if self.exec_() == QDialog.Accepted:
            return self.prompt_input.text()
        return None


class CopyPromptDialog(QDialog):
    def __init__(self, prompt_text, parent=None):
        super().__init__(parent)
        self.setObjectName("CopyPromptDialog")  # Apply object name
        self.setWindowTitle("Copy Prompt")
        layout = QVBoxLayout(self)
        prompt_label = QLabel(f"The following prompt has been copied:\n\n''{prompt_text}''")
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(prompt_label)
        layout.addWidget(buttons)


class DeletePromptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DeletePromptDialog")  # Apply object name
        self.setWindowTitle("Delete Prompt")
        layout = QVBoxLayout(self)
        prompt_label = QLabel("Are you sure you want to delete the selected prompt?")
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(prompt_label)
        layout.addWidget(buttons)


class EditPromptDialog(QDialog):
    def __init__(self, prompt_title, prompt_text, parent=None):
        super().__init__(parent)
        self.setObjectName("EditPromptDialog")  # Add this line to set the object name
        self.setWindowTitle("Edit Prompt")
        layout = QVBoxLayout(self)

        # Prompt Title Section
        title_label = QLabel("Edit Prompt Title:")
        self.title_input = QLineEdit()
        self.title_input.setObjectName("title_input")  # Add this line to set the object name
        self.title_input.setText(prompt_title)
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)

        # Prompt Text Section
        prompt_label = QLabel("Edit Prompt Text:")
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlainText(prompt_text)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(buttons)

    def get_edited_prompt(self):
        if self.exec_() == QDialog.Accepted:
            return self.title_input.text(), self.prompt_input.toPlainText()
        return None, None


class PromptManager(QWidget):
    # Define a custom signal for prompt changes
    prompt_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_connection()
        self.create_table()
        self.update_statistics()  # Initialize statistics
        self.prompt_changed.connect(self.update_statistics)  # Connect signal to update method

    def initUI(self):
        self.setWindowTitle("Promptiverse")
        self.setWindowIcon(QIcon("../Images/promptiverse_window.png"))
        self.setStyleSheet(STYLESHEET)  # Apply styles from styles.py

        # Create Grid Layout for Main Window
        layout = QGridLayout(self)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnMinimumWidth(0, 200)

        # Input Section
        input_section = QVBoxLayout()
        layout.addLayout(input_section, 0, 0, 1, 1)
        prompt_label = QLabel("Enter Prompt:")
        input_section.addWidget(prompt_label)
        self.prompt_input = QTextEdit()
        self.prompt_input.setMinimumHeight(100)
        self.prompt_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        input_section.addWidget(self.prompt_input)

        # Action Buttons
        action_buttons = QHBoxLayout()
        layout.addLayout(action_buttons, 1, 0, 1, 1)
        self.add_button = QPushButton("Add Prompt")
        self.show_button = QPushButton("Show Prompts")
        self.edit_button = QPushButton("Edit Prompt")
        action_buttons.addWidget(self.add_button)
        action_buttons.addWidget(self.show_button)
        action_buttons.addWidget(self.edit_button)

        # Search Section
        search_section = QHBoxLayout()
        layout.addLayout(search_section, 2, 0, 1, 1)
        search_label = QLabel("Search Prompt:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_prompts)  # Connect textChanged signal
        self.search_input.setObjectName("search_input")  # Set object name
        search_section.addWidget(search_label)
        search_section.addWidget(self.search_input)

        # Prompt List
        self.prompt_list = QListWidget()
        layout.addWidget(self.prompt_list, 0, 1, 3, 1)

        # Display Section
        self.prompt_display = QTextEdit()
        layout.addWidget(self.prompt_display, 3, 0, 1, 2)

        # Statistics Section
        self.statistics_label = QLabel()
        layout.addWidget(self.statistics_label, 4, 0, 1, 2)

        # Action Button Connections
        self.add_button.clicked.connect(self.add_prompt)
        self.show_button.clicked.connect(self.load_prompts)
        self.edit_button.clicked.connect(self.edit_prompt)

        # Connect double-click event to display prompt
        self.prompt_list.itemDoubleClicked.connect(self.display_selected_prompt)

    # Add this method to display the selected prompt
    def display_selected_prompt(self, item):
        title = item.text()
        try:
            self.cursor.execute("SELECT prompt FROM prompts WHERE title=?", (title,))
            prompt_text = self.cursor.fetchone()[0]
            self.prompt_display.setPlainText(prompt_text)
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to display prompt: {e}")

    # Add this method to filter prompts based on search input
    def filter_prompts(self, text):
        text = text.strip()
        self.prompt_list.clear()
        if not text:
            self.load_prompts()
            return
        try:
            self.cursor.execute("SELECT title FROM prompts WHERE title LIKE ?", ("%" + text + "%",))
            prompts = self.cursor.fetchall()
            for prompt in prompts:
                self.prompt_list.addItem(prompt[0])
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to filter prompts: {e}")

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
            prompt_text = self.prompt_input.toPlainText()
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

    def edit_prompt(self):
        selected_items = self.prompt_list.selectedItems()
        if not selected_items:
            self.show_warning_message("No prompt selected to edit.")
            return
        title = selected_items[0].text()
        try:
            self.cursor.execute("SELECT title, prompt FROM prompts WHERE title=?", (title,))
            prompt_title, prompt_text = self.cursor.fetchone()
            dialog = EditPromptDialog(prompt_title, prompt_text, self)
            edited_title, edited_prompt = dialog.get_edited_prompt()
            if edited_title and edited_prompt:
                self.cursor.execute(
                    "UPDATE prompts SET title=?, prompt=? WHERE title=?",
                    (edited_title, edited_prompt, title),
                )
                self.connection.commit()
                self.prompt_changed.emit()  # Emit signal after editing prompt
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to edit prompt: {e}")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_warning_message(self, message):
        QMessageBox.warning(self, "Warning", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptManager()
    window.show()
    sys.exit(app.exec_())
