import sqlite3
import sys

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


class AddPromptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Prompt")
        self.layout = QVBoxLayout()
        self.prompt_label = QLabel("Enter Prompt Title:")
        self.prompt_input = QLineEdit()
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.prompt_input)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_prompt_title(self):
        if self.exec_() == QDialog.Accepted:
            return self.prompt_input.text()
        return None


class CopyPromptDialog(QDialog):
    def __init__(self, prompt_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Copy Prompt")
        self.layout = QVBoxLayout()
        self.prompt_label = QLabel(
            "The following prompt has been copied:\n\n''" + prompt_text + "''"
        )
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttons.accepted.connect(self.accept)
        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)


class DeletePromptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Prompt")
        self.layout = QVBoxLayout()
        self.prompt_label = QLabel("Are you sure you want to delete the selected prompt?")
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)


class PromptManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_connection()
        self.create_table()

    def initUI(self):
        self.setWindowTitle("Promptiverse")
        self.setGeometry(100, 100, 600, 400)

        self.prompt_label = QLabel("Enter Prompt:")
        self.prompt_input = QLineEdit()
        self.add_button = QPushButton("Add Prompt")
        self.add_button.clicked.connect(self.add_prompt)

        self.show_button = QPushButton("Show Prompts")
        self.show_button.clicked.connect(self.load_prompts)

        self.search_label = QLabel("Search Prompt:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_prompt)

        self.prompt_list = QListWidget()
        self.prompt_list.itemDoubleClicked.connect(self.display_prompt)

        self.copy_button = QPushButton("Copy Prompt")
        self.copy_button.clicked.connect(self.copy_prompt)

        self.delete_button = QPushButton("Delete Prompt")
        self.delete_button.clicked.connect(self.delete_prompt)

        self.prompt_display = QTextEdit()

        vbox = QVBoxLayout()
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
        vbox.addLayout(button_hbox)

        vbox.addWidget(self.prompt_display)

        self.setLayout(vbox)

    def create_connection(self):
        self.connection = sqlite3.connect("prompts.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS prompts (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            prompt TEXT)""")
        self.connection.commit()

    def add_prompt(self):
        dialog = AddPromptDialog(self)
        title = dialog.get_prompt_title()
        if title:
            prompt = self.prompt_input.text()
            if prompt:
                self.cursor.execute(
                    "INSERT INTO prompts (title, prompt) VALUES (?, ?)", (title, prompt)
                )
                self.connection.commit()
                self.prompt_input.clear()

    def load_prompts(self):
        self.prompt_list.clear()
        self.cursor.execute("SELECT title FROM prompts")
        prompts = self.cursor.fetchall()
        for prompt in prompts:
            self.prompt_list.addItem(prompt[0])

    def display_prompt(self, item):
        title = item.text()
        self.cursor.execute("SELECT prompt FROM prompts WHERE title=?", (title,))
        prompt = self.cursor.fetchone()
        if prompt:
            self.prompt_display.setPlainText(prompt[0])

    def copy_prompt(self):
        selected_items = self.prompt_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No prompt selected to copy.")
            return
        prompt_text = self.prompt_display.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(prompt_text)
        dialog = CopyPromptDialog(prompt_text, self)
        dialog.exec_()

    def delete_prompt(self):
        selected_items = self.prompt_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No prompt selected for deletion.")
            return
        dialog = DeletePromptDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            for item in selected_items:
                title = item.text()
                self.cursor.execute("DELETE FROM prompts WHERE title=?", (title,))
                self.connection.commit()
                self.prompt_list.takeItem(self.prompt_list.row(item))

    def search_prompt(self):
        search_text = self.search_input.text()
        if not search_text:
            self.load_prompts()
            return
        self.prompt_list.clear()
        self.cursor.execute(
            "SELECT title FROM prompts WHERE title LIKE ?", ("%" + search_text + "%",)
        )
        prompts = self.cursor.fetchall()
        for prompt in prompts:
            self.prompt_list.addItem(prompt[0])

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptManager()
    window.show()
    sys.exit(app.exec_())
