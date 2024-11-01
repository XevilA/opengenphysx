import sys
import numpy as np
import sympy as sp
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QComboBox, QLabel,
    QLineEdit, QPushButton, QWidget, QMessageBox, QHBoxLayout,
    QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

class DotminiENGLab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dotmini ENGLab")
        self.setGeometry(100, 100, 1000, 700)

        # Set modern MacOS-like style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QComboBox {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 5px 10px;
                background-color: white;
                min-height: 30px;
            }
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 5px 10px;
                background-color: white;
                min-height: 30px;
                margin: 5px 0;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                min-height: 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0051D5;
            }
            QPushButton:pressed {
                background-color: #003EAA;
            }
            QLabel {
                color: #1d1d1f;
                padding: 5px;
            }
            QFrame {
                border-radius: 10px;
                background-color: white;
            }
        """)

        # Main container with padding
        main_container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Left panel
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_panel.setStyleSheet("""
            QFrame#leftPanel {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        # Physics topic selector with modern styling
        self.physics_topic = QComboBox()
        self.physics_topic.addItems([
            "Select Topic", "Dynamics", "Newton's Laws",
            "Work & Energy", "Kinematics", "Projectile Motion",
            "Calculus"
        ])
        self.physics_topic.currentIndexChanged.connect(self.on_topic_changed)
        left_layout.addWidget(self.physics_topic)

        # Input fields container
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout()
        self.input_container.setLayout(self.input_layout)
        left_layout.addWidget(self.input_container)

        # Results display
        self.result_label = QLabel("Results will appear here")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #f8f8f8;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        left_layout.addWidget(self.result_label)

        # Buttons container
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton("Calculate")
        self.plot_button = QPushButton("Plot Graph")
        self.calculate_button.clicked.connect(self.calculate_result)
        self.plot_button.clicked.connect(self.plot_graph)
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.plot_button)
        left_layout.addLayout(button_layout)

        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel, stretch=2)

        # Right panel (AI Chat)
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_panel.setStyleSheet("""
            QFrame#rightPanel {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        right_layout = QVBoxLayout()

        # Chat display with LaTeX support
        self.web_view = QWebEngineView()
        self.web_view.setMinimumWidth(300)
        self.web_view.setHtml(self.get_initial_html())
        right_layout.addWidget(self.web_view)

        # Input area
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ask a question...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        right_layout.addLayout(input_layout)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, stretch=1)

        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        self.input_fields = []

    def get_initial_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML"></script>
            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({
                    tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]},
                    messageStyle: "none"
                });
            </script>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    margin: 20px;
                    color: #1d1d1f;
                }
                .message {
                    margin-bottom: 15px;
                    padding: 10px;
                    border-radius: 8px;
                }
                .user-message {
                    background-color: #007AFF22;
                }
                .ai-message {
                    background-color: #f5f5f7;
                }
            </style>
        </head>
        <body>
            <div id="chat-container"></div>
        </body>
        </html>
        """

    def update_chat_display(self, user_message, ai_response):
        script = f"""
            var container = document.getElementById('chat-container');
            var userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.innerHTML = '<strong>You:</strong> ' + {repr(user_message)};
            var aiDiv = document.createElement('div');
            aiDiv.className = 'message ai-message';
            aiDiv.innerHTML = '<strong>AI:</strong> ' + {repr(ai_response)};
            container.appendChild(userDiv);
            container.appendChild(aiDiv);
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, aiDiv]);
            window.scrollTo(0, document.body.scrollHeight);
        """
        self.web_view.page().runJavaScript(script)

    def send_message(self):
        user_message = self.user_input.text()
        if user_message:
            ai_response = self.get_ai_response(user_message)
            self.update_chat_display(user_message, ai_response)
            self.user_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a message.")

    def get_ai_response(self, message):
        url = "https://api.opentyphoon.ai/v1/chat/completions"
        # Add instruction for LaTeX formatting
        enhanced_message = (
            "Please format any mathematical expressions, equations, or physics formulas "
            "using LaTeX notation enclosed in $ symbols. For example, use $F = ma$ for "
            "Newton's second law. Here's the question: " + message
        )

        payload = {
            "model": "typhoon-v1.5x-70b-instruct",
            "messages": [{"role": "user", "content": enhanced_message}],
            "max_tokens": 512,
            "temperature": 0.96,
            "top_p": 0.9,
            "top_k": 0,
            "repetition_penalty": 1.05,
            "min_p": 0
        }
        headers = {
            "Authorization": "Bearer sk-kdTPGlP6akWgbfw0V0CCQ4IPz9GfYjPTEU1X7cC1OMqLMMie",  # Replace with your actual API key
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("choices")[0].get("message").get("content", "No response from AI.")
            else:
                return f"Error {response.status_code}: Unable to communicate with AI."
        except Exception as e:
            return f"Error: {str(e)}"

    def on_topic_changed(self, index):
        # Clear existing input fields
        while self.input_layout.count():
            item = self.input_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.input_fields.clear()

        topic = self.physics_topic.currentText()

        if topic == "Select Topic":
            return
        elif topic in ["Dynamics", "Newton's Laws", "Work & Energy"]:
            self.create_physics_inputs(topic)
        elif topic in ["Kinematics", "Projectile Motion"]:
            self.create_kinematic_inputs(topic)
        elif topic == "Calculus":
            self.create_calculus_inputs()

    def create_physics_inputs(self, topic):
        if topic == "Dynamics":
            self.add_input_field("Mass (kg)", "mass")
            self.add_input_field("Acceleration (m/s²)", "acceleration")
            self.add_input_field("Force (N)", "force")
        elif topic == "Newton's Laws":
            self.add_input_field("Mass (kg)", "mass")
            self.add_input_field("Force (N)", "force")
        elif topic == "Work & Energy":
            self.add_input_field("Work (J)", "work")
            self.add_input_field("Energy (J)", "energy")

    def create_kinematic_inputs(self, topic):
        self.add_input_field("Initial Velocity (m/s)", "v0")
        self.add_input_field("Final Velocity (m/s)", "v")
        self.add_input_field("Time (s)", "t")

    def create_calculus_inputs(self):
        self.add_input_field("Function (e.g., x^2 + 2*x + 1)", "function")
        self.add_input_field("Variable (e.g., x)", "variable")

    def add_input_field(self, label_text, identifier):
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setObjectName(identifier)
        self.input_layout.addWidget(label)
        self.input_layout.addWidget(input_field)
        self.input_fields.append(input_field)

    def calculate_result(self):
        topic = self.physics_topic.currentText()
        try:
            if topic == "Dynamics":
                mass = float(self.input_fields[0].text())
                acceleration = float(self.input_fields[1].text())
                force = mass * acceleration
                self.result_label.setText(f"Calculated Force: {force:.2f} N")
            elif topic == "Newton's Laws":
                mass = float(self.input_fields[0].text())
                force = float(self.input_fields[1].text())
                acceleration = force / mass
                self.result_label.setText(f"Calculated Acceleration: {acceleration:.2f} m/s²")
            elif topic == "Work & Energy":
                work = float(self.input_fields[0].text())
                energy = float(self.input_fields[1].text())
                self.result_label.setText(f"Total Work-Energy: {work + energy:.2f} J")
            elif topic == "Kinematics":
                v0 = float(self.input_fields[0].text())
                v = float(self.input_fields[1].text())
                t = float(self.input_fields[2].text())
                average_acceleration = (v - v0) / t
                self.result_label.setText(f"Average Acceleration: {average_acceleration:.2f} m/s²")
            elif topic == "Calculus":
                function = self.input_fields[0].text()
                variable = self.input_fields[1].text()
                x = sp.symbols(variable)
                func = sp.sympify(function)
                derivative = sp.diff(func, x)
                self.result_label.setText(f"Derivative: {derivative}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values.")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An error occurred: {str(e)}")

    def plot_graph(self):
        topic = self.physics_topic.currentText()
        # Placeholder for plotting functionality
        QMessageBox.information(self, "Plotting", f"Plotting is not implemented for {topic} yet.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = DotminiENGLab()
    main_win.show()
    sys.exit(app.exec())
