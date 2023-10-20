import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QTextEdit
from PySide2.QtCore import QTimer
from PySide2.QtGui import QTextCursor, QTextCharFormat, QFont

indent = '  '
refresh_rate_ms = 500

class MarkdownCompilerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_output)
        self.timer.start(refresh_rate_ms)  # Set the update interval in milliseconds (1 second in this case)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()  # Use QHBoxLayout for side-by-side widgets

        # Text Input
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        # Text Output
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        central_widget.setLayout(layout)

        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("_transientlab_md")
        self.show()

    def update_output(self):
        # Clear the text_output widget
        self.text_output.clear()

        # Get the input text from the text input widget
        input_text = self.text_input.toPlainText()

        # Initialize the transformed text
        transformed_text = ""

        # Split input text into lines
        lines = input_text.split('\n')

        # Iterate through the lines
        for line in lines:
            char_format = QTextCharFormat()
            font = char_format.font()

            if line.startswith('# '):
                font_size = 20
                font.setBold(True)
                line_text = line[2:]

            elif line.startswith('## '):
                font_size = 18
                font.setBold(True)
                line_text = indent + line[3:]

            elif line.startswith('### '):
                font_size = 16
                font.setBold(True)
                line_text = line[4:]

            elif line.startswith('#### '):
                font_size = 14
                font.setBold(True)
                line_text = line[5:]

            elif line.startswith('\n'):
                line_text = '\n'                                                                                                
            else:
                line_text = line
                font_size = 12

            # Create a QTextCharFormat with the desired font size

            font.setPointSize(font_size)

            # Apply the format to the line
            char_format.setFont(font)
            cursor = QTextCursor(self.text_output.document())
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(line_text, char_format)

            # Add a line break to separate lines
            cursor.insertText("\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarkdownCompilerApp()
    sys.exit(app.exec_())
