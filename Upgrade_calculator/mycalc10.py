from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLineEdit, QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QLabel

from keypad import numPadList, operatorList, constantList, functionList
from connection import connectionWithConstants, connectionWithFunctions

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignRight)
        self.setMaxLength(15)


class Calculator(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Display Window
        displayLayout = QGridLayout()
        self.displayResult = LineEdit()
        self.displayStatus = QLabel("")
        self.displayCurrentInput = LineEdit()
        self.displayStatus.setAlignment(Qt.AlignCenter)
        displayLayout.addWidget(self.displayResult, 0, 0, 1, 0)
        displayLayout.addWidget(self.displayStatus, 2, 0, 2, 1)
        displayLayout.addWidget(self.displayCurrentInput, 2, 1, 2, 2)

        # Button Creation and Placement
        numLayout = QGridLayout()
        opLayout = QGridLayout()
        constLayout = QGridLayout()
        funcLayout = QGridLayout()

        buttonGroups = {
            'num': {'buttons': numPadList, 'layout': numLayout, 'columns': 3},
            'op': {'buttons': operatorList, 'layout': opLayout, 'columns': 2},
            'constants': {'buttons': constantList, 'layout': constLayout, 'columns': 1},
            'functions': {'buttons': functionList, 'layout': funcLayout, 'columns': 1},
        }

        for label in buttonGroups.keys():
            r = 0; c = 0
            buttonPad = buttonGroups[label]
            for btnText in buttonPad['buttons']:
                button = Button(btnText, self.buttonClicked)
                buttonPad['layout'].addWidget(button, r, c)
                c += 1
                if c >= buttonPad['columns']:
                    c = 0; r += 1

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addLayout(displayLayout, 0, 0, 1, 0)
        mainLayout.addLayout(numLayout, 1, 0)
        mainLayout.addLayout(opLayout, 1, 1)
        mainLayout.addLayout(constLayout, 2, 0)
        mainLayout.addLayout(funcLayout, 2, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("My Calculator")


    def buttonClicked(self):
        display = self.displayResult
        status = self.displayStatus
        currentInput = self.displayCurrentInput
        button = self.sender()
        key = button.text()

        if "Error" in status.text():
            self.clearDisplays()
        elif display.text() and key in operatorList[:4]:
            pass
        elif display.text() and status.text() is "":
            self.clearDisplays()

        if key == '=':
            try:
                result = eval(str(display.text()) + str(status.text()) + str(currentInput.text()))
                display.setText(str(result))
                status.clear()
                currentInput.clear()
            except:
                status.setText('Error : 잘못된 수식입니다!')

        elif key == 'C':
            display.clear()
            status.clear()
            currentInput.clear()

        elif key in constantList:
            self.display.setText(self.display.text() + connectionWithConstants[key])

        elif key in functionList:
            for i in range(len(self.display.text())-1, -1, -1):
                if self.display.text()[i] not in numPadList:
                    n = self.display.text()[i:]
                    self.display.setText(self.display.text()[:i+1])
                    break
            self.display.setText(self.display.text() + connectionWithFunctions(n)[key])
        elif key in operatorList[:4]:
            display.setText(currentInput.text())
            status.setText(key)
            currentInput.clear()

        else:
            currentInput.setText(currentInput.text() + key)

    def clearDisplays(self):
        self.displayResult.clear()
        self.displayStatus.clear()
        self.displayCurrentInput.clear()



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

