import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QTextEdit

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.vbox = QVBoxLayout()
		self.label = QLabel(self)
		self.button = QPushButton("Pushme", self)
		self.line = QLineEdit(self)
		self.vbox.addWidget(self.line)
		self.vbox.addWidget(self.label)
		self.vbox.addWidget(self.button)
		self.label.setText("")
		self.setLayout(self.vbox)
		self.button.clicked.connect(self.action)
	def action(self):
		answer = self.line.text()
		self.label.setText(answer)	
app = QApplication(sys.argv)
win = Window()
win.show() 
sys.exit(app.exec())
# написать калькулятор