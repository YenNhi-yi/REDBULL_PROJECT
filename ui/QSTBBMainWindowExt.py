import os
import random
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from Project.Controllers.AuthController import AuthController
from Project.Controllers.RegionController import RegionController
from Project.Models.Culturecard import CultureCard
from Project.ui.CoLenExt import CoLenExt
from Project.ui.CorrectExt import CorrectExt
from Project.ui.QSTBBMainWindow import Ui_MainWindow
from Project.ui.TBB_HTExt import TBB_HTExt


class QSTBBMainWindowExt(QMainWindow, Ui_MainWindow):
    def __init__(self, province_name, auth, on_question_complete=None):
        super().__init__()
        self.setupUi(self)
        self.auth = auth

        image_path = os.path.join("images", "qstbb.png")
        if os.path.exists(image_path):
            self.label.setPixmap(QPixmap(image_path))
            self.label.setScaledContents(True)
        else:
            print("Ảnh nền không tồn tại:", image_path)
        self.province_name = province_name
        self.on_question_complete = on_question_complete
        self.auth = AuthController()
        self.region_controller = RegionController("TayBacBo")

        self.questions = self.region_controller.dc.get_questions_by_province(province_name).copy()
        self.current_question = None
        self.previous_question = None
        self.provinces_answered = set()

        self.setup_events()
        self.load_question()

    def setup_events(self):
        self.pushButton_A.clicked.connect(lambda: self.check_answer("A"))
        self.pushButton_B.clicked.connect(lambda: self.check_answer("B"))
        self.pushButton_C.clicked.connect(lambda: self.check_answer("C"))
        self.pushButton_D.clicked.connect(lambda: self.check_answer("D"))

    def load_question(self):
        if not self.questions:
            self.ht_screen = TBB_HTExt(parent_to_close=self)
            self.ht_screen.show()
            return
        if len(self.questions) == 1:
            self.current_question = self.questions[0]
        else:
            while True:
                candidate = random.choice(self.questions)
                if candidate != self.previous_question:
                    self.current_question = candidate
                    break
        self.current_question = random.choice(self.questions)

        if "question" not in self.current_question or "options" not in self.current_question:
            QMessageBox.critical(self, "Lỗi dữ liệu", "Thiếu trường 'question' hoặc 'options'")
            self.close()
            return

        options = self.current_question["options"]

        self.label_Qs.setText(self.current_question["question"])
        self.label_A.setText(options.get("A", ""))
        self.label_B.setText(options.get("B", ""))
        self.label_C.setText(options.get("C", ""))
        self.label_D.setText(options.get("D", ""))

    def check_answer(self, user_choice):
        correct_answer = self.current_question["answer"]
        if user_choice == correct_answer:
            card_info = self.current_question.get("culture_card", {})
            card = CultureCard(
                province=card_info.get("province", self.province_name),
                title=card_info.get("text", self.current_question["question"]),
                image=card_info.get("image_path", "")
            )

            player = self.auth.get_current_player()
            if player:
                player.add_card(card)
                self.auth.save_players()

            self.provinces_answered.add(self.province_name)
            if self.current_question in self.questions:
                self.questions.remove(self.current_question)

            image_path = card.image or "images/default.png"
            if not os.path.exists(image_path):
                image_path = "images/default.png"

            # MỞ GIAO DIỆN CORRECT
            self.correct_popup = CorrectExt(
                image_path=image_path,
                on_next_callback=self.handle_correct_done
            )
            self.correct_popup.show()
        else:
            self.incorrect_popup = CoLenExt(on_next_callback=self.load_question)
            self.incorrect_popup.show()

    def handle_correct_done(self):
        self.load_question()


