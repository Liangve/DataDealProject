import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from secondary_window import SecondaryWindow  # 确保导入正确

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("No data received", self)
        self.label.setGeometry(50, 50, 200, 50)

        self.button = QPushButton("Open Secondary Window", self)
        self.button.setGeometry(50, 100, 200, 50)
        self.button.clicked.connect(self.open_secondary_window)

    def open_secondary_window(self):
        self.secondary_window = SecondaryWindow()
        self.secondary_window.data_signal.connect(self.update_label)
        self.secondary_window.show()

    def update_label(self, data_array):
        if isinstance(data_array, np.ndarray):
            data_str = ', '.join(data_array.astype(str))
            self.label.setText(f"Received: {data_str}")
        else:
            self.label.setText("Invalid data type")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
