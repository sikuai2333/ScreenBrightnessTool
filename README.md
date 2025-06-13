<!--
 * @Author: sikuai2333 2643927725@qq.com
 * @Date: 2025-04-26 10:08:35
 * @LastEditors: sikuai
 * @LastEditTime: 2025-06-13 09:00:24
 * @FilePath: /屏幕亮度调节/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 屏幕亮度调节工具 (ScreenBrightnessTool)

一个基于PyQt5的跨平台屏幕亮度调节程序，通过创建半透明遮罩层来调整屏幕亮度。

[English Version](#english-version)

## 功能特点

- 通过滑动条平滑调整屏幕亮度
- 支持多个显示器
- 预设亮度模式：正常模式、护眼模式、夜间模式
- 支持高对比度和防蓝光模式
- **护眼模式强度调节**：可自定义护眼模式的亮度值(30%-90%)
- 系统托盘图标，最小化后仍可运行
- 开机自启动设置
- 跨平台支持（Windows、macOS、Linux）
- **悬浮窗功能**：
  - 显示系统时间和当前亮度值
  - 右键拖拽可在屏幕任意位置停靠
  - 自定义悬浮窗背景颜色和文字颜色
  - 主窗口打开时自动隐藏，关闭或最小化时显示
- **热键支持**：支持使用Ctrl+E或自定义热键退出软件
- **定时功能**：
  - 支持时间段设置，可指定开始时间和结束时间
  - 在时间段内自动应用选定模式，时间段外恢复正常模式
  - 支持跨日设置（如晚上10点到次日早上6点）
- **暗黑模式**：支持应用界面暗黑/亮色主题切换
- **区域亮度调节**：可以选择只调整屏幕的特定区域亮度
- **官方网站**：提供GitHub链接，可获取最新版本和提交问题

## 文件结构

项目主要包含以下文件：

- `main.py` - 程序入口，初始化和协调各模块
- `main_window.py` - 用户界面模块，处理UI交互
- `brightness_control.py` - 亮度控制核心模块，通过透明遮罩实现亮度控制
- `floating_button.py` - 悬浮窗模块，实现屏幕上的悬浮控制功能
- `icon.png` - 应用图标
- `requirements.txt` - 依赖包列表

## 安装与使用

### 依赖

- Python 3.6+
- PyQt5 5.15.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

### 打包可执行文件

#### Windows

```bash
# 基础打包
pyinstaller --noconsole --onefile --icon=icon.png --name=ScreenBrightnessTool main.py

# 更高级打包（增加版本信息等）
pyinstaller --noconsole --onefile --icon=icon.png --name=ScreenBrightnessTool --version-file=version.txt main.py
```

#### macOS

```bash
# 打包为独立应用
pyinstaller --noconsole --onefile --icon=icon.icns --name=ScreenBrightnessTool main.py

# 打包为app格式
pyinstaller --noconsole --windowed --icon=icon.icns --name=ScreenBrightnessTool main.py

# 创建DMG安装包（需要先打包成app）
hdiutil create -srcfolder "dist/ScreenBrightnessTool.app" -volname "ScreenBrightnessTool" -fs HFS+ -format UDBZ "dist/ScreenBrightnessTool.dmg"
```

#### Linux

```bash
# 基础打包
pyinstaller --noconsole --onefile --name=ScreenBrightnessTool main.py

# 打包为AppImage（需要安装appimagetool）
# 1. 使用PyInstaller打包
pyinstaller --noconsole --name=ScreenBrightnessTool main.py
# 2. 创建AppDir结构
# 3. 使用appimagetool打包
```

## 使用说明

### 主窗口功能

1. 通过滑动条调整屏幕亮度（10%-100%）
2. 可调整护眼模式强度（30%-90%），定制个人舒适度
3. 点击预设模式按钮快速切换亮度：
   - 正常模式（100%亮度）
   - 护眼模式（自定义强度，默认70%亮度）
   - 夜间模式（40%亮度）
4. 勾选"增强对比度"可启用高对比度滤镜
5. 勾选"防蓝光模式"可减少屏幕蓝光
6. 勾选"开机自启动"可设置系统启动时自动运行
7. 关闭窗口时程序会最小化到系统托盘，点击托盘图标可重新打开界面

### 悬浮窗功能

- 显示当前系统时间和屏幕亮度值
- **左键点击**悬浮窗显示菜单，可调整亮度、切换模式或显示主窗口
- **右键长按**悬浮窗实现拖拽，松开鼠标停止拖拽
- 在主窗口的"悬浮窗设置"中可以自定义背景颜色和文字颜色
- 当打开主窗口时，悬浮窗会自动隐藏

### 热键功能

- 默认使用Ctrl+E快捷键退出程序
- 可以在设置中选择其他预设热键：Ctrl+Q或Alt+F4

### 暗黑模式

- 在"外观设置"中启用暗黑模式，使界面更适合夜间使用
- 设置会自动保存，下次启动时保持相同的界面主题

### 区域亮度调节

- 在"外观设置"中启用"区域亮度调节"功能
- 点击"选择区域"按钮，然后在屏幕上拖动鼠标选择需要调节亮度的区域
- 选择完成后亮度调节仅应用于选定区域
- 可以通过"清除区域"按钮恢复全屏亮度调节

### 定时功能

- 可以设置时间段（开始时间和结束时间）自动切换特定模式
- 支持设置跨日时间段（如晚上10点到次日早上6点）
- 在设定时间段内自动应用选定模式，时间段外恢复正常模式
- 支持的定时模式包括：护眼模式、夜间模式和防蓝光模式
- 结合开机自启动功能，可以实现日常使用的自动化亮度调节

### 其他功能

- 点击"官方网站"按钮可直接访问GitHub项目页面
- 通过"应用设置"按钮保存当前配置，下次启动自动应用
- "恢复默认"按钮可重置所有设置

## 开发说明

程序主要分为四个模块：

1. `main.py` - 程序入口，初始化和协调各模块
2. `main_window.py` - 用户界面模块，处理UI交互
3. `brightness_control.py` - 亮度控制核心模块，通过透明遮罩实现亮度控制
4. `floating_button.py` - 悬浮窗模块，实现屏幕上的悬浮控制功能

## 技术实现

程序通过在屏幕上覆盖一个半透明的遮罩层来调整屏幕显示的亮度。调整遮罩的透明度可以实现亮度的变化。这种方式虽不能改变显示器的实际硬件亮度，但可以达到类似的视觉效果，并且具有以下优势：

- 跨平台兼容性强
- 不需要管理员权限
- 可以应用于不支持硬件亮度调节的设备

### 最近修复的问题

- 修复了悬浮窗（如火绒流量窗口、右键菜单等）在遮罩层下方闪烁的问题
- 优化了遮罩层窗口的堆叠顺序，减少对其他窗口的干扰
- 改进了窗口属性设置，增强了与系统的兼容性
- 修复了启动时亮度设置不自动应用的问题
- 添加了暗黑模式和区域亮度调节功能

## 贡献指南

欢迎提交问题和改进建议！如果您想为项目做出贡献，请遵循以下步骤：

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 许可证

MIT

---

# English Version <a name="english-version"></a>

# Screen Brightness Tool

A cross-platform screen brightness adjustment tool based on PyQt5, which controls screen brightness by creating semi-transparent overlays.

## Features

- Smoothly adjust screen brightness via slider
- Support for multiple displays
- Preset brightness modes: Normal, Eye Protection, and Night modes
- High-contrast and Blue-light filter modes
- **Eye Protection Intensity Control**: Customize the brightness level (30%-90%) for eye protection mode
- System tray icon for background operation
- Auto-start on system boot
- Cross-platform compatibility (Windows, macOS, Linux)
- **Floating Widget**:
  - Displays system time and current brightness
  - Right-click and drag to position anywhere on screen
  - Customizable background and text colors
  - Auto-hides when main window is visible
- **Hotkey Support**: Exit application using Ctrl+E or custom hotkeys
- **Timer Function**: 
  - Supports time range setting with start and end times
  - Automatically applies selected mode during the set time range, and restores normal mode outside that range
  - Supports cross-day settings (e.g., 10 PM to 6 AM next day)
- **Dark Mode**: Toggle between dark and light application themes
- **Area Brightness Adjustment**: Select specific screen areas for brightness adjustment
- **Official Website**: Provides GitHub link for latest versions and issue reporting

## File Structure

The project consists of these main files:

- `main.py` - Program entry point that initializes and coordinates all modules
- `main_window.py` - UI module handling user interactions
- `brightness_control.py` - Core brightness control module implementing the overlay system
- `floating_button.py` - Floating widget module for on-screen brightness control
- `icon.png` - Application icon
- `requirements.txt` - List of dependencies

## Installation & Usage

### Requirements

- Python 3.6+
- PyQt5 5.15.0+

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Running the Program

```bash
python main.py
```

### Building Executables

#### Windows

```bash
# Basic build
pyinstaller --noconsole --onefile --icon=icon.png --name=ScreenBrightnessTool main.py

# Advanced build with version info
pyinstaller --noconsole --onefile --icon=icon.png --name=ScreenBrightnessTool --version-file=version.txt main.py
```

#### macOS

```bash
# Build standalone executable
pyinstaller --noconsole --onefile --icon=icon.icns --name=ScreenBrightnessTool main.py

# Build app bundle
pyinstaller --noconsole --windowed --icon=icon.icns --name=ScreenBrightnessTool main.py

# Create DMG installer (requires app bundle first)
hdiutil create -srcfolder "dist/ScreenBrightnessTool.app" -volname "ScreenBrightnessTool" -fs HFS+ -format UDBZ "dist/ScreenBrightnessTool.dmg"
```

#### Linux

```bash
# Basic build
pyinstaller --noconsole --onefile --name=ScreenBrightnessTool main.py

# Build AppImage (requires appimagetool)
# 1. Create with PyInstaller
pyinstaller --noconsole --name=ScreenBrightnessTool main.py
# 2. Create AppDir structure
# 3. Use appimagetool to build AppImage
```

## User Guide

### Main Window

1. Adjust screen brightness (10%-100%) using the slider
2. Customize Eye Protection mode intensity (30%-90%) for personal comfort
3. Click preset mode buttons to quickly change brightness:
   - Normal Mode (100% brightness)
   - Eye Protection Mode (customizable intensity, 70% by default)
   - Night Mode (40% brightness)
4. Check "Enhanced Contrast" to enable high contrast filter
5. Check "Blue Light Filter" to reduce screen blue light
6. Check "Start with system" to run the program on system startup
7. Closing the window minimizes the program to system tray

### Floating Widget

- Displays current system time and screen brightness
- **Left-click** to show menu for brightness adjustment and mode switching
- **Right-click and hold** to drag the widget, release to stop
- Customize background and text colors in "Floating Widget Settings"
- Automatically hides when main window is opened

### Hotkey Features

- Default Ctrl+E hotkey to exit the program
- Other preset hotkeys available: Ctrl+Q or Alt+F4

### Dark Mode

- Enable Dark Mode in "Appearance Settings" for more comfortable night-time use
- Settings are automatically preserved between application restarts

### Area Brightness Adjustment

- Enable "Area Brightness Adjustment" in "Appearance Settings"
- Click "Select Area" button, then drag on screen to select the region for brightness adjustment
- Selected area will be the only part affected by brightness changes
- Click "Clear Area" to return to full-screen brightness adjustment

### Timer Function

- Set time ranges (start and end times) for automatic mode switching
- Support cross-day time ranges (e.g., 10 PM to 6 AM next day)
- Automatically applies the selected mode during set time range, and restores normal mode outside that range
- Supported timer modes: Eye Protection, Night Mode, and Blue Light Filter
- Combined with auto-start, enables automated daily brightness control

### Other Features

- Click "Official Website" button to visit the GitHub project page
- Save current configuration using "Apply Settings" button for automatic application on next startup
- "Reset Defaults" button to restore all settings to their default values

## Development

The program consists of four main modules:

1. `main.py` - Program entry point, initializes and coordinates modules
2. `main_window.py` - User interface module, handles UI interactions
3. `brightness_control.py` - Core brightness control module using transparent overlays
4. `floating_button.py` - Floating widget module for on-screen control

## Technical Implementation

The program adjusts screen brightness by overlaying a semi-transparent mask on the screen. Changing the mask's opacity changes the perceived brightness. While this doesn't alter the actual hardware brightness, it achieves a similar visual effect with these advantages:

- Strong cross-platform compatibility
- No administrator privileges required
- Works on devices without hardware brightness adjustment support

### Recently Fixed Issues

- Fixed flickering issues with floating windows under the brightness overlay
- Optimized window stacking order to reduce interference with other windows
- Improved window property settings for better system compatibility
- Fixed brightness settings not automatically applying at startup
- Added Dark Mode and Area Brightness Adjustment features

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT 