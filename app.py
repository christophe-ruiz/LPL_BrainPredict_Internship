from PySide2.QtWidgets import QMainWindow


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_infos()
        self.run()

    def set_infos(self):
        print('Setting initial position and size.')
        self.setGeometry(300, 300, 500, 250)
        print('Setting window title.')
        self.setWindowTitle('Prediction Data')

    def run(self):
        print('Running app')
        self.show()
