STYLESHEET = """
/* General Styling */
QWidget {
    background-color: #212121;
    font-family: Arial, sans-serif;
}

/* QLabel Styling */
QLabel {
    color: #f5f6fa;
    font-size: 16px;
}

QLabel#edit_prompt_title_label {
    color: #ffffff;
}

/* QLineEdit Styling */
QLineEdit {
    color: #39ff14; /* Light green font color */
}

QLineEdit#prompt_input {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 5px;
    margin-left: 13px;
    color: #ff5733; /* Override light green font color with specific color for this input */
}

QLineEdit#title_input {
    color: #ffffff;
}

QLineEdit#search_input {
    background-color: #212121;
    border: 1px solid #ffffff;
    border-radius: 5px;
    padding: 5px;
    color: #43f76d; /* Override light green font color with specific color for this input */
}

/* QTextEdit and QListWidget Styling */
QTextEdit, QListWidget {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 5px;
}

/* QPushButton Styling */
QPushButton {
    background-color: #05c46b;
    border: none;
    color: #f5f6fa;
    padding: 8px 16px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3e8e41;
}

/* QDialog Styling */
QDialog {
    background-color: #3e54bc;
}

QDialog#EditPromptDialog, QDialog#DeletePromptDialog, QDialog#AddPromptDialog {
    background-color: #3e54bc;
    border-radius: 5px;
}

QDialog#AddPromptDialog QLineEdit {
    color: #ffffff;
}

/* QMenuBar Styling */
QMenuBar {
    background-color: #333333;
    color: #ffffff;
}

QMenuBar::item {
    background-color: #333333;
    color: #ffffff;
    padding: 5px 10px;
}

QMenuBar::item:selected {
    background-color: #555555;
}

/* QMenu Styling */
QMenu {
    background-color: #090909;
    color: #f5f6fa;
    border: 1px solid #cccccc;
    border-radius: 5px;
}

QMenu::item {
    padding: 5px 20px;
}

QMenu::item:selected {
    background-color: #7a7a7a;
}


"""
