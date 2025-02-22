import os
from components.widget.spin_box_widget import SpinBoxWidget
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from font.dynamic_font_size import get_font_sizes, apply_fonts
from PyQt5.QtGui import QFont


class ModelWidget(QtWidgets.QWidget):
    def __init__(self, filename=None, parent=None):
        super(ModelWidget, self).__init__(parent)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.pre_trained_path = os.path.join(script_dir, "../../pre-trained")

        if not os.path.exists(self.pre_trained_path):
            os.makedirs(self.pre_trained_path)

        self.current_checked_checkbox = None
        self.current_checked_file = None


        self.setup_ui()

        self.load_files()
        font_sizes = get_font_sizes()
        font_family = "Montserrat"
        content_font = QFont(font_family, font_sizes["content"]) 


    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.layout.setSpacing(10)

        font = QtGui.QFont()
        font.setPointSize(9)
        self.setFont(font)

        # Train VAE button
        self.train_button = QtWidgets.QPushButton("Train Model")
        button_style = """
            QPushButton {
                background-color: #003333; 
                color: white; 
                font-family: Montserrat; 
                font-size: {font_sizes['button']}px; 
                font-weight: 600; 
                padding: 10px 20px;
                border-radius: 5px; 
                border: none;
            }
            QPushButton:hover {
                background-color: #005555;
            }
            QPushButton:disabled {
                background-color: #999999;  
                color: white;
            }
        """
        self.train_button.setStyleSheet(button_style)
        self.train_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Set fixed size for the button (CHANGED)
        self.train_button.setFixedSize(160, 40)  # Width: 200px, Height: 40px

        # Center the button horizontally (CHANGED)
        self.layout.addWidget(self.train_button, alignment=QtCore.Qt.AlignHCenter)

        # Table to display files
        self.files_table = QtWidgets.QTableWidget(self)
        self.files_table.setColumnCount(4)
        self.files_table.setHorizontalHeaderLabels(["Select", "Name", "Date", "Actions"])
        
        # Set minimum height and allow vertical expansion
        self.files_table.setMinimumHeight(200)
        self.files_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        
        # Table styling
        self.files_table.setStyleSheet("""    
            QHeaderView::section {
                background-color: #033;
                padding: 8px;
                color: white;            
                font-size: {font_sizes['content']}px;
                font-weight: bold;
                border: none;
                height: 50px;
            }
            QTableWidget {
                background-color: transparent;
                border: none;
            }
            QTableWidget::item {
                padding-left: 30px;
                background-color: transparent;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: inherit;
            }
            QTableCornerButton::section {
                border: none;
                background-color: #033;
            }
        """)

        # Adjust header and sizing
        self.files_table.horizontalHeader().setStretchLastSection(False)
        self.files_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.files_table.verticalHeader().setVisible(False)
        self.files_table.setShowGrid(False)
        self.files_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # Create a container widget for the table
        table_container = QtWidgets.QWidget()
        table_layout = QtWidgets.QVBoxLayout(table_container)
        table_layout.addWidget(self.files_table)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.layout.addWidget(table_container)

        # SpinBox widget
        self.slider_widget = SpinBoxWidget(1)
        self.layout.addWidget(self.slider_widget)



    def load_files(self, directory=None):
        self.uncheck_checkbox()

        if directory is None:
            directory = self.pre_trained_path

        if not os.path.exists(directory):
            os.makedirs(directory)

        files = os.listdir(directory)
        self.files_table.setRowCount(len(files))
        
        # Set row height
        row_height = 40  # Adjust this value as needed
        
        for index, file_name in enumerate(files):
            self.files_table.setRowHeight(index, row_height)
            full_path = os.path.join(directory, file_name)

            # Name column
            name_item = QtWidgets.QTableWidgetItem(file_name)
            name_item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignVCenter)
            self.files_table.setItem(index, 1, name_item)

            # Date column
            mod_time = os.path.getmtime(full_path)
            mod_date = QtCore.QDateTime.fromSecsSinceEpoch(int(mod_time)).toString(QtCore.Qt.DefaultLocaleShortDate)
            date_item = QtWidgets.QTableWidgetItem(mod_date)
            date_item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignVCenter)
            self.files_table.setItem(index, 2, date_item)

            # Checkbox column
            checkbox_widget = QtWidgets.QWidget()
            checkbox_layout = QtWidgets.QHBoxLayout(checkbox_widget)
            checkbox = QtWidgets.QCheckBox()
            checkbox.setStyleSheet("""
                QCheckBox {
                    background: transparent;
                }
                QCheckBox::indicator {
                    width: 15px;
                    height: 15px;
                    background-color: transparent;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #003333;
                    border-radius: 3px;
                    background-color: white;
                }
                QCheckBox::indicator:checked {
                    background-color: #005555;
                    border: 2px solid #003333;
                    border-radius: 3px;
                }
            """)
            checkbox.stateChanged.connect(lambda state, cb=checkbox, fn=file_name: self.checkbox_clicked(state, cb, fn))
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_widget.setStyleSheet("background: transparent;")
            self.files_table.setCellWidget(index, 0, checkbox_widget)

            # Actions column
            button_widget = QtWidgets.QWidget()
            button_layout = QtWidgets.QHBoxLayout(button_widget)
            actions_button = QtWidgets.QPushButton()
            
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../icon/arrow_up.png")
            if os.path.exists(icon_path):
                icon = QtGui.QIcon(icon_path)
                
                # Create a transformed icon rotated 180 degrees
                rotated_icon = QtGui.QIcon()
                rotated_pixmap = icon.pixmap(QtCore.QSize(10, 10)).transformed(QtGui.QTransform().rotate(180))
                rotated_icon.addPixmap(rotated_pixmap)
                
                actions_button.setIcon(rotated_icon)
                actions_button.setIconSize(QtCore.QSize(10, 10))
            
            actions_button.setFixedSize(30, 30)
            actions_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                    border-radius: 5px;
                }
            """)
            actions_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            actions_button.setContentsMargins(0, 0, 0, 0)
            actions_button.clicked.connect(lambda _, f=file_name: self.show_file_options(f))
            
            button_layout.addWidget(actions_button)
            button_layout.setAlignment(QtCore.Qt.AlignCenter)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_widget.setStyleSheet("background: transparent;")
            self.files_table.setCellWidget(index, 3, button_widget)

        # Adjust table height based on content
        total_height = ((len(files) + 1) * row_height) + self.files_table.horizontalHeader().height()
        self.files_table.setMinimumHeight(total_height)
            
    def checkbox_clicked(self, state, checkbox, filename):
        if state == QtCore.Qt.Checked:
            if self.current_checked_checkbox and self.current_checked_checkbox != checkbox:
                self.current_checked_checkbox.setChecked(False)
            self.current_checked_checkbox = checkbox
            print(f"Checkbox clicked for file: {filename}")
            self.current_checked_file = filename
        else:
            if self.current_checked_checkbox == checkbox:
                self.current_checked_checkbox = None
                print(f"Checkbox unchecked for file: {filename}")
                filename = None
                self.current_checked_file = None         

    def uncheck_checkbox(self):
        if self.current_checked_checkbox:
            self.current_checked_checkbox.setChecked(False)
            self.current_checked_checkbox = None
            self.current_checked_file = None
            print("Checkbox unchecked")

    def show_file_options(self, file):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
            QMenu { 
                background-color: #033; 
                border: none;
                font-weight: bold;
                padding: 0px;
            }
            QMenu::item { 
                color: white; 
            }
            QMenu::item:selected { 
                background-color: white;
                color: #033;
            }
            QMenu::item:hover { 
                background-color: white;
                color: #033; 
            }
        """)

        rename_action = QtWidgets.QAction("Rename", self)
        rename_action.triggered.connect(lambda: self.rename_file(file))

        delete_action = QtWidgets.QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_file(file))

        menu.addAction(rename_action)
        menu.addAction(delete_action)

        menu.exec_(QtGui.QCursor.pos())

    def rename_file(self, file):
        """Rename a file using a custom input dialog"""
        new_name, ok = self.create_custom_input_dialog(
            title="Rename File",
            label=f"Enter new name for {file}:"
        )

        if ok and new_name:
            old_path = os.path.join(self.pre_trained_path, file)
            new_path = os.path.join(self.pre_trained_path, new_name)
            try:
                os.rename(old_path, new_path)
                self.refresh_file_list()
            except OSError as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to rename file: {str(e)}")

    def delete_file(self, file):
        """Delete a file after user confirms through a custom message box"""
        confirm_delete = self.create_custom_message_box(
            title="Delete File",
            message=f"Are you sure you want to delete {file}?"
        )

        if confirm_delete:
            file_path = os.path.join(self.pre_trained_path, file)
            try:
                os.remove(file_path)
                self.refresh_file_list()
            except OSError as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to delete file: {str(e)}")


    def create_custom_message_box(self, title, message):
        """Create a custom message box"""
        message_box = QtWidgets.QMessageBox()
        icon = QIcon("icon/icon.ico")
        message_box.setWindowIcon(icon)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        message_box.setMinimumSize(600, 300)
        message_box.setSizeGripEnabled(True)
        message_box.setStyleSheet("""
            QMessageBox {
                font-size: {font_sizes['content']}px;
                font-weight: bold;
                padding: 20px;
                font-family: 'Montserrat', sans-serif;
            }
            QPushButton {
                margin-left: 10px;
                background-color: #003333;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: {font_sizes['button']}px;
                font-weight: bold;
                font-family: 'Montserrat', sans-serif;
                line-height: 20px;
            }
            QPushButton:hover {
                background-color: #005555;
            }
        """)

        return message_box.exec_() == QtWidgets.QMessageBox.Yes

    def create_custom_input_dialog(self, title, label, text=""):
        """Create a QInputDialog with custom styling"""
        input_dialog = QtWidgets.QInputDialog(self)
        input_dialog.setWindowTitle(title)
        input_dialog.setLabelText(label)
        input_dialog.setTextValue(text)

        # Apply custom styles to input dialog
        input_dialog.setStyleSheet("""
            QMessageBox {
                font-size: {font_sizes['content']}px;
                font-family: 'Montserrat', sans-serif;
            }
            QPushButton {
                margin-left: 10px;
                background-color: #003333;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: {font_sizes['button']}px;
                font-weight: bold;
                font-family: 'Montserrat', sans-serif;
                line-height: 20px;
            }
            QPushButton:hover {
                background-color: #005555;
            }
            QLineEdit {
                padding: 5px;
                width: 500px;
                font-family: 'Montserrat', sans-serif;
                font-size: {font_sizes['content']}px;
                border: 1px solid #ccc;
            }
            QLabel {
                font-size: {font_sizes['title']}px;
                font-weight: bold;
                font-family: 'Montserrat', sans-serif;
            }
        """)
        ok = input_dialog.exec_()

        return input_dialog.textValue(), ok

    def refresh_file_list(self):
        self.load_files()

