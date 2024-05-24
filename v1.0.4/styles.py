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

/* Styling for QLineEdit, QTextEdit, QListWidget */
QLineEdit, QTextEdit, QListWidget {
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
"""
