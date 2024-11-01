import sys
import numpy as np
import sympy as sp
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QComboBox, QLabel,
    QLineEdit, QPushButton, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt

class DotminiENGLab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dotmini ENGLab")
        self.setGeometry(100, 100, 600, 400)

        # Initialize components
        self.physics_topic = QComboBox(self)
        self.physics_topic.addItems(["Select Topic", "Dynamics", "Newton's Laws", "Work & Energy", "Calculus"])
        self.physics_topic.currentIndexChanged.connect(self.on_topic_changed)

        self.input_fields = []
        self.result_label = QLabel("Results will appear here", self)

        # Buttons
        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.clicked.connect(self.calculate_result)

        self.plot_button = QPushButton("Plot Graph", self)
        self.plot_button.clicked.connect(self.plot_graph)

        self.send_button = QPushButton("Send to Typhoon AI", self)
        self.send_button.clicked.connect(self.send_message)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Type your message here...")

        self.chat_display = QLabel("", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.physics_topic)
        layout.addWidget(self.result_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.send_button)
        layout.addWidget(self.chat_display)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_topic_changed(self):
        """Update input fields based on selected topic."""
        self.clear_input_fields()
        topic = self.physics_topic.currentText()

        if topic == "Dynamics":
            self.add_input_field("Mass (kg)")
            self.add_input_field("Velocity (m/s)")
        elif topic == "Newton's Laws":
            self.add_input_field("Mass (kg)")
            self.add_input_field("Acceleration (m/s²)")
        elif topic == "Work & Energy":
            self.add_input_field("Force (N)")
            self.add_input_field("Displacement (m)")
        elif topic == "Calculus":
            self.add_input_field("Enter Equation (in terms of x)")

    def add_input_field(self, placeholder):
        """Add an input field to the UI."""
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder)
        self.input_fields.append(input_field)
        self.layout().insertWidget(1 + len(self.input_fields), input_field)

    def clear_input_fields(self):
        """Remove all dynamic input fields."""
        for input_field in self.input_fields:
            self.layout().removeWidget(input_field)
            input_field.deleteLater()
        self.input_fields = []

    def calculate_result(self):
        """Calculate result based on selected topic."""
        topic = self.physics_topic.currentText()

        try:
            if topic == "Dynamics":
                mass = float(self.input_fields[0].text())
                velocity = float(self.input_fields[1].text())
                kinetic_energy = 0.5 * mass * velocity ** 2
                self.result_label.setText(f"Kinetic Energy: {kinetic_energy} J")
            elif topic == "Newton's Laws":
                mass = float(self.input_fields[0].text())
                acceleration = float(self.input_fields[1].text())
                force = mass * acceleration
                self.result_label.setText(f"Force: {force} N")
            elif topic == "Work & Energy":
                force = float(self.input_fields[0].text())
                displacement = float(self.input_fields[1].text())
                work_done = force * displacement
                self.result_label.setText(f"Work Done: {work_done} J")
            elif topic == "Calculus":
                equation = self.input_fields[0].text()
                x = sp.symbols('x')
                expr = sp.sympify(equation)
                derivative = sp.diff(expr, x)
                self.result_label.setText(f"Derivative: {derivative}")
            else:
                self.result_label.setText("Please select a valid topic.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values.")

    def plot_graph(self):
        """Plot graphs based on the current topic."""
        topic = self.physics_topic.currentText()

        try:
            if topic == "Dynamics":
                mass = float(self.input_fields[0].text())
                velocity_range = np.linspace(0, 20, 100)
                kinetic_energy = 0.5 * mass * velocity_range ** 2
                plt.plot(velocity_range, kinetic_energy, label="Kinetic Energy (J)")
                plt.xlabel("Velocity (m/s)")
                plt.ylabel("Kinetic Energy (J)")
                plt.title("Kinetic Energy vs. Velocity")

            elif topic == "Newton's Laws":
                mass = float(self.input_fields[0].text())
                acceleration_range = np.linspace(0, 20, 100)
                force = mass * acceleration_range
                plt.plot(acceleration_range, force, label="Force (N)")
                plt.xlabel("Acceleration (m/s²)")
                plt.ylabel("Force (N)")
                plt.title("Force vs. Acceleration")

            elif topic == "Work & Energy":
                force = float(self.input_fields[0].text())
                displacement_range = np.linspace(0, 20, 100)
                work_done = force * displacement_range
                plt.plot(displacement_range, work_done, label="Work Done (J)")
                plt.xlabel("Displacement (m)")
                plt.ylabel("Work Done (J)")
                plt.title("Work Done vs. Displacement")

            plt.legend()
            plt.grid(True)
            plt.show()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid input values for plotting.")

    def send_message(self):
        """Send user input to Typhoon AI API and display the response."""
        user_text = self.user_input.text()
        if not user_text:
            QMessageBox.warning(self, "Input Error", "Please enter a message.")
            return

        endpoint = 'https://api.opentyphoon.ai/v1/chat/completions'
        headers = {
            "Authorization": "Bearer sk-kdTPGlP6akWgbfw0V0CCQ4IPz9GfYjPTEU1X7cC1OMqLMMie",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "typhoon-v1.5x-70b-instruct",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": user_text}],
            "temperature": 0.9,
            "top_p": 0.9,
            "top_k": 0,
            "repetition_penalty": 1.05,
            "min_p": 0
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            # Extract and display the AI's response
            ai_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
            self.chat_display.setText(f"AI: {ai_message}")
            self.user_input.clear()
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "API Error", f"Failed to communicate with Typhoon AI: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DotminiENGLab()
    window.show()
    sys.exit(app.exec())
