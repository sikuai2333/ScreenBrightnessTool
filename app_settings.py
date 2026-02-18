from PyQt5.QtCore import QSettings

ORGANIZATION_NAME = "BrightnessControl"
APPLICATION_NAME = "BrightnessAdjuster"


def create_settings():
    """创建统一配置对象，避免散落硬编码。"""
    return QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
