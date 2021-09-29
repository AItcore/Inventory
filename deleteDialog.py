from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QMessageBox


class DeleteDialog(QDialog):

    def __init__(self, whichBD, db, parent=None):
        super().__init__(parent)
        self.whichBD = whichBD
        self.db = db
        self.setWindowTitle("Удаление")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.message = QLabel("Выберите что удалить")
        self.comboBox = QComboBox()
        items = []
        if whichBD == 0:
            items = db.get_responsible_person()
        elif whichBD == 1:
            items = db.get_location()
        elif whichBD == 2:
            items = db.get_types()
        for i, item in enumerate(items):
            self.comboBox.insertItem(i, item[1])
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.exec()

    def accept(self):
        if self.whichBD == 0:
            id_res_pers = self.db.get_res_pers_id(self.comboBox.currentText())
            if self.db.count_item_res_pers(id_res_pers) == 0:
                self.db.delete_res_pers(id_res_pers)
            else:
                answer = QMessageBox(self)
                answer.setWindowTitle("Ошибка удаления")
                answer.setText("Данный пользователь назначен")
                answer.exec()
        elif self.whichBD == 1:
            id_location = self.db.get_location_id(self.comboBox.currentText())
            if self.db.count_item_location(id_location) == 0:
                self.db.delete_location(id_location)
            else:
                answer = QMessageBox(self)
                answer.setWindowTitle("Ошибка удаления")
                answer.setText("Данное местоположение назначено")
                answer.exec()
        elif self.whichBD == 2:
            id_type = self.db.get_type_id(self.comboBox.currentText())
            if self.db.count_item_type(id_type) == 0:
                self.db.delete_type(id_type)
            else:
                answer = QMessageBox(self)
                answer.setWindowTitle("Ошибка удаления")
                answer.setText("Данный тип оборудования используется")
                answer.exec()
        self.hide()

    def reject(self):
        self.hide()
