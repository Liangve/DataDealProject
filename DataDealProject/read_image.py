import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt

def load_image(self):
    options = QFileDialog.Options()
    image_path, _ = QFileDialog.getOpenFileName(self, "打开图像", "", "图像文件 (*.png *.jpg *.bmp *.jpeg)",
                                               options=options)
    return image_path

def process_image(image_path):
        # 设置字体以支持中文
    plt.rcParams['font.family'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False

        # 读取图像
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # 阈值分割
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        # 查找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 确保找到轮廓
    if contours:
            # 假设最大的轮廓是曲线
        largest_contour = max(contours, key=cv2.contourArea)

            # 提取轮廓中的点并存储为numpy.ndarray
        curve_points = largest_contour[:, 0, :]
        ss = curve_points

            # 绘制轮廓以供验证
        output_img = np.zeros_like(img)
        cv2.drawContours(output_img, [largest_contour], -1, (255, 255, 255), thickness=1)

            # 将散点绘制在图像上
        for point in curve_points:
            cv2.circle(output_img, (point[0], point[1]), 1, (255, 255, 255), -1)

            # 显示识别到的散点图,翻转纵坐标
        plt.imshow(output_img, cmap='gray',origin='lower')
        plt.title('识别的散点图')
        plt.show()

        print("识别出的点 (numpy.ndarray):", curve_points)
        return ss
    else:
        print("未找到任何轮廓。")

# 示例调用
# 你需要在一个 QWidget 或 QMainWindow 的子类中调用这个函数
