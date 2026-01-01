import sys
import os
import platform
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings, QTime
from PyQt5.QtGui import QIcon, QColor
from main_window import MainWindow
from brightness_control import BrightnessControl
from floating_button import FloatingButton

class BrightnessApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("屏幕亮度调节工具")
        self.app.setOrganizationName("BrightnessControl")
        
        # 设置应用程序图标
        self.set_app_icon()
        
        # 初始化亮度控制器
        self.brightness_control = BrightnessControl()
        
        # 初始化主窗口
        self.main_window = MainWindow()
        
        # 将亮度控制器引用传递给主窗口
        self.main_window.set_brightness_control(self.brightness_control)
        
        # 获取悬浮球颜色设置
        settings = QSettings("BrightnessControl", "BrightnessAdjuster")
        bg_color = settings.value("float_bg_color", QColor(30, 30, 30, 180))
        if isinstance(bg_color, str):
            bg_color = QColor(bg_color)
        
        text_color = settings.value("float_text_color", QColor(255, 255, 255))
        if isinstance(text_color, str):
            text_color = QColor(text_color)
        
        # 初始化悬浮按钮
        self.floating_button = FloatingButton(parent=self.main_window, brightness_control=self.brightness_control)
        
        # 设置悬浮球颜色
        self.floating_button.set_colors(bg_color, text_color)
        
        # 设置悬浮按钮引用
        self.main_window.set_floating_button(self.floating_button)
        
        # 连接信号与槽
        self.connect_signals()
        
        # 检查是否需要设置自启动
        self.check_autostart()
        
        # 应用已保存的设置
        self.apply_saved_settings()
    
    def set_app_icon(self):
        """设置应用程序图标"""
        # 尝试从不同路径加载图标
        icon_paths = [
            "icon.png",                     # 根目录
            os.path.join("images", "icon.png"),  # images文件夹
            os.path.join("resources", "icon.png"),  # resources文件夹
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")  # 脚本所在目录
        ]
        
        for path in icon_paths:
            if os.path.exists(path):
                self.app.setWindowIcon(QIcon(path))
                break
    
    def connect_signals(self):
        """连接UI信号到亮度控制功能"""
        # 亮度滑动条变化时调整亮度
        self.main_window.brightness_slider.valueChanged.connect(
            self.brightness_control.set_brightness
        )
        
        # 同时更新悬浮按钮的显示
        self.main_window.brightness_slider.valueChanged.connect(
            self.update_floating_button_brightness
        )
        
        # 高对比度开关状态变化时切换高对比度模式
        self.main_window.high_contrast_checkbox.toggled.connect(
            self.brightness_control.toggle_high_contrast
        )
        
        # 防蓝光开关状态变化时切换防蓝光模式
        self.main_window.blue_light_checkbox.toggled.connect(
            self.brightness_control.toggle_blue_light_filter
        )
        
        # 悬浮按钮开关
        self.main_window.floating_btn_checkbox.toggled.connect(
            self.toggle_floating_button
        )
        
        # 应用设置时保存当前状态
        self.main_window.apply_btn.clicked.connect(self.save_settings)
    
    def update_floating_button_brightness(self, value):
        """更新悬浮按钮显示的亮度值"""
        if self.floating_button:
            self.floating_button.current_brightness = value
            self.floating_button.update_button_text()
    
    def toggle_floating_button(self, show):
        """显示或隐藏悬浮按钮"""
        # 如果主窗口可见，即使设置为显示悬浮按钮，也不要显示
        if show and not self.main_window.isVisible():
            self.floating_button.show()
        else:
            self.floating_button.hide()
    
    def apply_saved_settings(self):
        """应用上次保存的设置"""
        settings = QSettings("BrightnessControl", "BrightnessAdjuster")
        
        # 获取保存的亮度值，默认为100
        brightness = settings.value("brightness", 100, type=int)
        
        # 获取保存的高对比度设置，默认为False
        high_contrast = settings.value("high_contrast", False, type=bool)
        
        # 获取保存的防蓝光设置，默认为False
        blue_light = settings.value("blue_light_filter", False, type=bool)
        
        # 获取保存的悬浮按钮设置，默认为True
        show_floating_button = settings.value("show_floating_button", True, type=bool)
        
        # 直接应用亮度设置到亮度控制器
        self.brightness_control.set_brightness(brightness)
        self.brightness_control.toggle_high_contrast(high_contrast)
        self.brightness_control.toggle_blue_light_filter(blue_light)
        
        # 然后设置UI状态，避免触发重复的更改事件
        self.main_window.brightness_slider.blockSignals(True)
        self.main_window.high_contrast_checkbox.blockSignals(True)
        self.main_window.blue_light_checkbox.blockSignals(True)
        
        self.main_window.brightness_slider.setValue(brightness)
        self.main_window.high_contrast_checkbox.setChecked(high_contrast)
        self.main_window.blue_light_checkbox.setChecked(blue_light)
        
        self.main_window.brightness_slider.blockSignals(False)
        self.main_window.high_contrast_checkbox.blockSignals(False)
        self.main_window.blue_light_checkbox.blockSignals(False)
        
        # 设置按钮选中状态，但不立即显示或隐藏
        self.main_window.floating_btn_checkbox.setChecked(show_floating_button)
        
        # 初始化悬浮按钮的亮度显示
        self.floating_button.current_brightness = brightness
        self.floating_button.update_button_text()
        
        # 恢复区域选择模式
        area_mode = settings.value("area_mode", False, type=bool)
        if area_mode and hasattr(self.main_window, 'area_mode_checkbox'):
            self.main_window.area_mode_checkbox.setChecked(area_mode)
            self.brightness_control.is_area_selected = area_mode
    
    def save_settings(self):
        """保存当前设置"""
        settings = QSettings("BrightnessControl", "BrightnessAdjuster")
        
        # 保存当前亮度值
        settings.setValue("brightness", self.main_window.brightness_value)
        
        # 保存高对比度状态
        settings.setValue("high_contrast", self.main_window.high_contrast_checkbox.isChecked())
        
        # 保存防蓝光状态
        settings.setValue("blue_light_filter", self.main_window.blue_light_checkbox.isChecked())
        
        # 保存自启动状态
        settings.setValue("auto_start", self.main_window.autostart_checkbox.isChecked())
        
        # 保存悬浮按钮状态
        settings.setValue("show_floating_button", self.main_window.floating_btn_checkbox.isChecked())
        
        # 确保设置被写入
        settings.sync()
        
        # 检查是否需要更新自启动
        self.check_autostart()
    
    def check_autostart(self):
        """检查是否需要设置自启动"""
        settings = QSettings("BrightnessControl", "BrightnessAdjuster")
        auto_start = settings.value("auto_start", False, type=bool)
        
        if auto_start:
            self.enable_autostart()
        else:
            self.disable_autostart()
    
    def enable_autostart(self):
        """启用开机自启动"""
        if platform.system() == "Windows":
            # Windows下通过注册表设置自启动
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(
                key, "BrightnessAdjuster", 0, winreg.REG_SZ,
                f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
            )
            winreg.CloseKey(key)
        elif platform.system() == "Darwin":  # macOS
            # macOS下通过launchd设置自启动
            # 简化实现，实际需要创建一个plist文件
            pass
        elif platform.system() == "Linux":
            # Linux下创建.desktop文件到自启动目录
            autostart_dir = os.path.expanduser("~/.config/autostart")
            if not os.path.exists(autostart_dir):
                os.makedirs(autostart_dir)
            
            desktop_file = os.path.join(autostart_dir, "brightness-adjuster.desktop")
            with open(desktop_file, "w") as f:
                f.write(
                    "[Desktop Entry]\n"
                    "Type=Application\n"
                    "Name=屏幕亮度调节工具\n"
                    f"Exec={sys.executable} {os.path.abspath(sys.argv[0])}\n"
                    "Terminal=false\n"
                    "Hidden=false\n"
                    "X-GNOME-Autostart-enabled=true\n"
                )
    
    def disable_autostart(self):
        """禁用开机自启动"""
        if platform.system() == "Windows":
            # Windows下删除注册表项
            import winreg
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0, winreg.KEY_SET_VALUE
                )
                winreg.DeleteValue(key, "BrightnessAdjuster")
                winreg.CloseKey(key)
            except WindowsError:
                # 键不存在，忽略错误
                pass
        elif platform.system() == "Darwin":  # macOS
            # macOS下删除launchd配置
            pass
        elif platform.system() == "Linux":
            # Linux下删除自启动文件
            desktop_file = os.path.expanduser("~/.config/autostart/brightness-adjuster.desktop")
            if os.path.exists(desktop_file):
                os.remove(desktop_file)
    
    def run(self):
        """运行应用程序"""
        # 显示主窗口（这会自动隐藏悬浮按钮）
        self.main_window.show()
        
        return self.app.exec_()
    
    def cleanup(self):
        """清理资源"""
        self.brightness_control.cleanup()
        
        # 关闭悬浮按钮
        if self.floating_button:
            self.floating_button.close()


if __name__ == "__main__":
    app = BrightnessApp()
    
    try:
        exit_code = app.run()
    finally:
        app.cleanup()
    
    sys.exit(exit_code) 