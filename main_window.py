import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QSlider, QLabel, QPushButton, QCheckBox, QGroupBox, 
                            QApplication, QSystemTrayIcon, QMenu, QAction,
                            QTimeEdit, QGridLayout, QSpinBox, QComboBox, QShortcut,
                            QColorDialog, QFrame)
from PyQt5.QtCore import Qt, QSettings, QTime, QTimer, QUrl
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QColor, QPalette
import webbrowser  # 使用Python标准库的webbrowser模块打开URL

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
        self.timer_end_time = self.settings.value("timer_end_time", QTime(6, 0), type=QTime)
        self.timer_mode = self.settings.value("timer_mode", 0, type=int)
        self.eye_protect_intensity = self.settings.value("eye_protect_intensity", 70, type=int)
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)  # 新增暗黑模式设置
        
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
        self.setFixedSize(500, 600)  # 增加窗口高度以适应新功能
        
        # 设置应用主题
        self.apply_theme()
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建亮度调节组
        self.brightness_group = QGroupBox("屏幕亮度调节")
        self.brightness_layout = QGridLayout()
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(10)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(self.brightness_value)
        self.brightness_slider.setFixedWidth(300)
        
        self.brightness_value_label = QLabel(f"{self.brightness_value}%")
        self.brightness_value_label.setStyleSheet("font-weight: bold;")
        
        # 第一行：亮度滑动条和数值
        self.brightness_layout.addWidget(QLabel("亮度:"), 0, 0)
        self.brightness_layout.addWidget(self.brightness_slider, 0, 1)
        self.brightness_layout.addWidget(self.brightness_value_label, 0, 2)
        
        # 护眼模式强度设置
        self.eye_protect_intensity_label = QLabel("护眼模式强度:")
        self.eye_protect_intensity_slider = QSlider(Qt.Horizontal)
        self.eye_protect_intensity_slider.setMinimum(30)  # 最低亮度为30%
        self.eye_protect_intensity_slider.setMaximum(90)  # 最高亮度为90%
        self.eye_protect_intensity_slider.setValue(self.eye_protect_intensity)
        self.eye_protect_intensity_slider.setFixedWidth(300)
        self.eye_protect_intensity_value_label = QLabel(f"{self.eye_protect_intensity}%")
        self.eye_protect_intensity_value_label.setStyleSheet("font-weight: bold;")
        
        # 第二行：护眼模式强度滑动条和数值
        self.brightness_layout.addWidget(self.eye_protect_intensity_label, 1, 0)
        self.brightness_layout.addWidget(self.eye_protect_intensity_slider, 1, 1)
        self.brightness_layout.addWidget(self.eye_protect_intensity_value_label, 1, 2)
        
        # 模式勾选框
        self.checkbox_layout = QHBoxLayout()
        self.high_contrast_checkbox = QCheckBox("增强对比度")
        self.high_contrast_checkbox.setChecked(self.settings.value("high_contrast", False, type=bool))
        self.blue_light_checkbox = QCheckBox("防蓝光模式")
        self.blue_light_checkbox.setChecked(self.blue_light_filter)
        
        self.checkbox_layout.addWidget(self.high_contrast_checkbox)
        self.checkbox_layout.addWidget(self.blue_light_checkbox)
        self.checkbox_layout.addStretch()
        
        # 第三行：特殊模式复选框
        self.brightness_layout.addLayout(self.checkbox_layout, 2, 0, 1, 3)
        
        self.brightness_group.setLayout(self.brightness_layout)
        
        # 预设模式
        self.modes_group = QGroupBox("预设模式")
        self.modes_layout = QHBoxLayout()
        
        self.normal_mode_btn = QPushButton("正常模式")
        self.normal_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #2c3e50;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #b0b0b0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        
        self.dim_mode_btn = QPushButton("护眼模式")
        self.dim_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #e6f5d0;
                color: #2c3e50;
                border: 1px solid #c5e5a0;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d6e5c0;
                border: 1px solid #b5d590;
            }
            QPushButton:pressed {
                background-color: #c6d5b0;
            }
        """)
        
        self.night_mode_btn = QPushButton("夜间模式")
        self.night_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #d0d9f5;
                color: #2c3e50;
                border: 1px solid #b0c0e5;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0c9e5;
                border: 1px solid #a0b0d5;
            }
            QPushButton:pressed {
                background-color: #b0b9d5;
            }
        """)
        
        self.modes_layout.addWidget(self.normal_mode_btn)
        self.modes_layout.addWidget(self.dim_mode_btn)
        self.modes_layout.addWidget(self.night_mode_btn)
        
        self.modes_group.setLayout(self.modes_layout)
        
        # 悬浮球设置组
        self.float_group = QGroupBox("悬浮窗设置")
        self.float_layout = QGridLayout()
        self.float_layout.setColumnStretch(1, 1)  # 让第二列自动扩展

        # 显示悬浮球选项
        self.floating_btn_checkbox = QCheckBox("显示悬浮窗")
        self.floating_btn_checkbox.setChecked(self.settings.value("show_floating_button", True, type=bool))

        # 背景颜色选择
        self.float_bg_color_label = QLabel("背景颜色:")
        self.float_bg_color_label.setMinimumWidth(80)  # 设置最小宽度
        
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
        self.float_text_color_label.setMinimumWidth(80)  # 设置最小宽度
        
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
        self.timer_layout.setColumnStretch(1, 1)  # 让第二列自动扩展
        self.timer_layout.setContentsMargins(10, 0, 10, 10)  # 设置边距：左、上、右、下

        self.timer_checkbox = QCheckBox("启用定时切换")
        self.timer_checkbox.setChecked(self.timer_enabled)

        self.timer_start_time_label = QLabel("开始时间:")
        self.timer_start_time_label.setMinimumWidth(80)  # 设置最小宽度
        self.timer_start_time_edit = QTimeEdit()
        self.timer_start_time_edit.setTime(self.timer_time)
        self.timer_start_time_edit.setDisplayFormat("HH:mm")

        self.timer_end_time_label = QLabel("结束时间:")
        self.timer_end_time_label.setMinimumWidth(80)  # 设置最小宽度
        self.timer_end_time_edit = QTimeEdit()
        self.timer_end_time_edit.setTime(self.timer_end_time)
        self.timer_end_time_edit.setDisplayFormat("HH:mm")

        self.timer_mode_label = QLabel("定时模式:")
        self.timer_mode_label.setMinimumWidth(80)  # 设置最小宽度
        self.timer_mode_combo = QComboBox()
        self.timer_mode_combo.addItems(["护眼模式", "夜间模式", "防蓝光模式"])
        self.timer_mode_combo.setCurrentIndex(self.timer_mode)
        
        # 第一行：启用定时
        self.timer_layout.addWidget(self.timer_checkbox, 0, 0, 1, 2)
        
        # 第二行：开始时间
        self.timer_layout.addWidget(self.timer_start_time_label, 1, 0)
        self.timer_layout.addWidget(self.timer_start_time_edit, 1, 1)
        
        # 第三行：结束时间
        self.timer_layout.addWidget(self.timer_end_time_label, 2, 0)
        self.timer_layout.addWidget(self.timer_end_time_edit, 2, 1)
        
        # 第四行：定时模式
        self.timer_layout.addWidget(self.timer_mode_label, 3, 0)
        self.timer_layout.addWidget(self.timer_mode_combo, 3, 1)
        
        self.timer_group.setLayout(self.timer_layout)
        
        # 热键设置组
        self.hotkey_group = QGroupBox("热键设置")
        self.hotkey_layout = QGridLayout()
        self.hotkey_layout.setColumnStretch(1, 1)  # 让第二列自动扩展

        self.exit_hotkey_label = QLabel("退出程序热键:")
        self.exit_hotkey_label.setMinimumWidth(100)  # 设置最小宽度
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
        
        # 添加外观设置组
        self.appearance_group = QGroupBox("外观设置")
        self.appearance_layout = QGridLayout()
        
        # 暗黑模式开关
        self.dark_mode_checkbox = QCheckBox("暗黑模式")
        self.dark_mode_checkbox.setChecked(self.dark_mode)
        self.dark_mode_checkbox.toggled.connect(self.toggle_dark_mode)
        
        # 添加区域选择模式选项
        self.area_mode_checkbox = QCheckBox("区域亮度调节")
        self.area_mode_checkbox.setChecked(self.settings.value("area_mode", False, type=bool))
        self.area_mode_checkbox.toggled.connect(self.toggle_area_mode)
        
        # 添加区域选择按钮
        self.select_area_btn = QPushButton("选择区域")
        self.select_area_btn.clicked.connect(self.start_area_selection)
        self.select_area_btn.setEnabled(self.area_mode_checkbox.isChecked())
        
        # 添加清除区域按钮
        self.clear_area_btn = QPushButton("清除区域")
        self.clear_area_btn.clicked.connect(self.clear_selected_area)
        self.clear_area_btn.setEnabled(self.area_mode_checkbox.isChecked())
        
        # 布局
        self.appearance_layout.addWidget(self.dark_mode_checkbox, 0, 0)
        self.appearance_layout.addWidget(self.area_mode_checkbox, 1, 0)
        self.appearance_layout.addWidget(self.select_area_btn, 1, 1)
        self.appearance_layout.addWidget(self.clear_area_btn, 1, 2)
        
        self.appearance_group.setLayout(self.appearance_layout)
        
        # 底部按钮区域
        self.bottom_layout = QHBoxLayout()
        
        self.autostart_checkbox = QCheckBox("开机自启动")
        self.autostart_checkbox.setChecked(self.auto_start)

        # 添加GitHub链接按钮
        self.github_btn = QPushButton("官方网站")
        self.github_btn.setIcon(self.app_icon if self.app_icon else QIcon())
        self.github_btn.setCursor(Qt.PointingHandCursor)

        self.reset_btn = QPushButton("恢复默认")
        self.apply_btn = QPushButton("应用设置")
        
        self.bottom_layout.addWidget(self.autostart_checkbox)
        self.bottom_layout.addWidget(self.github_btn)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.reset_btn)
        self.bottom_layout.addWidget(self.apply_btn)
        
        # 添加所有组件到主布局
        self.main_layout.addWidget(self.brightness_group)
        self.main_layout.addWidget(self.modes_group)
        self.main_layout.addWidget(self.float_group)
        self.main_layout.addWidget(self.timer_group)
        self.main_layout.addWidget(self.hotkey_group)
        self.main_layout.addWidget(self.appearance_group)  # 添加外观设置组
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_layout)
        
        # 连接信号和槽
        self.brightness_slider.valueChanged.connect(self.update_brightness)
        self.eye_protect_intensity_slider.valueChanged.connect(self.update_eye_protect_intensity)
        self.normal_mode_btn.clicked.connect(lambda: self.set_brightness_mode(100))
        self.dim_mode_btn.clicked.connect(self.set_eye_protect_mode)
        self.night_mode_btn.clicked.connect(lambda: self.set_brightness_mode(40))
        self.reset_btn.clicked.connect(self.reset_settings)
        self.apply_btn.clicked.connect(self.apply_settings)
        self.autostart_checkbox.toggled.connect(self.toggle_autostart)
        self.blue_light_checkbox.toggled.connect(self.toggle_blue_light)
        self.floating_btn_checkbox.toggled.connect(self.toggle_floating_button)
        self.timer_checkbox.toggled.connect(self.toggle_timer)
        self.exit_hotkey_combo.currentIndexChanged.connect(self.update_exit_hotkey)
        self.github_btn.clicked.connect(self.open_github)
        self.dark_mode_checkbox.toggled.connect(self.toggle_dark_mode)
        self.area_mode_checkbox.toggled.connect(self.toggle_area_mode)
        
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
    
    def update_eye_protect_intensity(self, value):
        """更新护眼模式强度"""
        self.eye_protect_intensity = value
        self.eye_protect_intensity_value_label.setText(f"{value}%")
        self.settings.setValue("eye_protect_intensity", value)
    
    def set_brightness_mode(self, value):
        self.brightness_slider.setValue(value)
    
    def set_eye_protect_mode(self):
        """使用自定义护眼模式强度"""
        self.brightness_slider.setValue(self.eye_protect_intensity)
    
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
        self.timer_start_time_edit.setEnabled(state)
        self.timer_end_time_edit.setEnabled(state)
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
        # 检查是否开启了定时功能
        if not self.timer_enabled:
            return
        
        current_time = QTime.currentTime()
        scheduled_start_time = self.timer_start_time_edit.time()
        scheduled_end_time = self.timer_end_time_edit.time()
        
        # 跨天情况处理
        is_in_time_range = False
        if scheduled_start_time < scheduled_end_time:
            # 正常情况：开始时间早于结束时间
            is_in_time_range = scheduled_start_time <= current_time < scheduled_end_time
        else:
            # 跨天情况：开始时间晚于结束时间（例如晚上10点到早上6点）
            is_in_time_range = current_time >= scheduled_start_time or current_time < scheduled_end_time
        
        # 根据是否在时间范围内执行相应操作
        mode_index = self.timer_mode_combo.currentIndex()
        
        # 如果在时间范围内且之前未应用设置
        if is_in_time_range and not getattr(self, 'timer_applied', False):
            self.apply_timer_mode(mode_index)
            self.timer_applied = True
        # 如果不在时间范围内且之前已应用设置
        elif not is_in_time_range and getattr(self, 'timer_applied', False):
            # 恢复正常模式
            self.set_brightness_mode(100)
            self.blue_light_checkbox.setChecked(False)
            self.high_contrast_checkbox.setChecked(False)
            self.timer_applied = False
    
    def apply_timer_mode(self, mode_index):
        """应用定时模式设置"""
        if mode_index == 0:  # 护眼模式
            self.set_brightness_mode(self.eye_protect_intensity)
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
        self.eye_protect_intensity_slider.setValue(70)
        self.high_contrast_checkbox.setChecked(False)
        self.blue_light_checkbox.setChecked(False)
        self.autostart_checkbox.setChecked(False)
        self.timer_checkbox.setChecked(False)
        self.timer_start_time_edit.setTime(QTime(22, 0))
        self.timer_end_time_edit.setTime(QTime(6, 0))
        self.timer_mode_combo.setCurrentIndex(0)
        self.exit_hotkey_combo.setCurrentIndex(0)
        self.floating_btn_checkbox.setChecked(True)
        self.dark_mode_checkbox.setChecked(False)  # 重置暗黑模式设置
        self.area_mode_checkbox.setChecked(False)  # 重置区域模式设置
        
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
        self.settings.setValue("eye_protect_intensity", self.eye_protect_intensity)
        self.settings.setValue("auto_start", self.auto_start)
        self.settings.setValue("blue_light_filter", self.blue_light_filter)
        self.settings.setValue("timer_enabled", self.timer_enabled)
        self.settings.setValue("timer_time", self.timer_start_time_edit.time())
        self.settings.setValue("timer_end_time", self.timer_end_time_edit.time())
        self.settings.setValue("timer_mode", self.timer_mode_combo.currentIndex())
        self.settings.setValue("exit_shortcut", self.exit_shortcut)
        self.settings.setValue("show_floating_button", self.floating_btn_checkbox.isChecked())
        self.settings.setValue("dark_mode", self.dark_mode)  # 保存暗黑模式设置
        self.settings.setValue("area_mode", self.area_mode_checkbox.isChecked())  # 保存区域模式设置
        
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

    def open_github(self):
        """打开GitHub官方网站"""
        webbrowser.open("https://github.com/sikuai2333/ScreenBrightnessTool")

    # 添加暗黑模式相关方法
    def apply_theme(self):
        """应用当前主题设置"""
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()
            
    def set_dark_theme(self):
        """设置暗黑主题"""
        app = QApplication.instance()
        palette = QPalette()
        
        # 设置暗色调色板
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        app.setPalette(palette)
        
        # 设置样式表
        app.setStyleSheet("""
            QGroupBox {
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #ddd;
            }
            QPushButton {
                background-color: #444;
                border: 1px solid #555;
                border-radius: 3px;
                color: #ddd;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #666;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #444;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ddd;
                border: 1px solid #777;
                width: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }
            QCheckBox {
                color: #ddd;
            }
            QLabel {
                color: #ddd;
            }
            QComboBox {
                background-color: #444;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 2px 5px;
            }
            QTimeEdit {
                background-color: #444;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)
    
    def set_light_theme(self):
        """设置亮色主题"""
        app = QApplication.instance()
        app.setPalette(app.style().standardPalette())
        app.setStyleSheet("""
            QGroupBox::title {
                padding: 0 8px;
            }
        """)
        
    def toggle_dark_mode(self, enabled):
        """切换暗黑模式"""
        self.dark_mode = enabled
        self.apply_theme()
        
        # 保存设置
        self.settings.setValue("dark_mode", enabled)

    def toggle_area_mode(self, enabled):
        """切换区域模式"""
        # 启用或禁用相关按钮
        self.select_area_btn.setEnabled(enabled)
        self.clear_area_btn.setEnabled(enabled)
        
        # 如果禁用区域模式，清除已选区域
        if not enabled:
            self.clear_selected_area()
    
    def start_area_selection(self):
        """启动区域选择过程"""
        # 隐藏主窗口，避免干扰区域选择
        self.hide()
        
        # 使用亮度控制器启动区域选择
        if hasattr(self, 'brightness_control') and self.brightness_control:
            self.brightness_control.start_area_selection()
        
        # 使用定时器稍后重新显示主窗口
        QTimer.singleShot(1000, self.show)
    
    def clear_selected_area(self):
        """清除已选择的区域"""
        if hasattr(self, 'brightness_control') and self.brightness_control:
            self.brightness_control.clear_selected_area()
    
    def set_brightness_control(self, brightness_control):
        """设置亮度控制器的引用"""
        self.brightness_control = brightness_control


# 添加QShortcut类
from PyQt5.QtWidgets import QShortcut 