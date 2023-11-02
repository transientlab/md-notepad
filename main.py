import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QListWidget, QPushButton, QFileDialog, QGridLayout, QCheckBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QTextCursor, QTextCharFormat



class md_notebook(QMainWindow):
    def __init__(self):
        super().__init__()

        self.indent = '  '
        self.refresh_rate_ms = 100
        self.notes_directory = os.getcwd()
        self.autosave = True
        self.file_path = 'new.md'


        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_output)
        self.timer.start(self.refresh_rate_ms)  # Set the update interval in milliseconds (1 second in this case)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()

        # Button to Select Directory
        select_directory_button = QPushButton("Select Directory")
        select_directory_button.clicked.connect(self.select_directory)
        grid_layout.addWidget(select_directory_button, 0, 0, 1, 1)  # Row 0, Column 0, Span 1 row, 1 column

        new_file_button = QPushButton("New File")
        new_file_button.clicked.connect(self.new_file)
        grid_layout.addWidget(new_file_button, 1, 0, 1, 1)  # Row 1, Column 0, Span 1 row, 1 column

        self.auto_save_checkbox = QCheckBox("Auto Save")
        self.auto_save_checkbox.setChecked(self.autosave)
        self.auto_save_checkbox.stateChanged.connect(self.toggle_auto_save)
        grid_layout.addWidget(self.auto_save_checkbox, 2, 0, 1, 1)  # Row 2, Column 0, Span 1 row, 1 column

        self.file_list_widget = QListWidget()
        self.file_list_widget.setFixedWidth(160)
        self.file_list_widget.itemSelectionChanged.connect(self.load_selected_file)
        grid_layout.addWidget(self.file_list_widget, 3, 0, 1, 1)  # Row 3, Column 0, Span 1 row, 1 column

        # Text Input
        self.text_input = QTextEdit()
        grid_layout.addWidget(self.text_input, 0, 1, 4, 1)  # Row 0, Column 1, Span 4 rows, 1 column

        # Text Output
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        grid_layout.addWidget(self.text_output, 0, 2, 4, 1)  # Row 0, Column 2, Span 4 rows, 1 column
        self.text_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        central_widget.setLayout(grid_layout)
        self.load_md_files()
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("_transientlab_md")
        self.show()

    def toggle_auto_save(self, state):
        global autosave
        autosave = bool(state)

    def load_md_files(self):
        self.file_list_widget.clear()
        directory = self.notes_directory
        for filename in os.listdir(directory):
            if filename.endswith('.md'):
                item = self.file_list_widget.addItem(filename)

    def load_selected_file(self):
        selected_item = self.file_list_widget.currentItem()
        self.text_input.clear()
        if selected_item is not None:
            directory = self.notes_directory
            self.file_path = os.path.join(directory, selected_item.text())
            with open(self.file_path, 'r') as file:
                content = file.read()
                self.text_input.setPlainText(content)
                # self.text_output.show()  # Show the output widget

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if directory:
            self.notes_directory = directory
            self.load_md_files()
    
    def new_file(self):
        # Ask the user for a new file name
        new_file_name, _ = QFileDialog.getSaveFileName(self, "Create a New File", self.notes_directory, "Markdown Files (*.md)")
        if new_file_name:
            # Create a new file in the active directory
            with open(new_file_name, "w") as file:
                file.write('# ' + new_file_name)  # You can set the initial content as needed

            # Update the list of files to include the new file
            self.load_md_files()

            # Select the newly created file in the list
            for i in range(self.file_list_widget.count()):
                item = self.file_list_widget.item(i)
                if item.text() == os.path.basename(new_file_name):
                    self.file_list_widget.setCurrentItem(item)
                    break
            self.file_path = new_file_name

        self.load_md_files()

    def update_output(self):
        input_text = self.text_input.toPlainText()

        if self.autosave:
            with open(self.file_path, "w") as file:
                file.write(input_text)

        self.text_output.clear()

        lines = input_text.split('\n')
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
                line_text = self.indent + line[3:]

            elif line.startswith('### '):
                font_size = 16
                font.setBold(True)
                line_text = 2 * self.indent + line[4:]

            elif line.startswith('#### '):
                font_size = 14
                font.setBold(True)
                line_text = 3 * self.indent + line[5:]

            elif line.startswith('\n'):
                line_text = '\n'                                                                                                
                font_size = 12
            else:
                line_text = line
                font_size = 12

            font.setPointSize(font_size)
            char_format.setFont(font)
            cursor = QTextCursor(self.text_output.document())
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(line_text, char_format)
            cursor.insertText("\n")            

        input_scroll_bar_position = self.text_input.verticalScrollBar().value()
        self.text_output.verticalScrollBar().setValue(input_scroll_bar_position)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = md_notebook()
    sys.exit(app.exec())
