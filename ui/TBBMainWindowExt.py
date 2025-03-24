from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Project.Controllers.AuthController import AuthController
from Project.Controllers.RegionController import RegionController
from Project.ui.QSTBBMainWindowExt import QSTBBMainWindowExt
from Project.ui.TBBMainWindow import Ui_MainWindow


class TBBMainWindowExt(QMainWindow, Ui_MainWindow):
    def __init__(self, on_start_questions):
        super().__init__()
        self.setupUi(self)

        # Sự kiện chuyển màn
        self.on_start_questions = on_start_questions

        # Controller điều khiển miền và dữ liệu người chơi
        self.region_controller = RegionController("TayBacBo")
        self.auth = AuthController()
        self.player = self.auth.get_current_player()

        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        self.pushButton.clicked.connect(self.start_first_province)

    def start_first_province(self):
        self.open_next_province()

    def open_next_province(self):
        province = self.region_controller.get_next_province()
        if not province:
            QMessageBox.information(self, "Chúc mừng", "Bạn đã hoàn thành miền TayBacBo!")
            if self.on_start_questions:
                self.on_start_questions("TayBacBo")  # Quay lại giao diện chọn miền
            self.close()
            return

        # Mở giao diện câu hỏi của tỉnh
        self.q_window = QSTBBMainWindowExt(province, self.on_question_complete)
        self.q_window.show()
        self.close()


    def on_question_complete(self, province, card_data):
        if not self.player.has_card(province):
            self.player.add_card(card_data)
            self.auth.save_players()

        self.open_next_province()