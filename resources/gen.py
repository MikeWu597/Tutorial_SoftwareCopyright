import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, 
    QPushButton, QFileDialog, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt

class FileMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件合并工具")
        self.setGeometry(100, 100, 500, 400)
        self.setAcceptDrops(True)
        
        # 创建UI组件
        self.list_widget = QListWidget()
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(False)
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        
        self.btn_generate = QPushButton("生成 source.txt")
        self.btn_clear = QPushButton("清空列表")
        self.btn_add = QPushButton("添加文件")
        
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.btn_clear)
        layout.addWidget(self.btn_add)
        self.setLayout(layout)
        
        # 连接信号
        self.btn_generate.clicked.connect(self.generate_file)
        self.btn_clear.clicked.connect(self.clear_list)
        self.btn_add.clicked.connect(self.add_files)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.add_file_to_list(file_path)
        event.acceptProposedAction()
    
    def add_file_to_list(self, file_path):
        # 检查文件是否已存在列表中
        if not any(self.list_widget.item(i).data(Qt.UserRole) == file_path 
                  for i in range(self.list_widget.count())):
            # 创建新的列表项
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)  # 存储完整路径
            self.list_widget.addItem(item)
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择文件", "", "所有文件 (*.*)"
        )
        for file in files:
            self.add_file_to_list(file)
    
    def clear_list(self):
        self.list_widget.clear()
    
    def generate_file(self):
        if self.list_widget.count() == 0:
            QMessageBox.warning(self, "警告", "文件列表为空！")
            return
        
        try:
            with open("source.txt", "w", encoding="utf-8") as output_file:
                for i in range(self.list_widget.count()):
                    file_path = self.list_widget.item(i).data(Qt.UserRole)
                    try:
                        with open(file_path, "r", encoding="utf-8") as input_file:
                            for line in input_file:
                                stripped_line = line.rstrip()
                                if stripped_line:  # 检查是否非空行
                                    output_file.write(stripped_line + "\n")
                    except UnicodeDecodeError:
                        # 尝试使用其他常见编码
                        try:
                            with open(file_path, "r", encoding="latin-1") as input_file:
                                for line in input_file:
                                    stripped_line = line.rstrip()
                                    if stripped_line:
                                        output_file.write(stripped_line + "\n")
                        except Exception as e:
                            QMessageBox.critical(
                                self, "错误", 
                                f"无法读取文件（编码问题）: {file_path}\n{str(e)}"
                            )
                            return
                    except Exception as e:
                        QMessageBox.critical(
                            self, "错误", 
                            f"读取文件时出错: {file_path}\n{str(e)}"
                        )
                        return
            
            QMessageBox.information(
                self, "成功", 
                f"文件已生成: source.txt\n位置: {os.getcwd()}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "错误", 
                f"写入输出文件时出错: {str(e)}"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileMergerApp()
    window.show()
    sys.exit(app.exec_())