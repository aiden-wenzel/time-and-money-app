from app import App
import os
import platform

dir_path = os.path.dirname(os.path.realpath(__file__))
current_os = platform.system()

if __name__=="__main__":
    app_root = os.path.split(dir_path)[0]
    data_path = os.path.join(app_root, "data/")
    app = App(data_path)
    app.run()