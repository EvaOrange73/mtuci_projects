import re
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton

from stylesheet import style


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_operations = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_operations)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_result)

        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        self.b_1 = QPushButton("1", self)
        self.hbox_first.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_first.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_first.addWidget(self.b_3)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_7 = QPushButton("7", self)
        self.hbox_third.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_third.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_third.addWidget(self.b_9)

        self.b_plus = QPushButton("+", self)
        self.hbox_operations.addWidget(self.b_plus)

        self.b_minus = QPushButton("-", self)
        self.hbox_operations.addWidget(self.b_minus)

        self.b_multiply = QPushButton("*", self)
        self.hbox_operations.addWidget(self.b_multiply)

        self.b_divide = QPushButton("/", self)
        self.hbox_operations.addWidget(self.b_divide)

        self.b_0 = QPushButton("0", self)
        self.hbox_result.addWidget(self.b_0)

        self.b_dote = QPushButton(".", self)
        self.hbox_result.addWidget(self.b_dote)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_multiply.clicked.connect(lambda: self._operation("*"))
        self.b_divide.clicked.connect(lambda: self._operation("/"))
        self.b_result.clicked.connect(self._result)

        self.b_dote.clicked.connect(lambda: self._button("."))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))

    def _button(self, param):
        line = self.input.text()
        self.input.setText(line + param)

    def _operation(self, op):
        input_str = self.input.text()
        if input_str and input_str.count(".") < 2:
            if input_str[0] != '-':
                input_str = re.split("[+\-*/]", input_str)[0]
            else:
                input_str = '-' + re.split("[+\-*/]", input_str)[1]

            if re.search("\.", input_str):
                self.num_1 = float(input_str)
            else:
                self.num_1 = int(input_str)

            self.op = op
            self.input.setText(str(self.num_1) + str(self.op))

        elif op == '-':
            self.input.setText(op)
        else:
            self.input.setText("")

    def _result(self):
        input_str = self.input.text()
        if input_str and re.search("[+\-*/]", input_str[1:-1]) and input_str.count(".") < 3:
            input_str = re.split("[+\-*/]", input_str)[-1]

            if "." in input_str:
                if input_str.count(".") > 1:
                    self.input.setText("")
                    return
                self.num_2 = float(input_str)
            else:
                self.num_2 = int(input_str)

            result = ""
            if self.op == "+":
                result = self.num_1 + self.num_2
            elif self.op == "-":
                result = self.num_1 - self.num_2
            elif self.op == "*":
                result = self.num_1 * self.num_2
            elif self.op == "/":
                if self.num_2 == 0:
                    result = "на 0 делить нельзя"
                else:
                    result = self.num_1 / self.num_2

            if type(result) == float and int(result) == result:
                result = int(result)
            self.input.setText(str(result))
        else:
            self.input.setText("")


app = QApplication(sys.argv)

app.setStyleSheet(style)

win = Calculator()
win.show()

sys.exit(app.exec_())
