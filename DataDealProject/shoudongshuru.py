import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal


class MatrixInputApp(QWidget):
    data_signal = pyqtSignal(object)  # 使用 object 来传递 pandas.DataFrame

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.configure_window()
        self.create_layout()
        self.create_widgets()
        self.set_layout()

    def configure_window(self):
        self.setWindowTitle('矩阵输入界面')
        self.resize(600, 400)

    def create_layout(self):
        self.layout = QVBoxLayout()

    def create_widgets(self):
        self.create_info_label()
        self.create_input_box()
        self.create_confirm_button()

    def create_info_label(self):
        self.label = QLabel('请按照矩阵形式手动输入参数。\n示例：a,a,a,a;b,b,b,b;', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

    def create_input_box(self):
        self.input_box = QLineEdit(self)
        self.input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.input_box)

    def create_confirm_button(self):
        self.button = QPushButton('确认', self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.on_confirm)

    def set_layout(self):
        self.setLayout(self.layout)

    def on_confirm(self):
        input_text = self.input_box.text()
        try:
            df = self.convert_to_dataframe(input_text)
            self.data_signal.emit(df)
            QMessageBox.information(self, '输入内容', f'您输入的矩阵参数是：\n{input_text}\n\n转换后的DataFrame：\n{df}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'转换失败，请检查输入格式。\n错误信息：\n{str(e)}')

    def convert_to_dataframe(self, input_text):
        rows = input_text.split(';')
        data = [row.split(',') for row in rows if row.strip()]
        df = pd.DataFrame(data)
        df = df.to_numpy()
        return df

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    app = QApplication(sys.argv)
    ex = MatrixInputApp()
    ex.show()
    sys.exit(app.exec_())
