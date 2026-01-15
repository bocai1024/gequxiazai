import pygetwindow as gw
import tools
import logging
import json
import os


# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
PROGRESS_FILE = "progress.json"

def gequxiazai(gequmname):
    """
    酷我音乐歌曲下载函数

    Args:
        gequmname (str): 歌曲名称

    Returns:
        bool: 操作是否成功
    """
    try:
        # 查找酷我音乐窗口
        kuwo_windows = gw.getWindowsWithTitle('酷我音乐')
        if not kuwo_windows:
            logger.error("未找到酷我音乐窗口")
            return False

        kuwo = kuwo_windows[0]  # 获取第一个匹配的窗口
        logger.info(f"找到酷我音乐窗口: 位置({kuwo.left}, {kuwo.top}), 大小({kuwo.width}x{kuwo.height})")

        # 执行一系列点击操作
        operations = [
            {"x": kuwo.left + 265, "y": kuwo.top + 26, "text": gequmname, "action": "搜索歌曲"},
            {"x": kuwo.left + 554, "y": kuwo.top + 244, "action": "点击搜索结果"},
            {"x": kuwo.left + 357, "y": kuwo.top + 255, "action": "点击下载按钮"},
            {"x": kuwo.left + 384, "y": kuwo.top + 500, "action": "确认下载"}
        ]

        for i, op in enumerate(operations):
            try:
                logger.info(f"执行第{i + 1}步操作: {op['action']}")

                if 'text' in op:
                    # 带文本输入的操作
                    tools.click_at_shuru(op["x"], op["y"], op["text"])
                else:
                    # 仅点击操作
                    tools.click_at_shuru(op["x"], op["y"])

                logger.info(f"第{i + 1}步操作完成: {op['action']}")

            except Exception as e:
                logger.error(f"第{i + 1}步操作失败: {op['action']}, 错误: {str(e)}")
                return False

        logger.info(f"歌曲下载流程完成: {gequmname}")
        return True

    except gw.PyGetWindowException as e:
        logger.error(f"窗口操作异常: {str(e)}")
        return False
    except AttributeError as e:
        logger.error(f"窗口属性访问错误: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"函数执行出错: {str(e)}")
        return False


def load_progress(file_path):
    """
    加载文件处理进度

    Args:
        file_path (str): 要处理的文件路径

    Returns:
        int: 上次处理到的行号，默认为0
    """
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
            return progress_data.get(file_path, 0)
    return 0


def save_progress(file_path, line_num):
    """
    保存文件处理进度

    Args:
        file_path (str): 文件路径
        line_num (int): 当前行号
    """
    progress_data = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)

    progress_data[file_path] = line_num

    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)


def read_file_with_progress(file_path, encoding='utf-8'):
    """
    按行读取文件并跟踪进度

    Args:
        file_path (str): 文件路径
        encoding (str): 文件编码

    Yields:
        tuple: (行号, 行内容)
    """
    start_line = load_progress(file_path)
    current_line = 0

    with open(file_path, 'r', encoding=encoding) as file:
        for line_num, line in enumerate(file):
            content = line.rstrip('\n\r')

            # 如果当前行号小于起始行号，跳过
            if line_num < start_line:
                continue

            yield line_num, content
            current_line = line_num + 1
            # 实时保存进度
            save_progress(file_path, current_line)


def process_song_file(file_path):
    """
    处理歌曲文件

    Args:
        file_path (str): 歌曲列表文件路径
    """
    total_lines = sum(1 for line in open(file_path, 'r', encoding='utf-8'))
    start_line = load_progress(file_path)

    print(f"文件总行数: {total_lines}")
    print(f"从第 {start_line + 1} 行开始处理")

    for line_num, song_name in read_file_with_progress(file_path):
        if song_name.strip():  # 跳过空行
            print(f"处理第 {line_num + 1} 行: {song_name}")
            success = gequxiazai(song_name)
            if success:
                print(f"成功处理: {song_name}")
            else:
                print(f"处理失败: {song_name}")
                break  # 如果处理失败，可以选择中断或继续
        else:
            # 即使是空行也更新进度
            save_progress(file_path, line_num + 1)

    print("文件处理完成")


if __name__ == '__main__':
    process_song_file('songs_smart_deduplicated.txt')