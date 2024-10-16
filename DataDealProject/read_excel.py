import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QFileDialog

def read_excel_file(self):
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)",
                                               options=options)
    if file_name:
        try:
            df = pd.read_excel(file_name)
            df = df.to_numpy()
            return df  # 返回 DataFrame
        except Exception as e:
            print(f"Error reading file: {e}")
            return None  # 如果读取失败，返回 None
