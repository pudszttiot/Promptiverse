import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QScrollArea, QVBoxLayout


class HelpDialog(QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()
        self.setWindowTitle("How to Use...")
        self.setGeometry(550, 350, 800, 600)
        self.setWindowIcon(QIcon("../Images/promptiverse_window.png"))  # Corrected path

        help_text = r"""
            <p style="text-align: center;">
            <h2><span style="color: #00FF00;">===================================</span></h2>
            <h1><span style="color: #F5F5F5;">🛠 PROMPTIVERSE 🛠</span></h1>
            <h2><span style="color: #FFFFFF;">📝 Version: 1.0.9</span></h2>
            <h2><span style="color: #FFFFFF;">📅 Release Date: May 16, 2024</span></h2>
            <h2><span style="color: #00FF00;">===================================</span></h2></p>
        
            <p style="text-align: center;">
            <span style="color: #282c34; background-color: yellow;">
            Discover <strong><span style="color: #000000; background-color: yellow;">"Promptiverse"</span></strong>
            a friendly app for managing prompts!
            <br>It simplifies adding, editing, and organizing prompts with easy-to-use buttons and lists.
            <br>Get ready to unleash your creativity with Promptiverse!
            </span></p>

            <p><h3><span style="color: #FF0080;">Here's how to use it:</span></h3></p>
            <ol>
            <ul>
                <li><u>Adding a Prompt:</u>
            <ul>
                <li>Enter the prompt text in the text input area.</li>
                <li>Click the <strong><span style="color: #FF6600;">"Add Prompt"</span></strong> button.</li>
                <li>A dialog will prompt you to enter the title for the prompt. Enter the title and click <strong><span style="color: #FF6600;">"OK"</span></strong></li>
                <li>The prompt will be added to the database, and the prompt list will be updated.</li>

            </ul>
            </li>
            <br>
                <li><u>Showing Existing Prompts:</u>
            <ul>
                <li>Click the <strong><span style="color: #FF6600;">"Show Prompts"</span></strong> button.</li>
                <li>The list of existing prompts will be displayed in the prompt list on the right-hand side.</li>
            </ul>
            </li>
            <br>
                <li><u>Editing a Prompt:</u>
            <ul>
                <li>Select a prompt from the prompt list.</li>
                <li>Click the <strong><span style="color: #FF6600;">"Edit Prompt"</span></strong> button.</li>
                <li>A dialog will appear with the selected prompt's title and text.</li>
                <li>Modify the title and/or text as desired.</li>
                <li>Click <strong><span style="color: #FF6600;">"OK"</span></strong> to save the changes or <strong><span style="color: #FF6600;">"Cancel"</span></strong> to discard them.</li>
                <li>If you click <strong><span style="color: #FF6600;">"Delete"</span></strong> within the dialog, the prompt will be deleted after confirmation.</li>

            </ol>
            
            

            <p style="font-size: 20px; font-family: doergon, sans-serif; text-align: center;"><span style="color: #030303; background-color:#f5f5f5;">That's it!... Thank you for using <strong><span style="color: #94c7f7;">Promptiverse!</span></strong></span></p>

            <p style="text-align: center;"><img src="..\Images\promptiverse_window.png" alt="WindowLogo.png" width="250" height="200" border="1">

            <h6 style="color: #e8eaea;">▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃</h6>

            <h3><span style="color: #39ff14; background-color: #000000;">╬╬══▲▲▲👽👽 <u>MY CHANNELS</u> 👽👽▲▲▲══╬╬</span></h3></p>
            <br>
            <br>

            <span>
            <img src="../Socials/Github.png" alt="Github.png" width="30" height="30" border="2">
            <a href="https://github.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#e8eaea; margin-right:20px;" onclick="openLink('https://github.com/pudszttiot')">Github Page</a>
            </span> 

            <span>
            <img src="../Socials/Youtube.png" alt="Youtube.png" width="30" height="30" border="2">
            <a href="https://youtube.com/@pudszTTIOT" style="display:inline-block; text-decoration:none; color:#ff0000;" onclick="openLink('https://youtube.com/@pudszTTIOT')">YouTube Page</a>
            </span>

            <span>
            <img src="../Socials/SourceForge.png" alt="SourceForge.png" width="30" height="30" border="2">
            <a href="https://sourceforge.net/u/pudszttiot" style="display:inline-block; text-decoration:none; color:#ee730a;" onclick="openLink('https://sourceforge.net/u/pudszttiot')">SourceForge Page</a>
            </span>
        
            <span>
            <img src="../Socials/Dailymotion.png" alt="Dailymotion.png" width="30" height="30" border="2">
            <a href="https://dailymotion.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#0062ff;" onclick="openLink('https://dailymotion.com/pudszttiot')">Dailymotion Page</a>
            </span>

            <span>
            <img src="../Socials/Blogger.png" alt="Blogger.png" width="30" height="30" border="2">
            <a href="https://pudszttiot.blogspot.com" style="display:inline-block; text-decoration:none; color:#ff5722;" onclick="openLink('https://pudszttiot.blogspot.com')">Blogger Page</a>
            </span>

            <script>
            function openLink(url) {
                QDesktopServices.openUrl(QUrl(url));
            }
            </script>
        """

        help_label = QLabel()
        help_label.setAlignment(Qt.AlignLeft)
        help_label.setText(help_text)
        help_label.setOpenExternalLinks(True)  # Allow QLabel to open external links

        # Add a CSS background color
        help_label.setStyleSheet(
            "color: #1E90FF; background-color: #333333; padding: 10px;"
            "border: 2px solid #1E90FF; border-radius: 10px;"
        )

        # Create a scroll area for the help text
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(help_label)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)  # Add scroll area instead of help_label
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = HelpDialog()
    dialog.exec_()
    sys.exit(app.exec_())
