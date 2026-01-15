import tkinter as tk
import threading
import time

class MouseCoordinateDisplay:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("鼠标坐标显示器")
        self.root.geometry("200x80")  # 小窗口尺寸
        self.root.resizable(False, False)  # 不可调整大小

        # 设置窗口始终置顶
        self.root.wm_attributes("-topmost", True)

        # 创建标签用于显示坐标
        self.coordinate_label = tk.Label(
            self.root,
            text="获取中...",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.coordinate_label.pack(expand=True)

        # 控制线程运行的标志
        self.running = True

        # 启动坐标更新线程
        self.update_thread = threading.Thread(target=self.update_coordinates, daemon=True)
        self.update_thread.start()

    def update_coordinates(self):
        """在后台线程中定期更新鼠标坐标"""
        import pyautogui

        while self.running:
            try:
                # 获取当前鼠标位置
                x, y = pyautogui.position()

                # 在主线程中更新UI
                self.root.after(0, lambda: self.coordinate_label.config(
                    text=f"X: {x}\nY: {y}"
                ))

                # 暂停0.5秒
                time.sleep(0.5)
            except Exception as e:
                print(f"更新坐标时出错: {e}")
                break

    def start(self):
        """启动窗口"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """窗口关闭时的清理操作"""
        self.running = False
        self.root.destroy()

def show_mouse_coordinate_window():
    """启动鼠标坐标显示窗口"""
    app = MouseCoordinateDisplay()
    app.start()

if __name__ == "__main__":
    show_mouse_coordinate_window()
