from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from components.widget.collapsible_widget import CollapsibleWidget
from components.widget.file_container_widget import FileContainerWidget
from components.widget.file_preview_widget import FilePreviewWidget
from components.widget.model_widget import ModelWidget
from components.widget.process_log_widget import ProcessLogWidget
from components.widget.output_widget import OutputWidget
from components.widget.spin_box_widget import SpinBoxWidget
from components.button.DragDrop_Button import DragDrop_Button
from components.widget.result_preview_widget import SVCpreview
import os
import time

class Workplace(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Workplace, self).__init__(parent)
        self.uploaded_files = []
        self.setupUi()
        

    def setupUi(self):
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.setFont(font)

        # Create a scroll area
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Create a container widget for the scroll area content
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)

        # Set a size policy for the scroll widget that allows it to shrink
        self.scroll_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        # Add the scroll area to the main layout
        self.scroll_area.setWidget(self.scroll_widget)
        self.gridLayout.addWidget(self.scroll_area)

        # Call functions to set up collapsible components
        self.setup_input_collapsible()
        self.setup_model_collapsible()
        self.setup_preview_collapsible()
        self.setup_process_log_collapsible()
        self.setup_output_collapsible()
        self.setup_result_collapsible()

        # Generate Synthetic Data button
        button_layout = QtWidgets.QVBoxLayout()
        self.generate_data_button = QtWidgets.QPushButton("Generate Synthetic Data", self)
        self.generate_data_button.setStyleSheet(
            """
            QPushButton {
                background-color: #003333; 
                color: white; 
                font-family: Montserrat; 
                font-size: 14px; 
                font-weight: 600; 
                padding: 10px 20px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005555; 
            }
            """
        )
        self.generate_data_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # put the button at the bottom
        self.generate_data_button.clicked.connect(self.on_generate_data)

        button_layout.addWidget(self.generate_data_button, alignment=QtCore.Qt.AlignCenter)

        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        button_layout.addItem(spacer)

        # Adding the button to the main layout
        self.gridLayout.addLayout(button_layout, 1, 0)
        
    def on_generate_data(self):
        print("Synthetic data generated.")
        
        QtCore.QTimer.singleShot(0, lambda: self.collapsible_widget_process_log.toggle_container(True))
        QtCore.QTimer.singleShot(3000, lambda: self.collapsible_widget_output.toggle_container(True))
        QtCore.QTimer.singleShot(4000, lambda: self.collapsible_widget_result.toggle_container(True))
    
    def setup_input_collapsible(self):
        """Set up the 'Input' collapsible widget and its contents."""
        font = QtGui.QFont()
        font.setPointSize(20)

        # Call the collapsible widget component for Input
        self.collapsible_widget_input = CollapsibleWidget("Input", self)
        self.scroll_layout.addWidget(self.collapsible_widget_input)

        # Add the FileUploadWidget
        self.file_upload_widget = DragDrop_Button(self)
        self.file_upload_widget.file_uploaded.connect(self.update_file_display)  # Connect the signal
        self.collapsible_widget_input.add_widget(self.file_upload_widget)

        # Add "Add More Files" button to Input collapsible widget
        self.add_file_button = QtWidgets.QPushButton("Add More Files", self)
        self.add_file_button.setStyleSheet(
            """
            QPushButton {
                background-color: #003333; 
                color: white; 
                font-family: Montserrat; 
                font-size: 14px; 
                font-weight: 600; 
                padding: 8px 16px;
                margin-left: 15px; 
                margin-right: 15px; 
                border-radius: 5px; 
                border: none;
            }
            QPushButton:hover {
                background-color: #005555;  /* Change this to your desired hover color */
            }
            """
        )
        self.add_file_button.setFont(font)
        self.add_file_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_file_button.clicked.connect(self.add_more_files)
        self.collapsible_widget_input.add_widget(self.add_file_button)
        
        # Create a scrollable area to hold the file widgets
        self.file_scroll_area = QtWidgets.QScrollArea(self)
        self.file_scroll_area.setWidgetResizable(True)
        self.file_scroll_area.setMinimumHeight(150)

        # Create a container to hold the file widgets and its layout
        self.file_container_widget = QtWidgets.QWidget(self)
        self.file_container_layout = QtWidgets.QVBoxLayout(self.file_container_widget)
        self.file_container_layout.setSpacing(0)
        
        # Add the file container widget to the scroll area
        self.file_scroll_area.setWidget(self.file_container_widget)
        self.collapsible_widget_input.add_widget(self.file_scroll_area)
        

        # Initially hide other components
        self.file_upload_widget.setVisible(True)
        self.show_other_components(False)


        # Open the collapsible widget by default
        self.collapsible_widget_input.toggle_container(True)

    
    def show_other_components(self, show=True):
        """Show or hide other components based on file upload."""
        self.add_file_button.setVisible(show)
        self.file_container_widget.setVisible(show)

    def setup_model_collapsible(self):
        self.collapsible_model_container = CollapsibleWidget("Models", self)
        self.scroll_layout.addWidget(self.collapsible_model_container)

        self.model_widget = ModelWidget(self)
        self.collapsible_model_container.add_widget(self.model_widget)
    
    def setup_preview_collapsible(self):
        self.collapsible_widget_preview = CollapsibleWidget("File Preview", self)
        self.scroll_layout.addWidget(self.collapsible_widget_preview)

        self.file_preview_widget = FilePreviewWidget(self)
        self.collapsible_widget_preview.add_widget(self.file_preview_widget)

    def setup_process_log_collapsible(self):
        self.collapsible_widget_process_log = CollapsibleWidget("Process Log", self)
        self.scroll_layout.addWidget(self.collapsible_widget_process_log)

        self.process_log_widget = ProcessLogWidget(self)
        self.collapsible_widget_process_log.add_widget(self.process_log_widget)

    def setup_output_collapsible(self):
        self.collapsible_widget_output = CollapsibleWidget("Output", self)
        self.scroll_layout.addWidget(self.collapsible_widget_output)

        self.output_widget = OutputWidget(self)
        self.output_widget.clearUI.connect(self.clear_all_ui)
        self.collapsible_widget_output.add_widget(self.output_widget)

    def setup_result_collapsible(self):
        """Set up the 'Result' collapsible widget and its contents."""

        # Call collapsible widget for Result
        self.collapsible_widget_result = CollapsibleWidget("Result", self)
        self.scroll_layout.addWidget(self.collapsible_widget_result)

        self.svc_preview = SVCpreview(self)
        self.collapsible_widget_result.add_widget(self.svc_preview)
        
    def handle_file_removal(self, file_path, file_name):
        """Handle the file removal logic when a file is removed."""
        if file_path in self.uploaded_files:
            # Remove the file from the uploaded_files list
            self.uploaded_files.remove(file_path)  
            print(f"Removed file: {file_name}, remaining files: {self.uploaded_files}")  # Debug statement

            # Update the UI to reflect the removal
            for i in reversed(range(self.file_container_layout.count())):
                widget = self.file_container_layout.itemAt(i).widget()
                if isinstance(widget, FileContainerWidget) and widget.file_name == file_name:
                    widget.remove_file_signal.disconnect()  # Disconnect signal to avoid errors
                    self.file_container_layout.removeWidget(widget)  # Remove the widget from layout
                    widget.deleteLater()  # Schedule the widget for deletion
                    widget.setParent(None)  # Detach widget from its parent
                    break  # Exit after removing the specific file container

            # If no more files, show the file upload widget again
            if not self.uploaded_files:
                self.show_other_components(False)
                self.file_upload_widget.setVisible(True)
                self.file_preview_widget.clear()

            # Update the file container layout to reflect the changes
            self.file_container_layout.update()

    def update_file_display(self, new_uploaded_files):
        """Update the display of files based on newly uploaded files."""
        # Append new files to the existing list, avoiding duplicates
        for file_path in new_uploaded_files:
            if file_path not in self.uploaded_files:
                self.uploaded_files.append(file_path)
        
        print("Uploaded files:", self.uploaded_files)  # Debugging output
        
        has_files = bool(self.uploaded_files)
        self.show_other_components(has_files)

        # Hide the file upload widget if files are uploaded
        self.file_upload_widget.setVisible(not has_files)

        # Clear existing widgets in the file container layout
        for i in reversed(range(self.file_container_layout.count())):
            widget = self.file_container_layout.itemAt(i).widget()
            if widget is not None:
                widget.remove_file_signal.disconnect()  # Disconnect signal to avoid errors
                widget.deleteLater()  # Schedule widget deletion
                self.file_container_layout.removeWidget(widget)

        # Re-add file containers for each uploaded file and update preview
        for file_path in self.uploaded_files:
            file_name = os.path.basename(file_path)

            # Verify the file still exists before displaying it
            if os.path.exists(file_path):
                new_file_container = FileContainerWidget(file_path, self)
                new_file_container.hide_download_button()
                new_file_container.hide_retry_button()
                new_file_container.remove_file_signal.connect(self.handle_file_removal)  # Connect remove signal
                self.file_container_layout.addWidget(new_file_container)

                # Display the file content in the file preview widget
                self.file_preview_widget.display_file_contents(file_path)

                # Display the file content in the result preview widget
                self.svc_preview.display_file_contents(file_path, 0)

        self.file_preview_widget.set_uploaded_files(self.uploaded_files)
        
        # Automatically expand the preview collapsible widget if there are files
        if has_files:
            self.collapsible_widget_preview.toggle_container(True)

    def add_more_files(self):
        self.file_upload_widget.open_file_dialog()
    
    def get_image_path(self, image_name):
        path = os.path.join(os.path.dirname(__file__), '..', 'icon', image_name)
        return path
    
    def clear_all_ui(self):
        # Clear uploaded files
        self.uploaded_files = []
        
        # Reset file upload widget
        self.file_upload_widget.setVisible(True)
        self.show_other_components(False)
        
        # Clear file containers
        for i in reversed(range(self.file_container_layout.count())):
            widget = self.file_container_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Clear previews and logs
        self.file_preview_widget.clear()
        self.process_log_widget.clear()
        self.svc_preview.clear()
        
        # Collapse all widgets except Input
        self.collapsible_widget_preview.toggle_container(False)
        self.collapsible_widget_process_log.toggle_container(False)
        self.collapsible_widget_output.toggle_container(False)
        self.collapsible_widget_result.toggle_container(False)
        
if __name__ == "__main__":
    
    
    app = QtWidgets.QApplication([])
    window = Workplace()
    window.show()
    app.exec_()
