<!--
 * @Author: sikuai2333 2643927725@qq.com
 * @Date: 2025-04-26 10:08:35
 * @LastEditors: sikuai2333 2643927725@qq.com
 * @LastEditTime: 2025-04-26 10:55:31
 * @FilePath: \屏幕亮度调节\README.md
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
- 系统托盘图标，最小化后仍可运行
- 开机自启动设置
- 跨平台支持（Windows、macOS、Linux）
- **悬浮窗功能**：
  - 显示系统时间和当前亮度值
  - 右键拖拽可在屏幕任意位置停靠
  - 自定义悬浮窗背景颜色和文字颜色
  - 主窗口打开时自动隐藏，关闭或最小化时显示
- **热键支持**：支持使用Ctrl+E或自定义热键退出软件
- **定时功能**：可在指定时间自动切换预设模式


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

### 打包exe

1. 安装PyInstaller:
```bash
pip install pyinstaller
```
2. 打包
```bash
pyinstaller main.py --no-console
```



## 使用说明

### 主窗口功能

1. 通过滑动条调整屏幕亮度（10%-100%）
2. 点击预设模式按钮快速切换亮度：
   - 正常模式（100%亮度）
   - 护眼模式（70%亮度）
   - 夜间模式（40%亮度）
3. 勾选"增强对比度"可启用高对比度滤镜
4. 勾选"防蓝光模式"可减少屏幕蓝光
5. 勾选"开机自启动"可设置系统启动时自动运行
6. 关闭窗口时程序会最小化到系统托盘，点击托盘图标可重新打开界面

### 悬浮窗功能

- 显示当前系统时间和屏幕亮度值
- **左键点击**悬浮窗显示菜单，可调整亮度、切换模式或显示主窗口
- **右键长按**悬浮窗实现拖拽，松开鼠标停止拖拽
- 在主窗口的"悬浮窗设置"中可以自定义背景颜色和文字颜色
- 当打开主窗口时，悬浮窗会自动隐藏

### 热键功能

- 默认使用Ctrl+E快捷键退出程序
- 可以在设置中选择其他预设热键：Ctrl+Q或Alt+F4

### 定时功能

- 可以设置在指定时间自动切换到特定模式
- 支持的定时模式包括：护眼模式、夜间模式和防蓝光模式
- 结合开机自启动功能，可以实现日常使用的自动化亮度调节

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
- System tray icon for background operation
- Auto-start on system boot
- Cross-platform compatibility (Windows, macOS, Linux)
- **Floating Widget**:
  - Displays system time and current brightness
  - Right-click and drag to position anywhere on screen
  - Customizable background and text colors
  - Auto-hides when main window is visible
- **Hotkey Support**: Exit application using Ctrl+E or custom hotkeys
- **Timer Function**: Automatically switch to preset modes at specified times

## Screenshots

_Screenshots can be added here_

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

## User Guide

### Main Window

1. Adjust screen brightness (10%-100%) using the slider
2. Click preset mode buttons to quickly change brightness:
   - Normal Mode (100% brightness)
   - Eye Protection Mode (70% brightness)
   - Night Mode (40% brightness)
3. Check "Enhanced Contrast" to enable high contrast filter
4. Check "Blue Light Filter" to reduce screen blue light
5. Check "Start with system" to run the program on system startup
6. Closing the window minimizes the program to system tray

### Floating Widget

- Displays current system time and screen brightness
- **Left-click** to show menu for brightness adjustment and mode switching
- **Right-click and hold** to drag the widget, release to stop
- Customize background and text colors in "Floating Widget Settings"
- Automatically hides when main window is opened

### Hotkey Features

- Default Ctrl+E hotkey to exit the program
- Other preset hotkeys available: Ctrl+Q or Alt+F4

### Timer Function

- Set automatic mode switching at specified times
- Supported timer modes: Eye Protection, Night Mode, and Blue Light Filter
- Combined with auto-start, enables automated daily brightness control

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

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT 