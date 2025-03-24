from PyQt6.QtWidgets import QMainWindow

from Project.ui.MainWindow import Ui_MainWindow


class MainWindowExt(QMainWindow, Ui_MainWindow):
    def __init__(self, username=None, auth=None, on_play_clicked=None):
        super().__init__()
        self.setupUi(self)
        self.username = username
        self.auth = auth
        self.on_play_clicked = on_play_clicked
        self.setup_events()

    def setup_events(self):
        self.pushButton.clicked.connect(self.start_game)

    def start_game(self):
        print(f"Người chơi {self.username} bắt đầu khám phá!")
        print(f"[DEBUG] current_player trong MainWindowExt: {self.auth.get_current_player()}")
        if self.on_play_clicked:
            self.on_play_clicked()
