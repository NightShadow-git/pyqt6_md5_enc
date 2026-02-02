# -*- coding: utf-8 -*-
"""
文件名：md5_enc.py
作者：[NightShadow]
日期：[2026/2/2 20:01]
描述：md5加密UI工具，pyqt6实现
"""

import sys
from PyQt6.QtGui import QIcon, QFontMetrics
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QLabel, QTextEdit, QMainWindow, QFrame
from hashlib import md5


def set_widget_text(widget_n, widget_text: str = None, size_n: int = 10, family_n: str = '宋体', bold_n: bool = False, italic_n: bool = False, underline_n: bool = False, overline_n: bool = False, strikeout_n: bool = False, measure_text_n: bool = False) -> None | tuple:
    """
    设置组件的字体样式，可以被设置字体的组件：label,button
    """
    widget_n.setText(widget_text)
    font_n = widget_n.font()
    font_n.setPointSize(size_n)
    font_n.setFamily(family_n)
    font_n.setItalic(italic_n)
    font_n.setBold(bold_n)
    font_n.setUnderline(underline_n)
    font_n.setOverline(overline_n)
    font_n.setStrikeOut(strikeout_n)
    widget_n.setFont(font_n)
    if measure_text_n:
        font_measure = QFontMetrics(font_n)
        return int(font_measure.horizontalAdvance(widget_text)), int(font_measure.height())
    else:
        return None


class Md5Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.none = None
        self.setGeometry(500, 200, 500, 400)
        self.setMinimumSize(320, 240)
        self.setWindowTitle('MD5加密')
        self.setWindowIcon(QIcon('md5.ico'))
        self.root_width = self.width()
        self.root_height = self.height()
        self.statu_bar = self.statusBar()
        self.statu_bar.show()
        self.set_ui()
        self.setup_connects()
        self.show()

    def set_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        input_area = self.create_input()
        main_layout.addWidget(input_area)

        control_area = self.create_control()
        main_layout.addWidget(control_area)

        output_area = self.create_output()
        main_layout.addWidget(output_area)

        button_area = self.create_button()
        main_layout.addWidget(button_area)

    def create_input(self):
        input_area = QWidget()
        layout = QVBoxLayout(input_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        input_label = QLabel()
        set_widget_text(input_label, '请输入要加密的内容:', size_n=10)
        layout.addWidget(input_label)

        self.input_text_edit = QTextEdit()
        self.input_text_edit.setMinimumHeight(30)
        self.input_text_edit.setFrameShape(QFrame.Shape.Box)
        set_widget_text(self.input_text_edit, None, size_n=12)
        self.input_text_edit.setPlaceholderText("在此输入需要MD5加密的内容...")
        layout.addWidget(self.input_text_edit)

        return input_area

    def create_control(self):
        control_area = QWidget()
        layout = QHBoxLayout(control_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.uper_checkbox = QRadioButton()
        set_widget_text(self.uper_checkbox, '输出大写', size_n=10)
        self.uper_checkbox.setToolTip('是否将加密结果转换为大写')
        layout.addWidget(self.uper_checkbox)

        layout.addStretch(1)

        self.char_count_label = QLabel()
        set_widget_text(self.char_count_label, '字符数: 0', size_n=10)
        self.char_count_label.setToolTip('输入字符数统计')
        layout.addWidget(self.char_count_label)

        return control_area

    def create_output(self):
        output_area = QWidget()
        layout = QVBoxLayout(output_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.output_edit = QTextEdit()
        self.output_edit.setFrameShape(QFrame.Shape.Box)
        set_widget_text(self.output_edit, None, size_n=12)
        self.output_edit.setMinimumHeight(30)
        self.output_edit.setPlaceholderText("加密结果将显示在这里...")
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        return output_area

    def create_button(self):
        button_area = QWidget()
        layout = QHBoxLayout(button_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        layout.addStretch(1)

        self.out_button = QPushButton()
        set_widget_text(self.out_button, '加密', size_n=11)
        self.out_button.setToolTip('加密输入')
        layout.addWidget(self.out_button)

        self.copy_button = QPushButton()
        set_widget_text(self.copy_button, '复制', size_n=11)
        self.copy_button.setToolTip('复制加密结果')
        layout.addWidget(self.copy_button)

        self.clear_button = QPushButton()
        set_widget_text(self.clear_button, '清空', size_n=11)
        self.clear_button.setToolTip('清空输入输出')
        layout.addWidget(self.clear_button)

        return button_area

    def is_uper(self):
        text = self.output_edit.toPlainText()
        if text:
            if self.uper_checkbox.isChecked():
                self.output_edit.setPlainText(text.upper())
            else:
                self.output_edit.setPlainText(text.lower())

    def update_char_count(self):
        text = self.input_text_edit.toPlainText()
        self.char_count_label.setText(f'字符数: {len(text)}')

    def encrypt_text(self):
        text = self.input_text_edit.toPlainText()
        if text:
            if self.uper_checkbox.isChecked():
                result = md5(text.encode()).hexdigest().upper()
            else:
                result = md5(text.encode()).hexdigest()
            self.output_edit.setPlainText(result)
            self.statu_bar.showMessage('加密成功', 1000)
        else:
            self.statu_bar.showMessage('没东西，你加密啥呢', 1000)

    def copy_text(self):
        text = self.output_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.statu_bar.showMessage('已复制到剪切板', 1000)
        else:
            self.statu_bar.showMessage('没东西，你复制啥呢', 1000)

    def clear_all(self):
        if not self.output_edit.toPlainText() and not self.input_text_edit.toPlainText():
            self.statu_bar.showMessage('没东西，你清空啥呢', 1000)
        else:
            self.input_text_edit.clear()
            self.output_edit.clear()
            self.statu_bar.showMessage('清空完成', 1000)

    def setup_connects(self):
        self.uper_checkbox.toggled.connect(self.is_uper)
        self.input_text_edit.textChanged.connect(self.update_char_count)
        self.out_button.clicked.connect(self.encrypt_text)
        self.copy_button.clicked.connect(self.copy_text)
        self.clear_button.clicked.connect(self.clear_all)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Md5Window()
    sys.exit(app.exec())
