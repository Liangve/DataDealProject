import io
import sys

import numpy as np
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QMainWindow, QApplication
from matplotlib import pyplot as plt

# 自定义类和模块的导入
from shoudongshuru import MatrixInputApp
from uimain import Ui_Form
from read_excel import read_excel_file
from read_image import load_image, process_image
from zhengtai import CurvePlotter
from shangbaoluo import DataPlotter

class MyMainForm(QMainWindow, Ui_Form, DataPlotter):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)  # 初始化UI
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_changed)  # 连接下拉框事件
        self.comboBox_2.currentIndexChanged.connect(self.on_comboBox_2_changed)
        self.comboBox_3.currentIndexChanged.connect(self.on_comboBox_3_changed)
        self.comboBox_4.currentIndexChanged.connect(self.on_comboBox_4_changed)
        self.comboBox_17.currentIndexChanged.connect(self.showSelectedItems)
        self.pushButton_3.clicked.connect(self.Push_Button_3)
        self.pushButton_30.clicked.connect(self.showSelectedItems)# 连接按钮事件
        self.pushButton_30.clicked.connect(self.showSelectedItems1)
        self.pushButton_2.clicked.connect(self.Push_Button_2)

    def showSelectedItems(self):
        selected_items = self.comboBox_17.checkedItems()  # 获取选中的项
        print("Selected items:", selected_items)  # 打印选中的项

    def showSelectedItems1(self):
        selected_items = self.comboBox_18.checkedItems()  # 获取选中的项
        print("Selected items:", selected_items)  # 打印选中的项
    def on_comboBox_changed(self, index):
        # 根据下拉框选择项执行不同的操作
        if index == 1:  # 读取图像
            self.image_path = load_image(self)
            self.df = process_image(self.image_path)
        elif index == 2:  # 读取文件
            self.df = read_excel_file(self)
        elif index == 3:  # 手动输入
            self.handle = MatrixInputApp()
            self.handle.data_signal.connect(self.update_label)
            self.handle.show()
        elif index == 4:  # 现有函数
            self.mainWin = CurvePlotter()
            self.mainWin.data_signal.connect(self.update_label)
            self.mainWin.show()

    def update_label(self, data_array):
        # 更新数据标签
        self.df = data_array
        print(data_array)

    def on_comboBox_2_changed(self, index):
        # 根据选定方向调整数据
        if index == 1:
            self.Df = self.df.T  # 列方向
            print(f"矩阵已成功赋值：{self.Df}")
        elif index == 2:
            self.Df = self.df
            print(f"矩阵已成功赋值：{self.Df}")

    def on_comboBox_3_changed(self, index):
        # 设置X轴数据
        if index == 1:
            self.X = self.Df[:, 0]
        elif index == 2:
            self.X = self.Df[:, 1]
        print(f"X列数据已成功赋值：{self.X}")

    def on_comboBox_4_changed(self, index):
        # 设置Y轴数据
        if index == 1:
            self.Y = self.Df[:, 0]
        elif index == 2:
            self.Y = self.Df[:, 1]
        print(f"Y列数据已成功赋值：{self.Y}")

    def Push_Button_2(self):
        # 缓存数据并绘制曲线
        DD = DataPlotter.plot_data(self)
        if hasattr(self, 'X') and hasattr(self, 'Y') and len(self.X) == len(self.Y):
            fig, ax = plt.subplots()
            ax.plot(DD.x_spline, DD.y_spline, color='blue', marker='o', linestyle='-', linewidth=0.4, markersize=0.8)
            ax.plot(self.X, self.Y, color='black', marker='o', linestyle='-', linewidth=0.4, markersize=0.8)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Plot of X and Y')

            # 将图像渲染为缓冲区
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)

            # 加载并显示图像
            image = QImage()
            image.loadFromData(buf.getvalue())
            pixmap = QPixmap.fromImage(image)
            self.scene = QGraphicsScene()
            self.scene.addPixmap(pixmap)

            # 设置场景到多个视图
            self.graphicsView.setScene(self.scene)
            self.graphicsView_6.setScene(self.scene)
            self.graphicsView_7.setScene(self.scene)

            # 释放资源
            buf.close()
            plt.close(fig)

    def Push_Button_3(self):
        # 绘制曲线
        if hasattr(self, 'X') and hasattr(self, 'Y') and len(self.X) == len(self.Y):
            fig, ax = plt.subplots()
            ax.plot(self.X, self.Y, color='black', marker='o', linestyle='-', linewidth=0.4, markersize=0.8)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Plot of X and Y')

            # 渲染图像并显示
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)

            image = QImage()
            image.loadFromData(buf.getvalue())
            pixmap = QPixmap.fromImage(image)
            self.scene = QGraphicsScene()
            self.scene.addPixmap(pixmap)

            self.graphicsView.setScene(self.scene)
            self.graphicsView_6.setScene(self.scene)
            self.graphicsView_7.setScene(self.scene)

            buf.close()
            plt.close(fig)
        else:
            print("X或Y尚未赋值或长度不一致")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
