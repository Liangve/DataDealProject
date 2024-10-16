import io
import numpy as np
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QApplication, QGraphicsLineItem
from matplotlib import pyplot as plt
from shoudongshuru import MatrixInputApp
from uimain import Ui_Form
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from read_excel import read_excel_file
from read_image import load_image,process_image
from zhengtai import CurvePlotter
from junzhibaoluo import DataPlotter3
from shangbaoluo import DataPlotter
from xiabaoluo import DataPlotter2

class MyMainForm(QMainWindow, Ui_Form,DataPlotter):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_changed)
        self.comboBox_2.currentIndexChanged.connect(self.on_comboBox_2_changed)
        self.comboBox_3.currentIndexChanged.connect(self.on_comboBox_3_changed)
        self.comboBox_4.currentIndexChanged.connect(self.on_comboBox_4_changed)
        self.pushButton_30.clicked.connect(self.Push_Button_30)  # 连接按钮事件
        self.pushButton_30.clicked.connect(self.showSelectedItems1)
        self.pushButton_3.clicked.connect(self.Push_Button_3)


    def showSelectedItems(self):
        selected_items = self.comboBox_17.checkedItems()  # 获取选中的项
        print("Selected items:", selected_items)
        self.Push_Button_30(selected_items)
        print("Selected items:", selected_items)  # 打印选中的项

    def showSelectedItems1(self):
        selected_items = self.comboBox_18.checkedItems()  # 获取选中的项
        print("Selected items:", selected_items)  # 打印选中的项
    def on_comboBox_changed(self, index):
        if index == 1:  # 读取图像
            self.image_path = load_image(self)
            self.df = process_image(self.image_path)
            self.X = self.df[:, 0]
            self.Y = self.df[:, 1]
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
        self.df = data_array
        print(data_array)

    def on_comboBox_2_changed(self, index):
        if index == 1:
            self.Df = self.df.T # 默认纵向排列
            print(f"矩阵已成功赋值：{self.Df}")
        elif index == 2:
            self.Df = self.df
            print(f"矩阵已成功赋值：{self.Df}")

    def on_comboBox_3_changed(self, index):
        if index == 1:
            self.X = self.Df[:, 0]  # 默认纵向排列
        elif index == 2:
            self.X = self.Df[:, 1]  # 默认纵向排列
        print(f"X列数据已成功赋值：{self.X}")

    def on_comboBox_4_changed(self, index):
        if index == 1:
            self.Y = self.Df[:, 0]  # 默认纵向排列
        elif index == 2:
            self.Y = self.Df[:, 1]  # 默认纵向排列
        print(f"Y列数据已成功赋值：{self.Y}")

    def Push_Button_30(self):
        selected_items = self.comboBox_17.checkedItems()

        DD = DataPlotter.plot_data(self)
        DD2 = DataPlotter2.plot_data(self)
        DD3 = DataPlotter3.plot_data(self)
        if hasattr(self, 'X') and hasattr(self, 'Y') and len(self.X) == len(self.Y):
            # 创建一个新的图像和绘图区域
            fig, ax = plt.subplots()
            ax.plot(self.X, self.Y, color='black', marker='o', linestyle='-', linewidth=0.4, markersize=0.8)
            if '上包络线' in selected_items:
                ax.plot(DD.x_spline, DD.y_spline, color='blue', marker='o', linestyle='-', linewidth=0.4,
                    markersize=0.8)
            if '下包络线' in selected_items:
                ax.plot(DD2.x_spline, DD2.y_spline, color='blue', marker='o', linestyle='-', linewidth=0.4,
                        markersize=0.8)
            if '均值包络线' in selected_items:
                ax.plot(DD3.x_spline, DD3.y_mean, color='blue', marker='o', linestyle='-', linewidth=0.4, markersize=0.8)

            # 绘制点和线
            #ax.plot(DD.x_spline, DD.y_spline,color='blue', marker='o', linestyle='-',linewidth=0.4, markersize=0.8)
            #绘制均值包络线

            #傅里叶变换

            # 设置坐标轴标签和标题（可选）
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Plot of X and Y')

            # 翻转y轴方向以匹配QGraphicsView的坐标系
            # ax.invert_yaxis()

            # 将matplotlib图像渲染为缓冲区
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)

            # 使用QImage加载缓冲区的PNG图像数据
            image = QImage()
            image.loadFromData(buf.getvalue())

            # 将QImage转换为QPixmap并显示在QGraphicsView中
            pixmap = QPixmap.fromImage(image)
            self.scene = QGraphicsScene()
            self.scene.addPixmap(pixmap)

            # 将scene设置到graphicsView
            self.graphicsView.setScene(self.scene)
            self.graphicsView_6.setScene(self.scene)
            self.graphicsView_7.setScene(self.scene)

            # 释放资源
            buf.close()
            plt.close(fig)

    def Push_Button_3(self):
        if hasattr(self, 'X') and hasattr(self, 'Y') and len(self.X) == len(self.Y):
            # 创建一个新的图像和绘图区域
            fig, ax = plt.subplots()

            # 绘制点和线
            ax.plot(self.X, self.Y,color='black', marker='o', linestyle='-',linewidth=0.4, markersize=0.8)

            # 设置坐标轴标签和标题（可选）
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Plot of X and Y')

            # 翻转y轴方向以匹配QGraphicsView的坐标系
            # ax.invert_yaxis()

            # 将matplotlib图像渲染为缓冲区
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)

            # 使用QImage加载缓冲区的PNG图像数据
            image = QImage()
            image.loadFromData(buf.getvalue())

            # 将QImage转换为QPixmap并显示在QGraphicsView中
            pixmap = QPixmap.fromImage(image)
            self.scene = QGraphicsScene()
            self.scene.addPixmap(pixmap)

            # 将scene设置到graphicsView
            self.graphicsView.setScene(self.scene)
            self.graphicsView_6.setScene(self.scene)
            self.graphicsView_7.setScene(self.scene)

            # 释放资源
            buf.close()
            plt.close(fig)
        else:
            print("X或Y尚未赋值或长度不一致")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
