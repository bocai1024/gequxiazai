import time

import pyautogui

def find_image_position(image_path, confidence=0.8):
    """
    仅查找图片位置不点击

    Args:
        image_path (str): 图片路径
        confidence (float): 匹配置信度

    Returns:
        tuple: (bool, x, y) 是否找到，坐标x，坐标y
    """
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center_x, center_y = pyautogui.center(location)
            return True, center_x, center_y
    except:
        pass
    return False, None, None


if __name__ == '__main__':
    time.sleep(5)
    print(find_image_position('shoucang.png'))