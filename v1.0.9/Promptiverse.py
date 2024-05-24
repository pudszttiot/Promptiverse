import sqlite3
import sys

from menu_bar_template import HelpDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from styles import STYLESHEET


class AddPromptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Prompt")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Enter Prompt Title:"))
        self.prompt_input = QLineEdit()
        layout.addWidget(self.prompt_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_prompt_title(self):
        if self.exec_() == QDialog.Accepted:
            return self.prompt_input.text()
        return None


class CopyPromptDialog(QDialog):
    def __init__(self, prompt_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Copy Prompt")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"The following prompt has been copied:\n\n''{prompt_text}''"))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


class DeletePromptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Prompt")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Are you sure you want to delete the selected prompt?"))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class EditPromptDialog(QDialog):
    delete_prompt_signal = pyqtSignal(str)  # Signal to indicate prompt deletion

    def __init__(self, prompt_title, prompt_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Prompt")
        layout = QVBoxLayout(self)

        title_label = QLabel("Edit Prompt Title:")
        title_label.setObjectName("edit_prompt_title_label")  # Set the object name
        self.title_input = QLineEdit()
        self.title_input.setText(prompt_title)
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)

        prompt_label = QLabel("Edit Prompt Text:")
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlainText(prompt_text)
        layout.addWidget(prompt_label)
        layout.addWidget(self.prompt_input)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_prompt)
        layout.addWidget(delete_button)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_edited_prompt(self):
        if self.exec_() == QDialog.Accepted:
            return self.title_input.text(), self.prompt_input.toPlainText()
        return None, None

    def delete_prompt(self):
        confirm_dialog = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete the selected prompt?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm_dialog == QMessageBox.Yes:
            title = self.title_input.text()
            self.delete_prompt_signal.emit(title)  # Emit signal with title for deletion


