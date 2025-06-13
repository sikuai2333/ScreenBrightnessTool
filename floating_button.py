from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMenu, QAction, QSlider, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QTimer, QTime
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QScreen, QFont
import os

class FloatingButton(QWidget):
    def __init__(self, parent=None, brightness_control=None):
        super(FloatingButton, self).__init__(parent)
        self.brightness_control = brightness_control
        self.parent_window = parent
        
        # 设置无边框窗口，保持在最前面，并允许在整个屏幕范围内移动
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.SubWindow  # 允许跨窗口边界
        )
        
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 加载图标
        self.app_icon = self.load_icon()
        if self.app_icon:
            self.setWindowIcon(self.app_icon)
        
        # 窗口大小 - 长方形形状，适合显示时间
        self.setFixedSize(120, 48)
        
        # 拖动相关变量
        self.dragging = False
        self.drag_position = QPoint()
        
        # 默认颜色设置
        self.bg_color = QColor(30, 30, 30, 180)  # 背景颜色
        self.text_color = QColor(255, 255, 255)  # 文字颜色
        self.hover_color = QColor(50, 50, 50, 200)  # 悬停颜色
        self.pressed_color = QColor(80, 80, 80, 220)  # 按下颜色
        
        # 创建主按钮
        self.main_button = QPushButton("", self)
        self.main_button.setFixedSize(120, 48)
        self.update_button_style()
        
        # 按钮左键点击显示菜单
        self.main_button.clicked.connect(self.show_menu)
        
        # 移除鼠标穿透属性，确保可以正常接收鼠标事件
        self.main_button.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        
        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.main_button)
        
        # 当前亮度值
        self.current_brightness = 100
        
        # 获取屏幕信息，用于限制拖拽范围
        self.update_screen_geometry()
        
        # 设置时间更新定时器
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # 每秒更新一次
        
        # 初始显示时间
        self.update_time()
        
        # 启用鼠标跟踪，以便接收鼠标移动事件
        self.setMouseTracking(True)
        self.main_button.setMouseTracking(True)
    
    def update_button_style(self):
        """更新按钮样式表"""
        self.main_button.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({self.bg_color.red()}, {self.bg_color.green()}, {self.bg_color.blue()}, {self.bg_color.alpha()});
                border-radius: 10px;
                color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()});
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: rgba({self.hover_color.red()}, {self.hover_color.green()}, {self.hover_color.blue()}, {self.hover_color.alpha()});
            }}
            QPushButton:pressed {{
                background-color: rgba({self.pressed_color.red()}, {self.pressed_color.green()}, {self.pressed_color.blue()}, {self.pressed_color.alpha()});
            }}
        """)
    
    def update_time(self):
        """更新显示的时间"""
        current_time = QTime.currentTime()
        time_text = current_time.toString("HH:mm:ss")
        
        # 显示时间和亮度
        display_text = f"{time_text}\n{self.current_brightness}%"
        self.main_button.setText(display_text)
    
    def set_colors(self, bg_color, text_color):
        """设置悬浮球的颜色"""
        if bg_color:
            self.bg_color = bg_color
            # 更新悬停和按下颜色
            self.hover_color = QColor(
                min(self.bg_color.red() + 20, 255),
                min(self.bg_color.green() + 20, 255),
                min(self.bg_color.blue() + 20, 255),
                self.bg_color.alpha()
            )
            self.pressed_color = QColor(
                min(self.bg_color.red() + 50, 255),
                min(self.bg_color.green() + 50, 255),
                min(self.bg_color.blue() + 50, 255),
                self.bg_color.alpha()
            )
        
        if text_color:
            self.text_color = text_color
        
        # 更新按钮样式
        self.update_button_style()
    
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
    
    def update_screen_geometry(self):
        """更新屏幕几何信息"""
        self.available_geometry = QApplication.primaryScreen().availableGeometry()
        # 考虑多屏幕情况
        for screen in QApplication.screens():
            self.available_geometry = self.available_geometry.united(screen.availableGeometry())
    
    def update_button_text(self):
        """更新按钮上显示的亮度值（仅更新亮度值，不影响时间显示）"""
        self.current_brightness = self.current_brightness
        self.update_time()  # 通过调用update_time来更新完整显示
    
    def show_menu(self):
        """显示悬浮菜单"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(40, 40, 40, 230);
                border: 1px solid rgba(60, 60, 60, 200);
                border-radius: 5px;
                color: white;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: rgba(70, 70, 70, 230);
            }
        """)
        
        # 设置菜单图标
        if self.app_icon:
            menu.setWindowIcon(self.app_icon)
        
        # 亮度滑动条 - 使用自定义widget作为action
        slider_widget = QWidget()
        slider_layout = QVBoxLayout(slider_widget)
        
        brightness_slider = QSlider(Qt.Horizontal)
        brightness_slider.setMinimum(10)
        brightness_slider.setMaximum(100)
        brightness_slider.setValue(self.current_brightness)
        brightness_slider.setFixedWidth(150)
        brightness_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: rgba(80, 80, 80, 200);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: 1px solid #5c5c5c;
                width: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }
        """)
        
        brightness_slider.valueChanged.connect(self.set_brightness)
        slider_layout.addWidget(brightness_slider)
        
        slider_action = QWidgetAction(menu)
        slider_action.setDefaultWidget(slider_widget)
        menu.addAction(slider_action)
        
        # 添加预设模式
        menu.addSeparator()
        
        normal_action = menu.addAction("正常模式")
        normal_action.triggered.connect(lambda: self.set_brightness(100))
        
        # 获取护眼模式强度
        eye_protect_intensity = 70  # 默认值
        if self.parent_window and hasattr(self.parent_window, 'eye_protect_intensity'):
            eye_protect_intensity = self.parent_window.eye_protect_intensity
        
        dim_action = menu.addAction(f"护眼模式 ({eye_protect_intensity}%)")
        dim_action.triggered.connect(lambda: self.set_brightness(eye_protect_intensity))
        
        night_action = menu.addAction("夜间模式")
        night_action.triggered.connect(lambda: self.set_brightness(40))
        
        blue_light_action = menu.addAction("防蓝光")
        blue_light_action.setCheckable(True)
        blue_light_action.setChecked(self.brightness_control.is_blue_light_filter if hasattr(self.brightness_control, 'is_blue_light_filter') else False)
        blue_light_action.toggled.connect(self.toggle_blue_light)
        
        # 控制原窗口
        menu.addSeparator()
        
        show_main_window = menu.addAction("显示主窗口")
        show_main_window.triggered.connect(self.show_parent_window)
        
        exit_action = menu.addAction("退出")
        exit_action.triggered.connect(self.parent_window.close_application)
        
        # 显示菜单
        menu.exec_(self.mapToGlobal(self.main_button.pos()))
    
    def set_brightness(self, value):
        """设置亮度"""
        self.current_brightness = value
        
        # 更新按钮文本
        self.update_button_text()
        
        # 调用亮度控制器改变亮度
        if self.brightness_control:
            self.brightness_control.set_brightness(value)
            
            # 同步更新主窗口中的亮度滑动条
            if self.parent_window:
                self.parent_window.brightness_slider.setValue(value)
    
    def toggle_blue_light(self, enabled):
        """切换防蓝光模式"""
        if hasattr(self.brightness_control, 'toggle_blue_light_filter'):
            self.brightness_control.toggle_blue_light_filter(enabled)
            
            # 同步更新主窗口中的防蓝光复选框
            if self.parent_window and hasattr(self.parent_window, 'blue_light_checkbox'):
                self.parent_window.blue_light_checkbox.setChecked(enabled)
    
    def show_parent_window(self):
        """显示主窗口"""
        if self.parent_window:
            self.parent_window.showNormal()
            self.parent_window.activateWindow()
    
    def mousePressEvent(self, event):
        """鼠标按下事件，使用右键实现窗口拖动"""
        if event.button() == Qt.RightButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        else:
            super(FloatingButton, self).mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，使用右键实现窗口拖动（全屏范围）"""
        if event.buttons() == Qt.RightButton and self.dragging:
            # 计算新位置
            new_pos = event.globalPos() - self.drag_position
            
            # 更新屏幕几何信息
            self.update_screen_geometry()
            
            # 确保窗口不会完全拖出屏幕
            x = max(self.available_geometry.left(), min(new_pos.x(), self.available_geometry.right() - self.width()))
            y = max(self.available_geometry.top(), min(new_pos.y(), self.available_geometry.bottom() - self.height()))
            
            self.move(x, y)
            event.accept()
        else:
            super(FloatingButton, self).mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，使用右键实现窗口拖动"""
        if event.button() == Qt.RightButton:
            self.dragging = False
            event.accept()
        else:
            super(FloatingButton, self).mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        """绘制事件，添加长方形阴影效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制阴影
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 30))
        painter.drawRoundedRect(4, 4, self.width() - 8, self.height() - 8, 10, 10)
        
        painter.end()
    
    def moveEvent(self, event):
        """移动事件，确保悬浮按钮不会完全移出屏幕"""
        super(FloatingButton, self).moveEvent(event)
        
        # 检查是否需要更新屏幕几何信息
        self.update_screen_geometry()
        
        # 获取当前位置
        pos = self.pos()
        new_pos = pos
        
        # 确保按钮不会完全移出屏幕
        if pos.x() < self.available_geometry.left():
            new_pos.setX(self.available_geometry.left())
        elif pos.x() > self.available_geometry.right() - self.width():
            new_pos.setX(self.available_geometry.right() - self.width())
        
        if pos.y() < self.available_geometry.top():
            new_pos.setY(self.available_geometry.top())
        elif pos.y() > self.available_geometry.bottom() - self.height():
            new_pos.setY(self.available_geometry.bottom() - self.height())
        
        # 如果位置有变化，移动按钮
        if new_pos != pos:
            self.move(new_pos)
    
    def contextMenuEvent(self, event):
        """重写右键菜单事件，禁用默认的右键菜单"""
        # 禁用默认右键菜单，改为使用右键拖拽
        event.accept()


class QWidgetAction(QAction):
    """自定义Action，可以包含QWidget"""
    def __init__(self, parent=None):
        super(QWidgetAction, self).__init__(parent)
        self.widget = None
    
    def setDefaultWidget(self, widget):
        self.widget = widget
        
    def createWidget(self, parent):
        if self.widget:
            return self.widget
        return None 