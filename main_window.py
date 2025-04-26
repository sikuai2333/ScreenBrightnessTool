import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QSlider, QLabel, QPushButton, QCheckBox, QGroupBox, 
                            QApplication, QSystemTrayIcon, QMenu, QAction,
                            QTimeEdit, QGridLayout, QSpinBox, QComboBox, QShortcut,
                            QColorDialog, QFrame)
from PyQt5.QtCore import Qt, QSettings, QTime, QTimer
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QColor

class ColorPickerButton(QPushButton):
    """颜色选择按钮"""
    def __init__(self, title, initial_color=None, parent=None):
        super(ColorPickerButton, self).__init__(title, parent)
        
        self.color = initial_color or QColor(30, 30, 30, 180)
        self.clicked.connect(self.pick_color)
        self.update_button_color()
    
    def pick_color(self):
        """打开颜色选择对话框"""
        color = QColorDialog.getColor(self.color, self, "选择颜色", QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.color = color
            self.update_button_color()
            self.update_color()
    
    def update_button_color(self):
        """更新按钮显示颜色"""
        # 创建一个彩色框显示当前颜色
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({self.color.red()}, {self.color.green()}, {self.color.blue()}, {self.color.alpha()});
                color: {'black' if self.color.lightness() > 128 else 'white'};
                border: 1px solid #555;
                padding: 5px;
                min-width: 80px;
            }}
        """)
    
    def update_color(self):
        """子类实现此方法来处理颜色更新"""
        pass
    
    def get_color(self):
        """获取当前颜色"""
        return self.color

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # 初始化设置
        self.settings = QSettings("BrightnessControl", "BrightnessAdjuster")
        self.brightness_value = self.settings.value("brightness", 100, type=int)
        self.auto_start = self.settings.value("auto_start", False, type=bool)
        self.blue_light_filter = self.settings.value("blue_light_filter", False, type=bool)
        self.timer_enabled = self.settings.value("timer_enabled", False, type=bool)
        self.timer_time = self.settings.value("timer_time", QTime(22, 0), type=QTime)
        self.timer_mode = self.settings.value("timer_mode", 0, type=int)
        
        # 设置应用图标
        self.app_icon = self.load_icon()
        if self.app_icon:
            self.setWindowIcon(self.app_icon)
        
        # 设置自定义热键
        self.exit_shortcut = self.settings.value("exit_shortcut", "Ctrl+E", type=str)
        
        # 获取悬浮球颜色设置
        self.float_bg_color = self.settings.value("float_bg_color", QColor(30, 30, 30, 180))
        if isinstance(self.float_bg_color, str):
            self.float_bg_color = QColor(self.float_bg_color)
        
        self.float_text_color = self.settings.value("float_text_color", QColor(255, 255, 255))
        if isinstance(self.float_text_color, str):
            self.float_text_color = QColor(self.float_text_color)
        
        # 设置窗口属性
        self.setWindowTitle("屏幕亮度调节工具")
        self.setFixedSize(500, 550)  # 增加窗口高度以适应新功能
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建亮度调节组
        self.brightness_group = QGroupBox("屏幕亮度调节")
        self.brightness_layout = QVBoxLayout()
        
        # 亮度滑动条和标签
        self.slider_layout = QHBoxLayout()
        
        self.brightness_label = QLabel("亮度:")
        self.brightness_label.setFont(QFont("Arial", 10))
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(10)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(self.brightness_value)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.setTickInterval(10)
        
        self.brightness_value_label = QLabel(f"{self.brightness_value}%")
        self.brightness_value_label.setMinimumWidth(40)
        
        self.slider_layout.addWidget(self.brightness_label)
        self.slider_layout.addWidget(self.brightness_slider)
        self.slider_layout.addWidget(self.brightness_value_label)
        
        # 显示模式选项
        self.display_options_layout = QHBoxLayout()
        
        # 高对比度模式选项
        self.high_contrast_checkbox = QCheckBox("增强对比度")
        
        # 防蓝光模式选项
        self.blue_light_checkbox = QCheckBox("防蓝光模式")
        self.blue_light_checkbox.setChecked(self.blue_light_filter)
        
        self.display_options_layout.addWidget(self.high_contrast_checkbox)
        self.display_options_layout.addWidget(self.blue_light_checkbox)
        
        # 添加到亮度调节组
        self.brightness_layout.addLayout(self.slider_layout)
        self.brightness_layout.addLayout(self.display_options_layout)
        self.brightness_group.setLayout(self.brightness_layout)
        
        # 模式按钮组
        self.modes_group = QGroupBox("屏幕亮度切换")
        self.modes_layout = QHBoxLayout()
        
        self.normal_mode_btn = QPushButton("正常模式")
        self.dim_mode_btn = QPushButton("护眼模式")
        self.night_mode_btn = QPushButton("夜间模式")
        self.custom_mode_btn = QPushButton("自定模式")
        
        self.modes_layout.addWidget(self.normal_mode_btn)
        self.modes_layout.addWidget(self.dim_mode_btn)
        self.modes_layout.addWidget(self.night_mode_btn)
        self.modes_layout.addWidget(self.custom_mode_btn)
        
        self.modes_group.setLayout(self.modes_layout)
        
        # 悬浮球设置组
        self.float_group = QGroupBox("悬浮窗设置")
        self.float_layout = QGridLayout()
        
        # 显示悬浮球选项
        self.floating_btn_checkbox = QCheckBox("显示悬浮窗")
        self.floating_btn_checkbox.setChecked(self.settings.value("show_floating_button", True, type=bool))
        
        # 背景颜色选择
        self.float_bg_color_label = QLabel("背景颜色:")
        
        class BgColorButton(ColorPickerButton):
            def __init__(self, parent_window, initial_color):
                super(BgColorButton, self).__init__("选择", initial_color, parent_window)
                self.parent_window = parent_window
            
            def update_color(self):
                # 更新背景颜色
                self.parent_window.float_bg_color = self.color
                # 如果悬浮球已经创建，更新颜色
                if self.parent_window.floating_button:
                    self.parent_window.floating_button.set_colors(
                        self.parent_window.float_bg_color,
                        self.parent_window.float_text_color
                    )
        
        self.float_bg_color_btn = BgColorButton(self, self.float_bg_color)
        
        # 文字颜色选择
        self.float_text_color_label = QLabel("文字颜色:")
        
        class TextColorButton(ColorPickerButton):
            def __init__(self, parent_window, initial_color):
                super(TextColorButton, self).__init__("选择", initial_color, parent_window)
                self.parent_window = parent_window
            
            def update_color(self):
                # 更新文字颜色
                self.parent_window.float_text_color = self.color
                # 如果悬浮球已经创建，更新颜色
                if self.parent_window.floating_button:
                    self.parent_window.floating_button.set_colors(
                        self.parent_window.float_bg_color,
                        self.parent_window.float_text_color
                    )
        
        self.float_text_color_btn = TextColorButton(self, self.float_text_color)
        
        # 将选项添加到布局
        self.float_layout.addWidget(self.floating_btn_checkbox, 0, 0, 1, 2)
        self.float_layout.addWidget(self.float_bg_color_label, 1, 0)
        self.float_layout.addWidget(self.float_bg_color_btn, 1, 1)
        self.float_layout.addWidget(self.float_text_color_label, 2, 0)
        self.float_layout.addWidget(self.float_text_color_btn, 2, 1)
        
        self.float_group.setLayout(self.float_layout)
        
        # 定时功能组
        self.timer_group = QGroupBox("定时切换")
        self.timer_layout = QGridLayout()
        
        self.timer_checkbox = QCheckBox("启用定时切换")
        self.timer_checkbox.setChecked(self.timer_enabled)
        
        self.timer_time_label = QLabel("定时时间:")
        self.timer_time_edit = QTimeEdit()
        self.timer_time_edit.setTime(self.timer_time)
        self.timer_time_edit.setDisplayFormat("HH:mm")
        
        self.timer_mode_label = QLabel("定时模式:")
        self.timer_mode_combo = QComboBox()
        self.timer_mode_combo.addItems(["护眼模式", "夜间模式", "防蓝光模式"])
        self.timer_mode_combo.setCurrentIndex(self.timer_mode)
        
        # 第一行：启用定时
        self.timer_layout.addWidget(self.timer_checkbox, 0, 0, 1, 2)
        
        # 第二行：定时时间
        self.timer_layout.addWidget(self.timer_time_label, 1, 0)
        self.timer_layout.addWidget(self.timer_time_edit, 1, 1)
        
        # 第三行：定时模式
        self.timer_layout.addWidget(self.timer_mode_label, 2, 0)
        self.timer_layout.addWidget(self.timer_mode_combo, 2, 1)
        
        self.timer_group.setLayout(self.timer_layout)
        
        # 热键设置组
        self.hotkey_group = QGroupBox("热键设置")
        self.hotkey_layout = QGridLayout()
        
        self.exit_hotkey_label = QLabel("退出程序热键:")
        self.exit_hotkey_combo = QComboBox()
        self.exit_hotkey_combo.addItems(["Ctrl+E", "Ctrl+Q", "Alt+F4", "自定义"])
        
        # 设置当前值
        if self.exit_shortcut == "Ctrl+E":
            self.exit_hotkey_combo.setCurrentIndex(0)
        elif self.exit_shortcut == "Ctrl+Q":
            self.exit_hotkey_combo.setCurrentIndex(1)
        elif self.exit_shortcut == "Alt+F4":
            self.exit_hotkey_combo.setCurrentIndex(2)
        else:
            self.exit_hotkey_combo.setCurrentIndex(3)
        
        self.hotkey_layout.addWidget(self.exit_hotkey_label, 0, 0)
        self.hotkey_layout.addWidget(self.exit_hotkey_combo, 0, 1)
        
        self.hotkey_group.setLayout(self.hotkey_layout)
        
        # 底部按钮区域
        self.bottom_layout = QHBoxLayout()
        
        self.autostart_checkbox = QCheckBox("开机自启动")
        self.autostart_checkbox.setChecked(self.auto_start)
        
        self.reset_btn = QPushButton("恢复默认")
        self.apply_btn = QPushButton("应用设置")
        
        self.bottom_layout.addWidget(self.autostart_checkbox)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.reset_btn)
        self.bottom_layout.addWidget(self.apply_btn)
        
        # 添加所有组件到主布局
        self.main_layout.addWidget(self.brightness_group)
        self.main_layout.addWidget(self.modes_group)
        self.main_layout.addWidget(self.float_group)
        self.main_layout.addWidget(self.timer_group)
        self.main_layout.addWidget(self.hotkey_group)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_layout)
        
        # 连接信号和槽
        self.brightness_slider.valueChanged.connect(self.update_brightness)
        self.normal_mode_btn.clicked.connect(lambda: self.set_brightness_mode(100))
        self.dim_mode_btn.clicked.connect(lambda: self.set_brightness_mode(70))
        self.night_mode_btn.clicked.connect(lambda: self.set_brightness_mode(40))
        self.reset_btn.clicked.connect(self.reset_settings)
        self.apply_btn.clicked.connect(self.apply_settings)
        self.autostart_checkbox.toggled.connect(self.toggle_autostart)
        self.blue_light_checkbox.toggled.connect(self.toggle_blue_light)
        self.floating_btn_checkbox.toggled.connect(self.toggle_floating_button)
        self.timer_checkbox.toggled.connect(self.toggle_timer)
        self.exit_hotkey_combo.currentIndexChanged.connect(self.update_exit_hotkey)
        
        # 系统托盘图标
        self.setup_tray_icon()
        
        # 设置热键
        self.setup_shortcuts()
        
        # 定时器
        self.setup_timer()

        # 悬浮按钮引用
        self.floating_button = None
    
    def load_icon(self):
        """加载应用图标"""
        # 尝试从不同路径加载图标
        icon_paths = [
            "icon.png",                     # 根目录
            os.path.join("images", "icon.png"),  # images文件夹
            os.path.join("resources", "icon.png"),  # resources文件夹
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")  # 脚本所在目录
        ]
        
        for path in icon_paths:
            if os.path.exists(path):
                return QIcon(path)
        
        return None
    
    def update_brightness(self, value):
        self.brightness_value = value
        self.brightness_value_label.setText(f"{value}%")
        # 信号会连接到亮度控制类来实际改变亮度
    
    def set_brightness_mode(self, value):
        self.brightness_slider.setValue(value)
    
    def toggle_autostart(self, state):
        self.auto_start = state
        # 实现开机自启动的逻辑
    
    def toggle_blue_light(self, state):
        self.blue_light_filter = state
        # 蓝光过滤与高对比度模式互斥
        if state and self.high_contrast_checkbox.isChecked():
            self.high_contrast_checkbox.setChecked(False)
    
    def toggle_floating_button(self, state):
        # 悬浮按钮显示/隐藏由主程序控制
        # 这里设置的是"是否启用悬浮按钮功能"，而不是立即显示/隐藏
        if self.floating_button:
            if not state:
                # 如果禁用了悬浮按钮功能，则隐藏悬浮按钮
                self.floating_button.hide()
    
    def toggle_timer(self, state):
        self.timer_enabled = state
        self.timer_time_edit.setEnabled(state)
        self.timer_mode_combo.setEnabled(state)
    
    def update_exit_hotkey(self, index):
        # 根据选择的索引更新退出热键
        if index == 0:
            self.exit_shortcut = "Ctrl+E"
        elif index == 1:
            self.exit_shortcut = "Ctrl+Q"
        elif index == 2:
            self.exit_shortcut = "Alt+F4"
        else:
            # 自定义热键，可以在这里添加一个对话框让用户自定义
            self.exit_shortcut = "Ctrl+E"  # 默认使用Ctrl+E
        
        # 重新设置热键
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        # 清除已有的快捷键
        if hasattr(self, 'exit_key_sequence'):
            self.exit_key_sequence.deleteLater()
        
        # 设置退出快捷键
        self.exit_key_sequence = QShortcut(QKeySequence(self.exit_shortcut), self)
        self.exit_key_sequence.activated.connect(self.close_application)
    
    def setup_timer(self):
        # 创建定时器
        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self.check_scheduled_tasks)
        self.scheduler_timer.start(60000)  # 每分钟检查一次
    
    def check_scheduled_tasks(self):
        # 检查是否开启了定时功能且时间到了
        if not self.timer_enabled:
            return
        
        current_time = QTime.currentTime()
        scheduled_time = self.timer_time_edit.time()
        
        # 如果当前时间与设定时间的小时和分钟相同
        if current_time.hour() == scheduled_time.hour() and current_time.minute() == scheduled_time.minute():
            # 根据选择的模式执行对应操作
            mode_index = self.timer_mode_combo.currentIndex()
            if mode_index == 0:  # 护眼模式
                self.set_brightness_mode(70)
                self.blue_light_checkbox.setChecked(False)
                self.high_contrast_checkbox.setChecked(False)
            elif mode_index == 1:  # 夜间模式
                self.set_brightness_mode(40)
                self.blue_light_checkbox.setChecked(False)
                self.high_contrast_checkbox.setChecked(False)
            elif mode_index == 2:  # 防蓝光模式
                self.blue_light_checkbox.setChecked(True)
                self.high_contrast_checkbox.setChecked(False)
    
    def reset_settings(self):
        self.brightness_slider.setValue(100)
        self.high_contrast_checkbox.setChecked(False)
        self.blue_light_checkbox.setChecked(False)
        self.autostart_checkbox.setChecked(False)
        self.timer_checkbox.setChecked(False)
        self.timer_time_edit.setTime(QTime(22, 0))
        self.timer_mode_combo.setCurrentIndex(0)
        self.exit_hotkey_combo.setCurrentIndex(0)
        self.floating_btn_checkbox.setChecked(True)
        
        # 重置悬浮球颜色设置
        self.float_bg_color = QColor(30, 30, 30, 180)
        self.float_text_color = QColor(255, 255, 255)
        self.float_bg_color_btn.color = self.float_bg_color
        self.float_text_color_btn.color = self.float_text_color
        self.float_bg_color_btn.update_button_color()
        self.float_text_color_btn.update_button_color()
        
        # 更新悬浮球颜色
        if self.floating_button:
            self.floating_button.set_colors(self.float_bg_color, self.float_text_color)
    
    def apply_settings(self):
        # 保存设置
        self.settings.setValue("brightness", self.brightness_value)
        self.settings.setValue("auto_start", self.auto_start)
        self.settings.setValue("blue_light_filter", self.blue_light_filter)
        self.settings.setValue("timer_enabled", self.timer_enabled)
        self.settings.setValue("timer_time", self.timer_time_edit.time())
        self.settings.setValue("timer_mode", self.timer_mode_combo.currentIndex())
        self.settings.setValue("exit_shortcut", self.exit_shortcut)
        self.settings.setValue("show_floating_button", self.floating_btn_checkbox.isChecked())
        
        # 保存悬浮球颜色设置
        self.settings.setValue("float_bg_color", self.float_bg_color)
        self.settings.setValue("float_text_color", self.float_text_color)
        
        self.settings.sync()
    
    def setup_tray_icon(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        
        # 设置图标
        if self.app_icon:
            self.tray_icon.setIcon(self.app_icon)
        else:
            # 尝试使用系统默认图标或创建一个简单的空白图标
            blank_icon = QIcon()
            blank_icon.addPixmap(QIcon.fromTheme("application-x-executable").pixmap(128, 128))
            self.tray_icon.setIcon(blank_icon)
        
        self.tray_icon.setToolTip("屏幕亮度调节工具")
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show)
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.close_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def closeEvent(self, event):
        # 点击关闭按钮时最小化到系统托盘而不是退出
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("屏幕亮度调节工具", "程序已最小化到系统托盘", QSystemTrayIcon.Information, 2000)
        
        # 如果启用了悬浮按钮功能，则显示悬浮按钮
        if self.floating_button and self.floating_btn_checkbox.isChecked():
            self.floating_button.show()
    
    def showEvent(self, event):
        # 窗口显示时隐藏悬浮按钮
        if self.floating_button:
            self.floating_button.hide()
        super(MainWindow, self).showEvent(event)
    
    def hideEvent(self, event):
        # 窗口隐藏时显示悬浮按钮
        if self.floating_button and self.floating_btn_checkbox.isChecked():
            self.floating_button.show()
        super(MainWindow, self).hideEvent(event)
    
    def close_application(self):
        # 真正退出应用程序
        self.apply_settings()  # 保存设置
        QApplication.quit()
    
    def set_floating_button(self, button):
        # 设置悬浮按钮引用
        self.floating_button = button
        
        # 设置悬浮球的初始颜色
        if self.floating_button:
            self.floating_button.set_colors(self.float_bg_color, self.float_text_color)


# 添加QShortcut类
from PyQt5.QtWidgets import QShortcut 