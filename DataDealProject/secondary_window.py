import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import pyqtSignal

class SecondaryWindow(QMainWindow):
    data_signal = pyqtSignal(object)  # 使用 object 来传递 numpy.ndarray

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Secondary Window")
        self.setGeometry(100, 100, 300, 200)

        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(50, 50, 200, 50)

        self.button = QPushButton("Send Data", self)
        self.button.setGeometry(50, 100, 200, 50)
        self.button.clicked.connect(self.send_data)

    def send_data(self):
        # 获取文本输入框中的文本并转换为 numpy 数组
        data_str = self.line_edit.text()
        data_array = np.array([data_str])  # 简单示例，将字符串放入数组中
        self.data_signal.emit(data_array)
        self.close()
