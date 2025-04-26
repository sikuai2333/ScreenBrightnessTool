import sys
import platform
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

class BrightnessControl:
    def __init__(self):
        self._overlay = None
        self.is_high_contrast = False
        self.is_blue_light_filter = False
        self.screens = []
        self.initialize_screens()
    
    def initialize_screens(self):
        """初始化所有屏幕的遮罩"""
        app = QApplication.instance()
        if not app:
            # 如果没有QApplication实例，无法创建遮罩
            return
            
        # 清理已有遮罩
        if self._overlay:
            for overlay in self._overlay:
                overlay.close()
                overlay.deleteLater()
        
        self._overlay = []
        screen_count = app.desktop().screenCount()
        
        # 为每个屏幕创建遮罩
        for i in range(screen_count):
            screen_geometry = app.desktop().screenGeometry(i)
            overlay = BrightnessOverlay(i, screen_geometry)
            self._overlay.append(overlay)
            self.screens.append({"index": i, "geometry": screen_geometry})
            
        # 默认亮度设为100%（完全透明）
        self.set_brightness(100)
    
    def set_brightness(self, brightness_value):
        """设置屏幕亮度
        
        Args:
            brightness_value: 0-100之间的亮度值，100表示原始亮度
        """
        if not self._overlay:
            return
            
        # 亮度值反转为透明度：亮度100%对应透明度100%（即alpha=0）
        # 亮度0%对应透明度0%（即alpha=255）
        alpha = int(255 * (100 - brightness_value) / 100)
        
        for overlay in self._overlay:
            overlay.set_opacity(alpha)
            if not overlay.isVisible():
                overlay.show()
    
    def toggle_high_contrast(self, enabled):
        """切换高对比度模式"""
        self.is_high_contrast = enabled
        if self._overlay:
            for overlay in self._overlay:
                overlay.set_high_contrast(enabled)
                # 如果启用高对比度，关闭防蓝光
                if enabled:
                    self.is_blue_light_filter = False
                    overlay.set_blue_light_filter(False)
    
    def toggle_blue_light_filter(self, enabled):
        """切换防蓝光模式"""
        self.is_blue_light_filter = enabled
        if self._overlay:
            for overlay in self._overlay:
                overlay.set_blue_light_filter(enabled)
                # 如果启用防蓝光，关闭高对比度
                if enabled:
                    self.is_high_contrast = False
                    overlay.set_high_contrast(False)
    
    def cleanup(self):
        """清理所有遮罩"""
        if self._overlay:
            for overlay in self._overlay:
                overlay.close()
                overlay.deleteLater()
            self._overlay = []


class BrightnessOverlay(QWidget):
    def __init__(self, screen_index, geometry):
        super(BrightnessOverlay, self).__init__()
        
        self.screen_index = screen_index
        self.opacity = 0  # 默认完全透明
        self.is_high_contrast = False
        self.is_blue_light_filter = False
        
        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 总在最前
            Qt.Tool  # 工具窗口，不显示在任务栏
        )
        
        # 设置窗口透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 允许鼠标事件穿透窗口
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        # 设置窗口位置和大小
        self.setGeometry(geometry)
        
        # 根据操作系统设置特定属性
        if platform.system() == "Windows":
            # Windows下设置窗口为工具窗口类型
            self.setWindowFlags(self.windowFlags() | Qt.ToolTip)
        elif platform.system() == "Darwin":  # macOS
            # macOS下可能需要设置特定的属性
            pass
        
        # 使用定时器定期更新窗口，确保遮罩总是在最上层
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.ensure_on_top)
        self.update_timer.start(1000)  # 每秒执行一次
    
    def set_opacity(self, opacity):
        """设置遮罩的不透明度"""
        self.opacity = max(0, min(255, opacity))  # 限制在0-255范围内
        self.update()  # 触发重绘
    
    def set_high_contrast(self, enabled):
        """设置是否启用高对比度模式"""
        self.is_high_contrast = enabled
        self.update()  # 触发重绘
    
    def set_blue_light_filter(self, enabled):
        """设置是否启用防蓝光模式"""
        self.is_blue_light_filter = enabled
        self.update()  # 触发重绘
    
    def ensure_on_top(self):
        """确保遮罩总是在最上层"""
        # 如果窗口不可见，直接返回
        if not self.isVisible():
            return
        
        # 获取当前屏幕几何信息
        app = QApplication.instance()
        current_geometry = app.desktop().screenGeometry(self.screen_index)
        
        # 如果屏幕几何信息变化了，更新窗口位置和大小
        if self.geometry() != current_geometry:
            self.setGeometry(current_geometry)
        
        # 确保窗口在最上层
        self.raise_()
    
    def paintEvent(self, event):
        """绘制遮罩"""
        painter = QPainter(self)
        
        if self.is_high_contrast:
            # 高对比度模式使用蓝色滤镜
            painter.fillRect(self.rect(), QColor(0, 0, 255, self.opacity))
        elif self.is_blue_light_filter:
            # 防蓝光模式使用淡橙色滤镜（过滤蓝光）
            painter.fillRect(self.rect(), QColor(255, 155, 30, 40 + self.opacity // 10))
        else:
            # 普通模式使用黑色遮罩
            painter.fillRect(self.rect(), QColor(0, 0, 0, self.opacity))
        
        painter.end() 