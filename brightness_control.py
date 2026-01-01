import sys
import platform
from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QScreen, QCursor

class BrightnessControl:
    def __init__(self):
        self._overlay = None
        self.is_high_contrast = False
        self.is_blue_light_filter = False
        self.screens = []
        self.selected_area = None  # 存储选定的屏幕区域
        self.is_area_selected = False  # 是否使用区域模式
        self.initialize_screens()
        
        # 区域选择器
        self.area_selector = None
    
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
            # 如果在区域模式下，只有选中的区域才应用亮度设置
            if self.is_area_selected and self.selected_area:
                overlay.set_selected_area(self.selected_area)
            else:
                overlay.clear_selected_area()
                
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
    
    def start_area_selection(self):
        """开始选择屏幕区域"""
        if not self.area_selector:
            self.area_selector = AreaSelector(self)
        self.area_selector.start_selection()
    
    def select_area(self, selected_rect):
        """设置选定的屏幕区域"""
        self.selected_area = selected_rect
        self.is_area_selected = True
        
        # 重新应用当前亮度设置到选定区域
        if self._overlay:
            for overlay in self._overlay:
                overlay.set_selected_area(selected_rect)
    
    def clear_selected_area(self):
        """清除选定的屏幕区域"""
        self.selected_area = None
        self.is_area_selected = False
        
        # 更新所有遮罩
        if self._overlay:
            for overlay in self._overlay:
                overlay.clear_selected_area()
    
    def cleanup(self):
        """清理所有遮罩"""
        if self._overlay:
            for overlay in self._overlay:
                overlay.close()
                overlay.deleteLater()
            self._overlay = []
            
        if self.area_selector:
            self.area_selector.close()
            self.area_selector = None


class AreaSelector(QWidget):
    """屏幕区域选择器"""
    def __init__(self, brightness_control):
        super(AreaSelector, self).__init__(None, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.brightness_control = brightness_control
        self.setWindowOpacity(0.3)
        self.rubberband = None
        self.origin = QPoint()
        self.selection_active = False
        
        # 获取整个屏幕的几何信息
        screen_rect = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_rect)
        
    def start_selection(self):
        """开始区域选择过程"""
        # 显示全屏遮罩
        self.setCursor(Qt.CrossCursor)
        self.show()
        
    def mousePressEvent(self, event):
        """鼠标按下事件，开始绘制橡皮筋"""
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            if not self.rubberband:
                self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()
            self.selection_active = True
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，更新橡皮筋大小"""
        if self.selection_active:
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，完成选择"""
        if event.button() == Qt.LeftButton and self.selection_active:
            selected_rect = QRect(self.origin, event.pos()).normalized()
            
            # 确保选择区域有效
            if selected_rect.width() > 10 and selected_rect.height() > 10:
                # 通知亮度控制器应用选定区域
                self.brightness_control.select_area(selected_rect)
            
            self.selection_active = False
            self.rubberband.hide()
            self.hide()
            
            # 恢复正常光标
            self.setCursor(Qt.ArrowCursor)
    
    def keyPressEvent(self, event):
        """按键事件，ESC键取消选择"""
        if event.key() == Qt.Key_Escape:
            self.selection_active = False
            if self.rubberband:
                self.rubberband.hide()
            self.hide()
            
            # 恢复正常光标
            self.setCursor(Qt.ArrowCursor)


class BrightnessOverlay(QWidget):
    def __init__(self, screen_index, geometry):
        super(BrightnessOverlay, self).__init__()
        
        self.screen_index = screen_index
        self.opacity = 0  # 默认完全透明
        self.is_high_contrast = False
        self.is_blue_light_filter = False
        self.special_window_rects = []  # 存储特殊窗口的矩形区域
        self.selected_area = None  # 选定的屏幕区域
        
        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 总在最前
            Qt.Tool |  # 工具窗口，不显示在任务栏
            Qt.WindowTransparentForInput |  # 使窗口对输入事件透明
            Qt.WindowDoesNotAcceptFocus  # 窗口不接受焦点
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
        
        # 使用定时器查找并记录特殊窗口
        self.special_window_timer = QTimer(self)
        self.special_window_timer.timeout.connect(self.find_special_windows)
        self.special_window_timer.start(500)  # 每0.5秒执行一次
        
        # 设置Z-Order（稍微降低一些，允许特殊窗口在上层）
        self.lower()
    
    def set_selected_area(self, rect):
        """设置选定的屏幕区域"""
        self.selected_area = rect
        self.update()  # 触发重绘
    
    def clear_selected_area(self):
        """清除选定的屏幕区域"""
        self.selected_area = None
        self.update()  # 触发重绘
    
    def find_special_windows(self):
        """查找需要特殊处理的窗口（如火绒流量窗口、右键菜单等）"""
        # 在实际应用中，可能需要使用平台特定API来获取窗口信息
        # 这里仅作为示例，简化处理
        self.special_window_rects = []
        
        # 获取所有顶层窗口（Windows平台可使用Win32 API）
        # 此处是简化示例，实际实现需要与具体平台API交互
        # self.special_window_rects.append(QRect(x, y, width, height))
        
        # 标记需要更新
        self.update()
    
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
    
    def paintEvent(self, event):
        """绘制遮罩"""
        painter = QPainter(self)
        
        # 允许绘制区域合成
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        
        if self.selected_area:
            # 在选定区域模式下，只对选定区域应用滤镜效果
            if self.is_high_contrast:
                # 高对比度模式使用蓝色滤镜
                painter.fillRect(self.selected_area, QColor(0, 0, 255, self.opacity))
            elif self.is_blue_light_filter:
                # 防蓝光模式使用淡橙色滤镜（过滤蓝光）
                painter.fillRect(self.selected_area, QColor(255, 155, 30, 40 + self.opacity // 10))
            else:
                # 普通模式使用黑色遮罩
                painter.fillRect(self.selected_area, QColor(0, 0, 0, self.opacity))
        else:
            # 全屏模式下应用滤镜效果
            if self.is_high_contrast:
                # 高对比度模式使用蓝色滤镜
                painter.fillRect(self.rect(), QColor(0, 0, 255, self.opacity))
            elif self.is_blue_light_filter:
                # 防蓝光模式使用淡橙色滤镜（过滤蓝光）
                painter.fillRect(self.rect(), QColor(255, 155, 30, 40 + self.opacity // 10))
            else:
                # 普通模式使用黑色遮罩
                painter.fillRect(self.rect(), QColor(0, 0, 0, self.opacity))
        
        # 为特殊窗口区域创建透明区域（如火绒流量窗口、右键菜单等）
        if self.special_window_rects:
            # 设置擦除模式
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            
            for rect in self.special_window_rects:
                # 擦除特殊窗口区域
                painter.fillRect(rect, Qt.transparent)
        
        painter.end() 