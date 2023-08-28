from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import io, os, time, math, pystray, winerror, sys, threading, win32event, win32gui, win32con, win32api
import tkinter as tk
from PIL import Image, ImageTk
from google.cloud import vision
from pystray import MenuItem as item

try:
    mutex = win32event.CreateMutex(None, 1, 'pashateki_SingleInstanceMutex')
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        mutex = None
        print("Another instance is already running. Exiting.")
        sys.exit(0)

    def monitor_shutdown():
        def on_shutdown_handler(hwnd, msg, wparam, lparam):
            if msg == win32con.WM_QUERYENDSESSION:
                print("Shutting down or restarting...")
                shutdown_event.set()  # シャットダウンイベントを設定
                return 0  # システムにシャットダウンを許可する
            return True

        win32gui.PumpMessages()

    shutdown_event = threading.Event()  # シャットダウンを検知するためのイベント
    shutdown_thread = threading.Thread(target=monitor_shutdown)
    shutdown_thread.start()

    # Google Cloud Vision APIのクライアントを初期化
    client = vision.ImageAnnotatorClient.from_service_account_file("GCP.json")

    # スクリーンショットの保存先ディレクトリ
    screenshot_dir = './sch'
    text_folder = 'text'

    root = None  # グローバル変数としてrootを定義

    def load_image(image_path):
        # 画像を読み込み、Google Vision APIに送信可能な形式に変換
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return image

    def extract_text(image):
        response = client.document_text_detection(image=image) 
        text_data = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = ''.join([symbol.text for symbol in word.symbols])
                        bounding_box = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices]
                        text_data.append({"text": word_text, "bounding_box": bounding_box})
        return text_data  # テキストデータとバウンディングボックスを返す

    def display_screenshot_and_text(image_path):
        global root  # グローバル変数rootを使用
        if root:  # rootが存在する場合、以前のウィンドウを破棄
            try:
                root.destroy()
            except tk.TclError:  # ウィンドウが既に破棄されている場合
                pass
        root = tk.Tk()
        image = load_image(image_path)
        text = extract_text(image)
        pil_image = Image.open(image_path)

        # スクリーンショットが一定の大きさを超えた場合、表示するスクリーンショットの大きさを制限
        max_width = 800
        max_height = 600
        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail((max_width, max_height))

        tk_image = ImageTk.PhotoImage(pil_image)
        image_label = tk.Label(root, image=tk_image)
        image_label.image = tk_image
        image_label.pack(side='left')
        text_widget = tk.Text(root, wrap='word')
        text_widget.pack(side='right', fill='both', expand=True)  # テキストウィジェットをウィンドウに合わせて伸縮
        
        text_data = extract_text(image)
        full_text = ""
        last_y = 0
        for item in text_data:
            text = item["text"]
            bounding_box = item["bounding_box"]
            x, y = bounding_box[0]

            if y > last_y + 10:
                full_text += '\n'
            else:
                full_text += ' '

            full_text += text
            last_y = y

        text_widget.insert(tk.END, full_text)  # この行を追加

        save_var = tk.IntVar()
        save_button = tk.Checkbutton(root, text='Save', variable=save_var)
        save_button.pack(side='bottom')


        def on_close():
            if save_var.get():
                text = text_widget.get('1.0', 'end')
                # 2. 画像のファイル名からテキストファイル名を作成
                image_file_name = os.path.basename(os.path.splitext(image_path)[0])
                text_file_path = os.path.join(text_folder, f"{image_file_name}.txt")
                with open(text_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
            os.remove(image_path)
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_close)
        root.geometry(f"{math.ceil(pil_image.width*2)}x{math.ceil(pil_image.height*2)}")  # スクリーンショットのサイズに合わせてウィンドウのサイズを設定
        root.update()
        root.mainloop()

    class ScreenshotHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory and any(event.src_path.endswith(ext) for ext in ['.jpg', '.png', '.jpeg']):
                display_screenshot_and_text(event.src_path)

    observer = Observer()
    observer.schedule(ScreenshotHandler(), screenshot_dir, recursive=False)
    observer.start()

    def exit_app(icon, item):
        icon.stop()
        observer.stop()
        os._exit(0)  # プログラムを強制終了

    def create_icon(icon_path):
        image = Image.open(icon_path)
        icon = pystray.Icon("name", image, "pashateki", menu=pystray.Menu(item('Quit', exit_app)))
        icon.run()

    icon_path = 'icon.ico'
    create_icon(icon_path)

    def reset_and_restart():
        print("An error occurred. Restarting the application...")
        # 現在のPythonスクリプトを再起動
        os.execl(sys.executable, sys.executable, *sys.argv)

    try:
        while True:
            time.sleep(1)  # メインスレッドが終了しないようにする
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    reset_and_restart()