from PyQt6.QtWidgets import QPushButton

class Button(QPushButton):
    def __init__(self, text, action):
        super().__init__(text)
        self.text = text
        self.action = action
        self.clicked.connect(action)

    def exec(self):
        self.action()