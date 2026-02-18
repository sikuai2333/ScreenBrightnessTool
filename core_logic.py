from datetime import time


def brightness_to_alpha(brightness_value):
    """将亮度值转换为遮罩透明度(alpha)。"""
    clamped = max(0, min(100, int(brightness_value)))
    return int(255 * (100 - clamped) / 100)


def is_time_in_range(current_time, start_time, end_time):
    """判断当前时间是否落在给定时间段内（支持跨天）。"""
    if not isinstance(current_time, time) or not isinstance(start_time, time) or not isinstance(end_time, time):
        raise TypeError("current_time/start_time/end_time 必须是 datetime.time 类型")

    # 开始时间与结束时间相同，视为全天生效
    if start_time == end_time:
        return True

    if start_time < end_time:
        return start_time <= current_time < end_time

    # 跨天区间，例如 22:00-06:00
    return current_time >= start_time or current_time < end_time
