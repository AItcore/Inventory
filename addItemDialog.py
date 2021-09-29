from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QGridLayout, QLineEdit, QGroupBox, QComboBox, QCompleter
from database import Database


class AddItemDialog(QDialog):

    def __init__(self, db: Database, id, parent=None):
        super().__init__(parent)
        self.db = db
        self.id = id
        self.setWindowTitle("Добавление оборудования")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()

        self.inputsCharacteristic = []
        self.labelCharacteristic = []

        self.labelID = QLabel("ID")
        self.inputBoxID = QLineEdit()
        self.inputBoxID.setDisabled(True)
        self.inputBoxID.setText(id)

        self.labelType = QLabel("Тип оборудования")
        self.comboBoxTypes = QComboBox()

        self.typeModel = QStandardItemModel()

        for item in self.db.get_types():
            self.typeModel.appendRow(QStandardItem(item[1]))

        self.inpSerialNumber = QLineEdit()
        self.labelSerialNumber = QLabel()
        self.labelSerialNumber.setText("Серийный номер")

        self.inputBoxLocation = QLineEdit()
        self.labelLocation = QLabel()
        self.labelLocation.setText("Месторасположение")

        locations = self.db.get_location()
        self.loc_model = QStandardItemModel()

        for i, loc in enumerate(locations):
            self.loc_model.appendRow(QStandardItem(loc[1]))

        completer_loc = QCompleter(self.loc_model, self)
        completer_loc.setCaseSensitivity(Qt.CaseInsensitive)
        completer_loc.setCompletionRole(Qt.DisplayRole)
        completer_loc.setCompletionColumn(0)

        self.inputBoxLocation.setCompleter(completer_loc)

        self.inputBoxResponsiblePerson = QLineEdit()
        self.labelResponsiblePerson = QLabel()
        self.labelResponsiblePerson.setText("Ответственное лицо")

        responsible_persons = self.db.get_responsible_person()
        self.res_pers_model = QStandardItemModel()
        for i, res_pers in enumerate(responsible_persons):
            self.res_pers_model.appendRow(QStandardItem(res_pers[1]))

        completer_res_pers = QCompleter(self.res_pers_model, self)
        completer_res_pers.setCaseSensitivity(Qt.CaseInsensitive)
        completer_res_pers.setCompletionRole(Qt.DisplayRole)
        completer_res_pers.setCompletionColumn(0)
        self.inputBoxResponsiblePerson.setCompleter(completer_res_pers)

        self.groupBox = QGroupBox("Характеристики")

        self.gridBox = QGridLayout()

        self.labelCharacteristic = []
        self.inputCharacteristic = []

        self.groupBox.setLayout(self.gridBox)

        self.layout.addWidget(self.labelID, 0, 0)
        self.layout.addWidget(self.inputBoxID, 0, 1)

        self.layout.addWidget(self.labelType, 1, 0)
        self.layout.addWidget(self.comboBoxTypes, 1, 1)

        self.layout.addWidget(self.labelSerialNumber, 2, 0)
        self.layout.addWidget(self.inpSerialNumber, 2, 1)

        self.layout.addWidget(self.labelLocation, 3, 0)
        self.layout.addWidget(self.inputBoxLocation, 3, 1)

        self.layout.addWidget(self.labelResponsiblePerson, 4, 0)
        self.layout.addWidget(self.inputBoxResponsiblePerson, 4, 1)

        self.layout.addWidget(self.groupBox, 5, 0, 7, 2)

        self.layout.addWidget(self.buttonBox, 15, 0, 1, 2)

        self.comboBoxTypes.currentIndexChanged.connect(self.change_type)

        self.comboBoxTypes.setModel(self.typeModel)

        self.setLayout(self.layout)

    def change_type(self):
        for elem in self.inputsCharacteristic:
            self.gridBox.removeWidget(elem)
        for elem in self.labelCharacteristic:
            self.gridBox.removeWidget(elem)
        self.inputsCharacteristic = []
        self.labelCharacteristic = []
        type_id = self.db.get_type_id(self.comboBoxTypes.currentText())
        requiredCharacteristics = self.db.get_characteristics(type_id)
        if requiredCharacteristics is not None:
            requiredCharacteristics.sort(key=lambda k: k[1])
            for i, elem in enumerate(requiredCharacteristics):
                input = QLineEdit()
                label = QLabel(elem[1])
                self.gridBox.addWidget(label, 6 + i, 0)
                self.gridBox.addWidget(input, 6 + i, 1)
                self.labelCharacteristic.append(label)
                self.inputsCharacteristic.append(input)

    def accept(self):
        text_characteristic = ''
        for i in range(len(self.inputsCharacteristic)):
            text_characteristic += self.labelCharacteristic[i].text() + ": " + self.inputsCharacteristic[
                i].text() + "\n"
        if self.db.get_res_pers_id(self.inputBoxResponsiblePerson.text().title()) is None:
            self.db.insert_res_pers(self.inputBoxResponsiblePerson.text().title())
        if self.db.get_location_id(self.inputBoxLocation.text().title()) is None:
            self.db.insert_location(self.inputBoxLocation.text().title())
        item = {
            'id': self.id,
            'type': self.db.get_type_id(self.comboBoxTypes.currentText()),
            'characteristic': text_characteristic,
            'serial_number': self.inpSerialNumber.text(),
            'location': self.db.get_location_id(self.inputBoxLocation.text().title()),
            'responsible_person': self.db.get_res_pers_id(self.inputBoxResponsiblePerson.text().title())
        }
        self.db.insert_item(item)
        self.hide()

    def reject(self):
        self.hide()