class PromptManager(QWidget):
    prompt_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_connection()
        self.create_table()
        self.update_statistics()
        self.prompt_changed.connect(self.update_statistics)

    def initUI(self):
        self.setWindowTitle("Promptiverse")
        self.setWindowIcon(QIcon("../Images/promptiverse_window.png"))
        self.setStyleSheet(STYLESHEET)

        layout = QGridLayout(self)

        input_section = QVBoxLayout()
        layout.addLayout(input_section, 0, 0, 1, 1)
        input_section.addWidget(QLabel("Enter Prompt:"))
        self.prompt_input = QTextEdit()
        self.prompt_input.setMinimumHeight(100)
        self.prompt_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        input_section.addWidget(self.prompt_input)

        action_buttons = QHBoxLayout()
        layout.addLayout(action_buttons, 1, 0, 1, 1)
        self.add_button = QPushButton(QIcon("../Images/Add_Prompt.png"), "Add Prompt")
        self.show_button = QPushButton(QIcon("../Images/Show_Prompt.png"), "Show Prompts")
        self.edit_button = QPushButton(QIcon("../Images/Edit_Prompt.png"), "Edit Prompt")
        action_buttons.addWidget(self.add_button)
        action_buttons.addWidget(self.show_button)
        action_buttons.addWidget(self.edit_button)

        search_section = QHBoxLayout()
        layout.addLayout(search_section, 2, 0, 1, 1)
        search_section.addWidget(QLabel("Search Prompt:"))
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("color: #43f76d;")

        self.search_input.textChanged.connect(self.filter_prompts)
        search_section.addWidget(self.search_input)

        self.prompt_list = QListWidget()
        layout.addWidget(self.prompt_list, 0, 1, 3, 1)

        self.prompt_display = QTextEdit()
        layout.addWidget(self.prompt_display, 3, 0, 1, 2)

        self.clear_button_display = QPushButton(QIcon("../Images/Clear_Clean.png"), "Clear Display")
        layout.addWidget(self.clear_button_display, 4, 0, 1, 2)

        self.statistics_label = QLabel()
        layout.addWidget(self.statistics_label, 5, 0, 1, 2)

        self.add_button.clicked.connect(self.add_prompt)
        self.show_button.clicked.connect(self.load_prompts)
        self.edit_button.clicked.connect(self.edit_selected_prompt)
        self.clear_button_display.clicked.connect(self.clear_display)
        self.prompt_list.itemDoubleClicked.connect(self.display_selected_prompt)

        self.prompt_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.prompt_list.customContextMenuRequested.connect(self.show_context_menu)

    def clear_display(self):
        self.prompt_display.clear()

    def show_context_menu(self, position):
        context_menu = QMenu()
        edit_action = QAction(QIcon("../Images/Edit_Context_2.png"), "Edit", self)
        copy_action = QAction(QIcon("../Images/Copy_Context.png"), "Copy", self)
        context_menu.addAction(edit_action)
        context_menu.addAction(copy_action)
        edit_action.triggered.connect(self.edit_selected_prompt)
        copy_action.triggered.connect(self.copy_selected_prompt)
        context_menu.exec_(self.prompt_list.mapToGlobal(position))

    def edit_selected_prompt(self):
        selected_items = self.prompt_list.selectedItems()
        if not selected_items:
            self.show_warning_message("No prompt selected to edit.")
            return
        title = selected_items[0].text()
        try:
            self.cursor.execute("SELECT title, prompt FROM prompts WHERE title=?", (title,))
            prompt_title, prompt_text = self.cursor.fetchone()
            dialog = EditPromptDialog(prompt_title, prompt_text, self)
            dialog.delete_prompt_signal.connect(self.delete_prompt_from_db)  # Connect signal
            edited_title, edited_prompt = dialog.get_edited_prompt()
            if edited_title is not None and edited_prompt is not None:
                if edited_title or edited_prompt:
                    self.cursor.execute(
                        "UPDATE prompts SET title=?, prompt=? WHERE title=?",
                        (edited_title, edited_prompt, title),
                    )
                    self.connection.commit()
                else:
                    self.delete_prompt_from_db(title)  # Delete prompt if both fields are empty
                self.prompt_changed.emit()
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to edit prompt: {e}")

    def delete_prompt_from_db(self, title):
        try:
            self.cursor.execute("DELETE FROM prompts WHERE title=?", (title,))
            self.connection.commit()
            self.load_prompts()  # Reload prompts after deletion
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to delete prompt: {e}")

    def copy_selected_prompt(self):
        selected_items = self.prompt_list.selectedItems()
        if not selected_items:
            self.show_warning_message("No prompt selected to copy.")
            return
        title = selected_items[0].text()
        try:
            self.cursor.execute("SELECT prompt FROM prompts WHERE title=?", (title,))
            prompt_text = self.cursor.fetchone()[0]
            clipboard = QApplication.clipboard()
            clipboard.setText(prompt_text)
            dialog = CopyPromptDialog(prompt_text, self)
            dialog.exec_()
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to copy prompt: {e}")

    def display_selected_prompt(self, item):
        title = item.text()
        try:
            self.cursor.execute("SELECT prompt FROM prompts WHERE title=?", (title,))
            prompt_text = self.cursor.fetchone()[0]
            self.prompt_display.setPlainText(prompt_text)
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to display prompt: {e}")

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
                    self.prompt_changed.emit()
                except sqlite3.Error as e:
                    self.show_error_message(f"Failed to add prompt: {e}")

    def load_prompts(self):
        try:
            self.prompt_list.clear()
            self.cursor.execute("SELECT title FROM prompts")
            prompts = self.cursor.fetchall()
            for prompt in prompts:
                self.prompt_list.addItem(prompt[0])
            self.prompt_changed.emit()
        except sqlite3.Error as e:
            self.show_error_message(f"Failed to load prompts: {e}")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_warning_message(self, message):
        QMessageBox.warning(self, "Warning", message)


class PromptManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Promptiverse")
        self.setWindowIcon(QIcon("../Images/promptiverse_window.png"))
        self.setStyleSheet(STYLESHEET)
        self.setGeometry(400, 100, 1214, 872)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.prompt_manager = PromptManager()
        layout.addWidget(self.prompt_manager)

        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu("Edit")
        undo_action = edit_menu.addAction("Undo")
        undo_action.triggered.connect(self.prompt_manager.prompt_input.undo)
        redo_action = edit_menu.addAction("Redo")
        redo_action.triggered.connect(self.prompt_manager.prompt_input.redo)
        cut_action = edit_menu.addAction("Cut")
        cut_action.triggered.connect(self.prompt_manager.prompt_input.cut)
        copy_action = edit_menu.addAction("Copy")
        copy_action.triggered.connect(self.prompt_manager.prompt_input.copy)
        paste_action = edit_menu.addAction("Paste")
        paste_action.triggered.connect(self.prompt_manager.prompt_input.paste)

        view_menu = menubar.addMenu("View")
        fullscreen_action = view_menu.addAction("Fullscreen")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        minimize_action = view_menu.addAction("Minimize")
        minimize_action.triggered.connect(self.minimize_window)

        help_menu = menubar.addMenu("Help")
        help_action = QAction("How To Use...", self)
        help_action.triggered.connect(self.open_help_dialog)
        help_menu.addAction(help_action)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def minimize_window(self):
        self.showMinimized()

    def open_help_dialog(self):
        dialog = HelpDialog()
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptManagerWindow()
    window.show()
    sys.exit(app.exec_())
