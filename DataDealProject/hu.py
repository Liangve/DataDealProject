import numpy as np
import matplotlib.pyplot as plt

# 生成时间序列
time = np.linspace(0, 10, 100)  # 0到10秒，100个点

# 生成随机电压曲线
np.random.seed(42)
voltage = np.sin(time) + 0.5 * np.random.normal(size=time.shape)

# 绘制电压曲线
plt.figure(figsize=(10, 5))
plt.plot(time, voltage, color='k')  # 使用黑色（'k'）绘制曲线
plt.axis('off')  # 关闭坐标轴
plt.show()
