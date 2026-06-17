from app import App
import os
import platform

dir_path = os.path.dirname(os.path.realpath(__file__))
current_os = platform.system()

if __name__=="__main__":
    if current_os == "Windows":
        print(dir_path)
        app = App(dir_path + "\..\data\\")
        app.run()
    elif current_os == "Linux":
        app = App(dir_path + "/../data/")
        app.run()
    else:
        print("Your OS is not supported! Only Windows and Linux is supported") 