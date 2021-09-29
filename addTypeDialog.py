from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QMessageBox, QGridLayout, QLineEdit, QGroupBox


class AddTypeDialog(QDialog):

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Добавление типа оборудования")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()

        self.labelType = QLabel("Тип оборудования")
        self.inputType = QLineEdit()

        self.labelCount = QLabel("Количество характеристик")
        self.inputCount = QLineEdit()
        self.inputCount.setMaxLength(1)
        self.inputCount.setText('0')
        self.inputCount.setInputMask('9')
        self.inputCount.textChanged.connect(self.change_count)

        self.groupBox = QGroupBox("Характеристики")

        self.gridBox = QGridLayout()

        self.labelCharacteristic = []
        self.inputCharacteristic = []

        self.groupBox.setLayout(self.gridBox)

        self.layout.addWidget(self.labelType, 0, 0)
        self.layout.addWidget(self.inputType, 0, 1)
        self.layout.addWidget(self.labelCount, 1, 0)
        self.layout.addWidget(self.inputCount, 1, 1)

        self.layout.addWidget(self.groupBox, 2, 0, 7, 2)

        self.layout.addWidget(self.buttonBox, 15, 0, 1, 2)

        self.setLayout(self.layout)

    def change_count(self):
        if self.inputCount.text().isdigit():
            count = int(self.inputCount.text())
            if count != len(self.inputCharacteristic) and count <= 6:
                for i in self.inputCharacteristic:
                    self.gridBox.removeWidget(i)
                for i in self.labelCharacteristic:
                    self.gridBox.removeWidget(i)
                self.inputCharacteristic = []
                self.labelCharacteristic = []
                for i in range(count):
                    label = QLabel("Название характеристики")
                    self.labelCharacteristic.append(label)
                    self.gridBox.addWidget(label, 3+i, 0)
                    inputBox = QLineEdit()
                    self.inputCharacteristic.append(inputBox)
                    self.gridBox.addWidget(inputBox, 3+i, 1)

    def accept(self):
        type = self.inputType.text()
        type = type[0].upper() + type[1:]
        if not self.db.exist_type(type):
            self.db.insert_type(type)
            id_type = self.db.get_type_id(type)
            for i in self.inputCharacteristic:
                text = i.text()[0].upper() + i.text()[1:]
                self.db.insert_characteristic(text, id_type)
            self.hide()
        else:
            mes = QMessageBox(self)
            mes.setWindowTitle("Ошибка")
            mes.setText("Данный тип оборудования существует")
            mes.exec()

    def reject(self):
        self.hide()
