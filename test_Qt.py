from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys


# creating a push button
button = QPushButton("CLICK", self)

# setting geometry of button
button.setGeometry(200, 150, 100, 40)

# adding action to a button
button.clicked.connect(self.clickme)

# getting text in button
text = button.text()

# creating label to print text
label = QLabel(text, self)
label.move(200, 200)