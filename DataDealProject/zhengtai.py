import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.stats import chi2


class CurvePlotter(QMainWindow):
    data_signal = pyqtSignal(object)  # 使用 object 来传递 numpy.ndarray
    def __init__(self):
        super().__init__()
        self.initUI()
        self.xlim = None
        self.ylim = None
        self.points = None  # 用于保存曲线点的坐标
        global s
        s = "sss"
        # 设置字体以支持中文
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

    def initUI(self):
        self.setWindowTitle('曲线生成器')
        self.setGeometry(100, 100, 1000, 600)

        # 创建主部件和布局
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 创建曲线显示区
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # 创建按钮区
        control_layout = QVBoxLayout()
        self.button_layout = QGridLayout()

        self.btn_norm = QPushButton('正态分布', self)
        self.btn_norm.clicked.connect(self.plot_normal_distribution)
        self.button_layout.addWidget(self.btn_norm, 0, 0)

        self.norm_param_label = QLabel('标准差:', self)
        self.button_layout.addWidget(self.norm_param_label, 0, 1)

        self.norm_param_input = QLineEdit(self)
        self.norm_param_input.setText('1')
        self.button_layout.addWidget(self.norm_param_input, 0, 2)

        self.btn_chi = QPushButton('卡方分布', self)
        self.btn_chi.clicked.connect(self.plot_chi_distribution)
        self.button_layout.addWidget(self.btn_chi, 1, 0)

        self.chi_param_label = QLabel('自由度:', self)
        self.button_layout.addWidget(self.chi_param_label, 1, 1)

        self.chi_param_input = QLineEdit(self)
        self.chi_param_input.setText('2')
        self.button_layout.addWidget(self.chi_param_input, 1, 2)

        # 添加sin, cos, tan按钮及其参数输入框
        self.btn_sin = QPushButton('sin函数', self)
        self.btn_sin.clicked.connect(self.plot_sin_function)
        self.button_layout.addWidget(self.btn_sin, 2, 0)

        self.sin_param_label = QLabel('频率:', self)
        self.button_layout.addWidget(self.sin_param_label, 2, 1)

        self.sin_param_input = QLineEdit(self)
        self.sin_param_input.setText('1')
        self.button_layout.addWidget(self.sin_param_input, 2, 2)

        self.btn_cos = QPushButton('cos函数', self)
        self.btn_cos.clicked.connect(self.plot_cos_function)
        self.button_layout.addWidget(self.btn_cos, 3, 0)

        self.cos_param_label = QLabel('频率:', self)
        self.button_layout.addWidget(self.cos_param_label, 3, 1)

        self.cos_param_input = QLineEdit(self)
        self.cos_param_input.setText('1')
        self.button_layout.addWidget(self.cos_param_input, 3, 2)

        self.btn_tan = QPushButton('tan函数', self)
        self.btn_tan.clicked.connect(self.plot_tan_function)
        self.button_layout.addWidget(self.btn_tan, 4, 0)

        self.tan_param_label = QLabel('频率:', self)
        self.button_layout.addWidget(self.tan_param_label, 4, 1)

        self.tan_param_input = QLineEdit(self)
        self.tan_param_input.setText('1')
        self.button_layout.addWidget(self.tan_param_input, 4, 2)

        control_layout.addLayout(self.button_layout)
        control_layout.addStretch()

        self.btn_confirm = QPushButton('确定', self)
        self.btn_confirm.clicked.connect(self.update_plot)
        control_layout.addWidget(self.btn_confirm)

        self.btn_save = QPushButton('保存', self)
        self.btn_save.clicked.connect(self.save_points)

        control_layout.addWidget(self.btn_save)

        main_layout.addLayout(control_layout)


    def plot_normal_distribution(self):
        self.current_plot = 'normal'
        self.update_plot(initial=True)

    def plot_chi_distribution(self):
        self.current_plot = 'chi'
        self.update_plot(initial=True)

    def plot_sin_function(self):
        self.current_plot = 'sin'
        self.update_plot(initial=True)

    def plot_cos_function(self):
        self.current_plot = 'cos'
        self.update_plot(initial=True)

    def plot_tan_function(self):
        self.current_plot = 'tan'
        self.update_plot(initial=True)

    def update_plot(self, initial=False):
        self.figure.clear()
        ax = self.figure.add_subplot(111)


        if self.current_plot == 'normal':
            try:
                std_dev = float(self.norm_param_input.text())
                x = np.linspace(-5, 5, 200)
                y = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (x / std_dev) ** 2)
                ax.plot(x, y, label='正态分布')
                ax.set_title('正态分布')
                self.points = np.column_stack((x, y))
                ax.legend()
            except ValueError:
                pass  # Handle invalid input

        elif self.current_plot == 'chi':
            try:
                df = float(self.chi_param_input.text())
                x = np.linspace(0, 10, 200)
                y = chi2.pdf(x, df)
                ax.plot(x, y, label='卡方分布')
                ax.set_title('卡方分布')
                self.points = np.column_stack((x, y))
                ax.legend()
            except ValueError:
                pass  # Handle invalid input

        elif self.current_plot == 'sin':
            try:
                freq = float(self.sin_param_input.text())
                x = np.linspace(0, 10, 200)
                y = np.sin(2 * np.pi * freq * x)
                ax.plot(x, y, label='sin函数')
                ax.set_title('sin函数')
                self.points = np.column_stack((x, y))
                ax.legend()
            except ValueError:
                pass  # Handle invalid input

        elif self.current_plot == 'cos':
            try:
                freq = float(self.cos_param_input.text())
                x = np.linspace(0, 10, 200)
                y = np.cos(2 * np.pi * freq * x)
                ax.plot(x, y, label='cos函数')
                ax.set_title('cos函数')
                self.points = np.column_stack((x, y))
                ax.legend()
            except ValueError:
                pass  # Handle invalid input

        elif self.current_plot == 'tan':
            try:
                freq = float(self.tan_param_input.text())
                x = np.linspace(-np.pi / (2 * freq), np.pi / (2 * freq), 200)
                y = np.tan(2 * np.pi * freq * x)
                ax.plot(x, y, label='tan函数')
                ax.set_title('tan函数')
                self.points = np.column_stack((x, y))
                ax.legend()
            except ValueError:
                pass  # Handle invalid input

        # 保持坐标系不变
        if initial:
            self.xlim = ax.get_xlim()
            self.ylim = ax.get_ylim()
        else:
            ax.set_xlim(self.xlim)
            ax.set_ylim(self.ylim)

        self.canvas.draw()

    def save_points(self):
        if self.points is not None:
            rounded_points = np.round(self.points,4)
            np.set_printoptions(suppress=True)  # 禁用科学计数法
             # 简单示例，将字符串放入数组中
            self.data_signal.emit(rounded_points)
            #self.close()
            #print("保存的点的坐标为：")
            #print(rounded_points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = CurvePlotter()
    mainWin.show()
    sys.exit(app.exec_())
