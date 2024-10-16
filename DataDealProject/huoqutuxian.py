import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt

class CurveRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = '曲线识别应用'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
        self.image_path = None
        self.curve_points = None

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 布局
        layout = QVBoxLayout()

        # 加载图像按钮
        self.load_button = QPushButton('加载图像', self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        # 显示图像的标签
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        # 处理图像按钮（移动到底部）
        self.process_button = QPushButton('处理图像', self)
        self.process_button.clicked.connect(self.process_image)
        layout.addWidget(self.process_button)

        # 设置中央小部件
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "",
                                                   "所有文件 (*);;JPEG (*.jpg;*.jpeg);;PNG (*.png)", options=options)
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)

    def process_image(self):
        if not self.image_path:
            return

        # 设置字体以支持中文
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

        # 读取图像
        img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        # 阈值分割
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        # 查找轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 确保找到轮廓
        if contours:
            # 假设最大的轮廓是曲线
            largest_contour = max(contours, key=cv2.contourArea)

            # 提取轮廓中的点并存储为numpy.ndarray
            self.curve_points = largest_contour[:, 0, :]
            ab = self.curve_points

            # 绘制轮廓以供验证
            output_img = np.zeros_like(img)
            cv2.drawContours(output_img, [largest_contour], -1, (255, 255, 255), thickness=1)

            # 将散点绘制在图像上
            for point in self.curve_points:
                cv2.circle(output_img, (point[0], point[1]), 1, (255, 255, 255), -1)

            # 显示识别到的散点图
            plt.imshow(output_img, cmap='gray')
            plt.title('识别的散点图')
            plt.show()

            # 打印识别点
            print("识别出的点 (numpy.ndarray):", ab)
        else:
            print("未找到任何轮廓。")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CurveRecognitionApp()
    ex.show()
    sys.exit(app.exec_())


