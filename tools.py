import pyautogui
import time
import pyperclip
import re

def click_at_shuru(x, y, text_to_input=None, select_all_first=True, click_type=0, delay_after_click=0.5):
    """
    改进版坐标点击函数，支持文本输入

    Args:
        x (int): X坐标
        y (int): Y坐标
        text_to_input (str, optional): 要输入的文本
        click_type (int): 点击类型，0为左键，1为右键，默认为0
        delay_after_click (float): 点击后等待时间
        select_all_first (bool): 是否先全选清空原内容
    """
    # 移动鼠标到指定坐标
    pyautogui.moveTo(x, y)
    time.sleep(0.1)

    # 执行点击操作
    if click_type == 0:  # 左键点击
        pyautogui.click(x, y)
    elif click_type == 1:  # 右键点击
        pyautogui.rightClick(x, y)

    # 如果提供了文本，则输入文本
    if text_to_input is not None:
        # 等待目标控件响应点击操作
        time.sleep(delay_after_click)
        if select_all_first:
            # 全选并删除现有内容
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('backspace')
            time.sleep(0.1)

        # 输入新文本
        pyperclip.copy(text_to_input)  # 复制文本到剪贴板
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')  # 粘贴文本
        time.sleep(0.2)

def smart_remove_duplicate_songs(input_filename='songs.txt', output_filename='songs_smart_deduplicated.txt'):
    """
    智能去重函数 - 识别相似歌曲名并保留一个版本

    Args:
        input_filename (str): 输入文件名
        output_filename (str): 输出文件名

    Returns:
        int: 去重后的歌曲数量
    """
    # 读取文件
    with open(input_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    songs = [line.strip() for line in lines if line.strip()]

    # 智能去重逻辑
    processed_titles = {}  # 存储标准化标题 -> 原标题的映射

    for song in songs:
        # 标准化歌曲名：移除版本信息、演员信息等
        normalized = normalize_song_title(song)

        # 如果标准化标题未出现过，或者当前版本更简洁，则保留
        if normalized not in processed_titles:
            processed_titles[normalized] = song
        else:
            # 比较两个版本，保留更简洁的版本
            existing_version = processed_titles[normalized]
            if is_better_version(song, existing_version):
                processed_titles[normalized] = song

    unique_songs = list(processed_titles.values())

    # 保存结果
    with open(output_filename, 'w', encoding='utf-8') as f:
        for song in unique_songs:
            f.write(song + '\n')

    print(f"原文件包含 {len(songs)} 首歌曲")
    print(f"智能去重后剩余 {len(unique_songs)} 首歌曲")
    print(f"删除了 {len(songs) - len(unique_songs)} 个重复/相似项")
    print(f"结果已保存到 {output_filename}")

    return len(unique_songs)

def normalize_song_title(title):
    """
    标准化歌曲标题，移除版本信息、演员信息等

    Args:
        title (str): 原始歌曲标题

    Returns:
        str: 标准化后的标题
    """
    # 移除括号内的电影/电视剧信息
    normalized = re.sub(r'\s*[（\(][^）\)]*[）\)][^（\(]*$', '', title)
    # 移除演员信息（如 "韩红/孙楠", "胡歌\白冰"）
    normalized = re.sub(r'\s*[-–]\s*[^/\n]+[/\\][^/\n]+$', '', normalized)
    # 移除其他附加信息
    normalized = re.sub(r'\s+[.-]\s+.*$', '', normalized)

    return normalized.strip()

def is_better_version(new_version, existing_version):
    """
    判断新版本是否比现有版本更好（更简洁或更有代表性）

    Args:
        new_version (str): 新版本标题
        existing_version (str): 现有版本标题

    Returns:
        bool: 新版本是否更优
    """
    # 优先保留不含额外信息的版本
    new_clean = normalize_song_title(new_version)
    existing_clean = normalize_song_title(existing_version)

    # 如果新版本更简洁，且原始标题长度相当，则优选简洁版本
    if len(new_version) < len(existing_version) and new_clean == existing_clean:
        return True

    # 优先保留不包含演员信息的版本
    if has_actor_info(existing_version) and not has_actor_info(new_version):
        return True

    # 优先保留不包含版本信息的版本
    if has_version_info(existing_version) and not has_version_info(new_version):
        return True

    # 否则保持原有版本
    return False

def has_actor_info(title):
    """
    检查标题是否包含演员信息

    Args:
        title (str): 歌曲标题

    Returns:
        bool: 是否包含演员信息
    """
    return bool(re.search(r'[-–]\s*[^/\n]+[/\\][^/\n]+', title))

def has_version_info(title):
    """
    检查标题是否包含版本信息（如电影、电视剧名称）

    Args:
        title (str): 歌曲标题

    Returns:
        bool: 是否包含版本信息
    """
    return bool(re.search(r'[（\(][^）\)]*[）\)]', title))

