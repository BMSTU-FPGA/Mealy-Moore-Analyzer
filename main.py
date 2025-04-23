import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QFrame, QComboBox, QSizePolicy
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

DEFAULT_FONT_SIZE = 20
DEFAULT_HEADER_FONT_SIZE = 26
DEFAULT_FONT_STYLE = 'Arial'
DEFAULT_MONOSPACE_FONT_STYLE = 'Consolas'

class BinaryParserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binary Parser")
        self.setFixedSize(700, 500)  # Scaled window size

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Scaled margins
        main_layout.setSpacing(20)  # Scaled spacing

        # Top part
        top_part = QWidget()
        top_layout = QVBoxLayout(top_part)
        top_layout.setSpacing(16)  # Scaled spacing

        # First line edit with toggle button
        line1_layout = QHBoxLayout()
        self.binary_input = QLineEdit()
        self.binary_input.setPlaceholderText("Cодержимое ячейки памяти")
        self.binary_input.setMaxLength(32)
        self.binary_input.setValidator(self.create_binary_validator())
        self.binary_input.setFont(QFont(DEFAULT_MONOSPACE_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        line1_layout.addWidget(self.binary_input)

        self.enable_button = QPushButton("E")
        self.enable_button.setCheckable(True)
        self.enable_button.setChecked(False)
        self.enable_button.setFixedSize(40, 40)  # Scaled size
        self.enable_button.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        self.enable_button.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                border-radius: 6px;
            }
        """)

        self.reset_button = QPushButton("R")
        self.reset_button.setCheckable(True)
        self.reset_button.setChecked(False)
        self.reset_button.setFixedSize(40, 40)  # Scaled size
        self.reset_button.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                border-radius: 6px;
            }
        """)


        line1_layout.addWidget(self.reset_button)
        line1_layout.addWidget(self.enable_button)

        top_layout.addLayout(line1_layout)

        # Second line edit with copy button
        line2_layout = QHBoxLayout()
        self.next_step_input = QLineEdit()
        self.next_step_input.setReadOnly(True)
        self.next_step_input.setFont(QFont(DEFAULT_MONOSPACE_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        line2_layout.addWidget(self.next_step_input)

        self.copy_button = QPushButton("📋")  # Clipboard emoji
        self.copy_button.setFixedSize(40, 40)  # Scaled size
        self.copy_button.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        self.copy_button.setStyleSheet("""
            QPushButton {
                border: 2px solid gray;
                border-radius: 6px;
                background-color: palette(button);
                padding: 0;
            }
        """)
        line2_layout.addWidget(self.copy_button)

        top_layout.addLayout(line2_layout)

        # Combo box with label at the bottom of first segment
        combo_layout = QHBoxLayout()
        self.next_x_label = QLabel("Следующий X:")
        self.next_x_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE)) 
        combo_layout.addWidget(self.next_x_label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(['x1', 'x2', 'x3', 'x4'])
        self.combo_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.combo_box.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        combo_layout.addWidget(self.combo_box)
        combo_layout.addStretch()  # Push combo box to the left

        top_layout.addLayout(combo_layout)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        top_layout.addWidget(separator)

        main_layout.addWidget(top_part)

        # Bottom part
        bottom_part = QWidget()
        bottom_layout = QVBoxLayout(bottom_part)
        bottom_layout.setSpacing(12)  # Scaled spacing

        # Labels for displaying parsed data
        self.x_label = QLabel("X: ")
        self.x_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        bottom_layout.addWidget(self.x_label)

        # Mealy Automata section
        mealy_label = QLabel("Автомат Мили")
        mealy_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_HEADER_FONT_SIZE))  # Scaled font size
        bottom_layout.addWidget(mealy_label)

        mealy_layout = QHBoxLayout()
        self.y_mil_label = QLabel("Y: ")
        self.y_mil_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        self.t_mil_label = QLabel("T: ")
        self.t_mil_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        mealy_layout.addWidget(self.y_mil_label)
        mealy_layout.addWidget(self.t_mil_label)
        bottom_layout.addLayout(mealy_layout)

        # Moore Automata section
        moore_label = QLabel("Автомат Мура")
        moore_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_HEADER_FONT_SIZE))  # Scaled font size
        bottom_layout.addWidget(moore_label)

        moore_layout = QHBoxLayout()
        self.y_mur_label = QLabel("Y: ")
        self.y_mur_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        self.t_mur_label = QLabel("T: ")
        self.t_mur_label.setFont(QFont(DEFAULT_FONT_STYLE, DEFAULT_FONT_SIZE))  # Scaled font size
        moore_layout.addWidget(self.y_mur_label)
        moore_layout.addWidget(self.t_mur_label)
        bottom_layout.addLayout(moore_layout)

        main_layout.addWidget(bottom_part)

        # Connect signals
        self.binary_input.textChanged.connect(self.update_display)
        self.enable_button.toggled.connect(self.toggle_enable_button_state)
        self.enable_button.toggled.connect(self.update_display)
        self.reset_button.toggled.connect(self.toggle_reset_button_state)
        self.reset_button.toggled.connect(self.update_display)
        self.combo_box.currentTextChanged.connect(self.update_display)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Initialize with empty values
        self.vals = {
            "x_str": "",
            "y_mil_str": "",
            "t_mil_str": "",
            "y_mur_str": "",
            "t_mur_str": ""
        }

    def create_binary_validator(self):
        """Create a validator that only allows 0s and 1s"""
        from PyQt6.QtGui import QRegularExpressionValidator
        from PyQt6.QtCore import QRegularExpression
        reg_ex = QRegularExpression("^[01]*$")
        return QRegularExpressionValidator(reg_ex)

    def toggle_enable_button_state(self, checked):
        """Update the toggle button appearance based on state"""
        if checked:
            self.enable_button.setStyleSheet("""
                QPushButton {
                    background-color: #b8bb26;
                    color: white;
                    border-radius: 6px;
                }
            """)
        else:
            self.enable_button.setStyleSheet("""
                QPushButton {
                    background-color: gray;
                    color: white;
                    border-radius: 6px;
                }
            """)
    
    def toggle_reset_button_state(self, checked):
        """Update the toggle button appearance based on state"""
        if checked:
            self.reset_button.setStyleSheet("""
                QPushButton {
                    background-color: #fb4934;
                    color: white;
                    border-radius: 6px;
                }
            """)
        else:
            self.reset_button.setStyleSheet("""
                QPushButton {
                    background-color: gray;
                    color: white;
                    border-radius: 6px;
                }
            """)

    def parse(self, bin_str):
        """Parse the binary string and return a dictionary of values"""

        dict_keys = ["x_str", "y_mil_str", "t_mil_str", "y_mur_str", "t_mur_str"]
        selected_values = (bin_str[30:32], bin_str[21:24], bin_str[16:18], bin_str[13:16], bin_str[8:11])
        # 00000000 111 00 111 11 000 111 11 0000 11
        # 00000000111001111100011111000011
        parsed_values = tuple(str(int(elem, base=2) + 1) for elem in selected_values)
        return dict(zip(dict_keys, parsed_values))

    def update_next_step_input(self):
        """Update next_step_input based on buttons state, combo_box and binary_input """
        bin_str = self.binary_input.text()
        if bin_str is None:
            return
        next_x_str = self.combo_box.currentText()
        next_x = bin(int(next_x_str[1:]) - 1)[2:].rjust(2, '0')
        reset = '1' if self.reset_button.isChecked() else '0'
        enable = '1' if self.enable_button.isChecked() else '0'
        text = bin_str[:-8] + reset + enable + bin_str[-6:-2] + next_x
        if len(text) != 32:
            print(text, len(text), bin_str[:-8], reset, enable, bin_str[-6:-2], next_x)
            os._exit(1)
        self.next_step_input.setText(text)
        #text[] = text[-32:]

    def update_display(self):
        """Update all displayed values based on current input and state"""
        
        bin_str = self.binary_input.text()
        if bin_str is not None and len(bin_str) == 32:
            self.vals = self.parse(bin_str)
            self.update_next_step_input()
        else:
            self.vals = None
        # Update the result line edit

        # Update all labels
        if self.vals is not None:
            self.x_label.setText(f"X: x{self.vals['x_str']}")
            self.y_mil_label.setText(f"Y: y{self.vals['y_mil_str']}")
            self.t_mil_label.setText(f"T: t{self.vals['t_mil_str']}")
            self.y_mur_label.setText(f"Y: y{self.vals['y_mur_str']}")
            self.t_mur_label.setText(f"T: t{self.vals['t_mur_str']}")
        else:
            self.x_label.setText("X:")
            self.y_mil_label.setText("Y:")
            self.t_mil_label.setText("T:")
            self.y_mur_label.setText("Y:")
            self.t_mur_label.setText("T:")

        # Update the combo box based on the state of the reset and enable buttons
        

    def copy_to_clipboard(self):
        """Copy the contents of the result line edit to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.next_step_input.text())

        # Change the copy button text to a green check mark emoji
        self.copy_button.setText("✅")

        # Set up a timer to revert the button text back to the clipboard emoji after 3 seconds
        QTimer.singleShot(3000, self.reset_copy_button)

    def reset_copy_button(self):
        """Reset the copy button text to the clipboard emoji"""
        self.copy_button.setText("📋")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BinaryParserApp()
    window.show()
    sys.exit(app.exec())