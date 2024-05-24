STYLESHEET = """
/* Styling for the main window (QWidget with empty object name) */
QWidget {
    background-color: #212121;
    font-family: Arial, sans-serif;
}

/* Styling for QLabel */
QLabel {
    color: #f5f6fa;
    font-size: 16px; /* Increase font size */
}

/* Styling for QLineEdit with object name "prompt_input" */
QLineEdit#prompt_input {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 5px; /* Adjust padding for size */
    margin-left: 13px; /* Adjust margin to move the input box position to the right */
}

/* Styling for QLineEdit with object name "title_input" */
QLineEdit#title_input {
    color: #39ff14; /* Set font color to the desired color */
}

/* Styling for QLineEdit with object name "search_input" */
QLineEdit#search_input {
    background-color: #212121;
    border: 1px solid #ffffff;
    border-radius: 5px;
    padding: 5px; /* Adjust padding for size */
    color: #39ff14; /* Set font color to black */
}

/* Styling for QTextEdit, QListWidget */
QTextEdit, QListWidget {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 5px;
}

/* Styling for QPushButton */
QPushButton {
    background-color: #05c46b; /* Green */
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

/* Styling for QPushButton when hovered */
QPushButton:hover {
    background-color: #45a049; /* Darker green */
}

/* Styling for QPushButton when pressed */
QPushButton:pressed {
    background-color: #3e8e41; /* Even darker green */
}

/* Styling for QDialog */
QDialog {
    background-color: #ffffff; /* White */
}

/* Styling for Edit Prompt Dialog */
QDialog#EditPromptDialog {
    background-color: #3e54bc; /* Blue */ /* Adjust background color as desired */
    border-radius: 5px;
}

/* Styling for Add Prompt Dialog */
QDialog#AddPromptDialog {
    background-color: #3e54bc; /* Blue */
    border-radius: 5px;
}

/* Styling for QLineEdit text color inside Add Prompt Dialog */
QDialog#AddPromptDialog QLineEdit {
    color: #ffffff; /* White */
}
"""
