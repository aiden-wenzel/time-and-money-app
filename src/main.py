from app import App
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__=="__main__":
    app = App(dir_path + "/../data/money_data.csv")
    app.run()