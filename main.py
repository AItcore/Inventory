import sys
from datetime import datetime
import threading
import re
from printDialog import PrintDialog
from addItemDialog import AddItemDialog
from addTypeDialog import AddTypeDialog
from database import Database
from deleteDialog import DeleteDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication, QTableWidget, QLineEdit, QLabel, \
    QTableWidgetItem, QGroupBox, QHeaderView, QComboBox, QMessageBox, QMainWindow, QAction, QInputDialog, QCompleter
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        # Настройка шрифта
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(12)
        self.setFont(self.font)

        # Создание меню
        self.create_menu()

        # Создание слоёв
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.layoutInput = QGridLayout()
        self.groupBox = QGroupBox("Добавление данных")
        self.gridBox = QGridLayout()

        # Создание элементов
        self.inputsCharacteristic = []
        self.labelCharacteristic = []
        self.comboBoxLocTabel = []
        self.comboBoxResPerTabel = []

        self.inpSearch = QLineEdit()
        self.labelSearch = QLabel()
        self.labelSearch.setText("Поиск")

        self.labelSerType = QLabel("По типу")

        self.comboBoxTypes = QComboBox()
        self.cbTypesFilter = QComboBox()
        types = self.get_types()
        for i, item in enumerate(types):
            self.comboBoxTypes.insertItem(i, item)
            self.cbTypesFilter.insertItem(i, item)
        self.cbTypesFilter.insertItem(0, "Все")
        self.cbTypesFilter.setCurrentIndex(0)

        self.btnAdd = QPushButton()
        self.btnAdd.setText("Добавить")
        self.btnAdd.setMinimumSize(90, 40)

        self.labelType = QLabel()
        self.labelType.setText("Тип оборудования")

        self.inpSerialNumber = QLineEdit()
        self.labelSerialNumber = QLabel()
        self.labelSerialNumber.setText("Серийный номер")

        self.inputBoxLocation = QLineEdit()
        self.labelLocation = QLabel()
        self.labelLocation.setText("Месторасположение")
        self.labelSerLoc = QLabel()
        self.labelSerLoc.setText("Месторасположение")
        self.cbLocFilter = QComboBox()
        locations = self.db.get_location()
        self.loc_model = QStandardItemModel()

        for i, loc in enumerate(locations):
            self.loc_model.appendRow(QStandardItem(loc[1]))
            self.cbLocFilter.insertItem(i, loc[1])

        completer_loc = QCompleter(self.loc_model, self)
        completer_loc.setCaseSensitivity(Qt.CaseInsensitive)
        completer_loc.setCompletionRole(Qt.DisplayRole)
        completer_loc.setCompletionColumn(0)

        self.inputBoxLocation.setCompleter(completer_loc)
        self.cbLocFilter.insertItem(0, "Все")
        self.cbLocFilter.setCurrentIndex(0)

        self.inputBoxResponsiblePerson = QLineEdit()
        self.cbResPersFilter = QComboBox()
        self.labelResponsiblePerson = QLabel()
        self.labelResponsiblePerson.setText("Ответственное лицо")
        self.labelSerResPers = QLabel()
        self.labelSerResPers.setText("Ответственное лицо")
        responsible_persons = self.db.get_responsible_person()
        self.res_pers_model = QStandardItemModel()
        for i, res_pers in enumerate(responsible_persons):
            self.res_pers_model.appendRow(QStandardItem(res_pers[1]))
            self.cbResPersFilter.insertItem(i, res_pers[1])

        completer_res_pers = QCompleter(self.res_pers_model, self)
        completer_res_pers.setCaseSensitivity(Qt.CaseInsensitive)
        completer_res_pers.setCompletionRole(Qt.DisplayRole)
        completer_res_pers.setCompletionColumn(0)
        self.inputBoxResponsiblePerson.setCompleter(completer_res_pers)

        self.cbResPersFilter.insertItem(0, "Все")
        self.cbResPersFilter.setCurrentIndex(0)

        self.btnSearch = QPushButton()
        self.btnSearch.setText("Найти")

        self.table = self.__create_table()
        self.fill_table(self.db.get_items())

        # Размещение слоёв
        self.layoutInput.addWidget(self.labelSearch, 0, 0)
        self.layoutInput.addWidget(self.inpSearch, 0, 1)
        self.layoutInput.addWidget(self.labelSerType, 0, 2)
        self.layoutInput.addWidget(self.cbTypesFilter, 0, 3)
        self.layoutInput.addWidget(self.labelSerLoc, 0, 4)
        self.layoutInput.addWidget(self.cbLocFilter, 0, 5)
        self.layoutInput.addWidget(self.labelSerResPers, 0, 6)
        self.layoutInput.addWidget(self.cbResPersFilter, 0, 7)
        self.layoutInput.addWidget(self.btnSearch, 0, 8)

        self.layoutInput.addWidget(self.groupBox, 1, 0, 3, 9)

        # Размещение объектов в GroupBox
        self.groupBox.setLayout(self.gridBox)
        self.font.setPointSize(10)
        self.groupBox.setFont(self.font)

        self.gridBox.addWidget(self.labelType, 0, 0)
        self.gridBox.addWidget(self.comboBoxTypes, 0, 1)

        self.gridBox.addWidget(self.labelLocation, 0, 2)
        self.gridBox.addWidget(self.inputBoxLocation, 0, 3)

        self.gridBox.addWidget(self.labelSerialNumber, 1, 0)
        self.gridBox.addWidget(self.inpSerialNumber, 1, 1)

        self.gridBox.addWidget(self.labelResponsiblePerson, 1, 2)
        self.gridBox.addWidget(self.inputBoxResponsiblePerson, 1, 3)

        self.gridBox.addWidget(self.btnAdd, 1, 10)
        # self.btnAdd.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.grid.addWidget(self.table, 0, 0, 1, 1)
        self.grid.addLayout(self.layoutInput, 1, 0, 1, 1)

        # Подключение событий
        self.inpSearch.textChanged.connect(self.search_input)
        self.comboBoxTypes.currentIndexChanged.connect(self.change_input)
        self.btnAdd.clicked.connect(self.add_item)
        self.btnSearch.clicked.connect(self.search)

        self.mainLayout = QWidget()
        self.mainLayout.setLayout(self.grid)
        self.setCentralWidget(self.mainLayout)
        self.change_input()
        self.setWindowTitle('Инвентаризация')
        self.setMinimumSize(600, 600)
        self.setGeometry(300, 25, 700, 700)
        self.showMaximized()
        self.show()

        self.statusBar().showMessage("Database loaded", 3000)

    def update_mode(self):
        if self.editMode:
            for elem in self.comboBoxLocTabel:
                elem.setDisabled(self.editMode)
            for elem in self.comboBoxResPerTabel:
                elem.setDisabled(self.editMode)
            self.editMode = False
        else:
            for elem in self.comboBoxLocTabel:
                elem.setDisabled(self.editMode)
            for elem in self.comboBoxResPerTabel:
                elem.setDisabled(self.editMode)
            self.editMode = True

    def inventory_mode(self):
        if not self.inventoryMode:
            self.inventoryModeItemsID = []
            self.comboBoxLocTabel = []
            self.comboBoxResPerTabel = []
            self.table.clear()
            self.table_header()
            self.table.setRowCount(0)
            self.inventoryMode = not self.inventoryMode
        else:
            self.search()
            self.inventoryMode = not self.inventoryMode

    def create_menu(self):
        # Действия
        addResPersAction = QAction("Добавить ответственное лицо", self)
        addResPersAction.triggered.connect(self.add_res_pers)

        deleteResPersAction = QAction("Удалить ответственное лицо", self)
        deleteResPersAction.triggered.connect(self.delete_res_pers)

        addLocationAction = QAction("Добавить месторасположение", self)
        addLocationAction.triggered.connect(self.add_location)

        deleteLocationAction = QAction("Удалить местоположение", self)
        deleteLocationAction.triggered.connect(self.delete_location)

        addTypeAction = QAction("Добавить тип оборудования", self)
        addTypeAction.triggered.connect(self.add_type)

        deleteTypeAction = QAction("Удалить тип оборудования", self)
        deleteTypeAction.triggered.connect(self.delete_type)

        editMode = QAction("Режим редактирования", self)
        editMode.triggered.connect(self.update_mode)

        inventoryMode = QAction("Режим инвентаризации", self)
        inventoryMode.triggered.connect(self.inventory_mode)

        printLabel = QAction("Создать документ штрихкодов", self)
        printLabel.triggered.connect(self.print_label)
        # Меню бар
        menubar = self.menuBar()
        # Добавление
        addMenu = menubar.addMenu("&Добавить")
        addMenu.addAction(addResPersAction)
        addMenu.addAction(addLocationAction)
        addMenu.addAction(addTypeAction)
        addMenu.addAction(printLabel)

        # Удаление
        deleteMenu = menubar.addMenu("&Удалить")
        deleteMenu.addAction(deleteResPersAction)
        deleteMenu.addAction(deleteLocationAction)
        deleteMenu.addAction(deleteTypeAction)

        # Режимы
        modeMenu = menubar.addMenu("&Режимы")
        modeMenu.addAction(editMode)
        modeMenu.addAction(inventoryMode)
        self.editMode = False
        self.inventoryMode = False
        self.print = False

    def print_label(self):
        dlg = PrintDialog(self)
        dlg.exec()

    def add_res_pers(self):
        text, ok = QInputDialog.getText(self, 'Добавить ответственное лицо',
                                        'Введите ФИО:')
        if ok:
            text = text.title()
            self.db.insert_res_pers(text)
            self.cbResPersFilter.insertItem(1, text)
            self.res_pers_model.appendRow(QStandardItem(text))
            for i in self.comboBoxResPerTabel:
                i.insertItem(1, text)
            self.statusBar().showMessage("Новое ответственное лицо добавлен", 5000)

    def add_location(self):
        text, ok = QInputDialog.getText(self, 'Добавить новое местоположение',
                                        'Введите название:')
        if ok:
            text = text[0].upper() + text[1:]
            self.db.insert_location(text)
            self.cbLocFilter.insertItem(1, text)
            self.loc_model.appendRow(text)
            for i in self.comboBoxLocTabel:
                i.insertItem(1, text)
            self.statusBar().showMessage("Новое местоположение добавлено", 5000)

    def add_type(self):
        count = self.db.count_type()
        dialog = AddTypeDialog(self.db, self)
        dialog.exec()
        if count < self.db.count_type():
            model = QStandardItemModel()
            self.comboBoxTypes.clear()
            self.cbTypesFilter.clear()
            for elem in self.db.get_types():
                model.appendRow(QStandardItem(elem[1]))
            self.comboBoxTypes.setModel(model)
            self.cbTypesFilter.setModel(model)
            self.statusBar().showMessage("Новый тип оборудования добавлен", 5000)

    def delete_res_pers(self):
        count = self.db.count_res_pers()
        DeleteDialog(0, self.db, self)
        if count > self.db.count_res_pers():
            responsible_persons = self.db.get_responsible_person()
            self.res_pers_model = QStandardItemModel()

            for res_pers in responsible_persons:
                self.res_pers_model.appendRow(QStandardItem(res_pers[1]))

            completer_res_pers = QCompleter(self.res_pers_model, self)
            completer_res_pers.setCaseSensitivity(Qt.CaseInsensitive)
            completer_res_pers.setCompletionRole(Qt.DisplayRole)
            completer_res_pers.setCompletionColumn(0)
            self.inputBoxResponsiblePerson.setCompleter(completer_res_pers)

            self.cbResPersFilter.clear()
            self.cbResPersFilter.setModel(self.res_pers_model)

            self.search()
            self.statusBar().showMessage("Deleted", 5000)

    def delete_location(self):
        count = self.db.count_location()
        DeleteDialog(1, self.db, self)
        if count > self.db.count_location():
            locations = self.db.get_location()
            self.loc_model = QStandardItemModel()

            for i, loc in enumerate(locations):
                self.loc_model.appendRow(QStandardItem(loc[1]))

            completer_loc = QCompleter(self.loc_model, self)
            completer_loc.setCaseSensitivity(Qt.CaseInsensitive)
            completer_loc.setCompletionRole(Qt.DisplayRole)
            completer_loc.setCompletionColumn(0)
            self.inputBoxLocation.setCompleter(completer_loc)

            self.cbLocFilter.clear()
            self.cbLocFilter.setModel(self.loc_model)

            self.search()
            self.statusBar().showMessage("Deleted", 5000)

    def delete_type(self):
        count = self.db.count_type()
        DeleteDialog(2, self.db, self)
        if count > self.db.count_type():
            model = QStandardItemModel()
            self.comboBoxTypes.clear()
            self.cbTypesFilter.clear()
            for elem in self.db.get_types():
                model.appendRow(QStandardItem(elem[1]))
            self.comboBoxTypes.setModel(model)
            self.cbTypesFilter.setModel(model)
            self.search()
            self.statusBar().showMessage("Deleted", 5000)

    def get_types(self):
        all_types = self.db.get_types()
        types = []
        for i in all_types:
            types.append(i[1])
        return types

    def __create_table(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        return table

    def search_input(self):
        if not self.inventoryMode:
            text = self.inpSearch.text().strip()
            if len(text) == 9:
                self.inpSearch.setText(text)
                if len(self.db.get_item_by_id(text)) >= 1:
                    self.search()
                    self.inpSearch.setText('')
                else:
                    res = re.match(r'SY(\d\d)(\d\d)\d\d\d', text)
                    year = int(res.group(1))
                    month = int(res.group(2))
                    if year <= int(str(datetime.now().timetuple().tm_year)[2:]) and month <= 12:
                        reply = QMessageBox.question(self, 'Message', 'Данного оборудования нету в базе данных.'
                                                                      '\nДобавить новое оборудование?',
                                                     QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            dialog = AddItemDialog(self.db, text)
                            dialog.exec()
                            self.inpSearch.setText('')
                            self.search()
        else:
            text = self.inpSearch.text().strip()
            if len(text) == 9:
                item = self.db.get_item_by_id(text)
                self.inpSearch.setText('')
                if len(item) > 0:
                    item = item[0]
                    if not item[0] in self.inventoryModeItemsID:
                        self.inventoryModeItemsID.append(item[0])
                        self.table.setRowCount(len(self.inventoryModeItemsID))
                        self.inpSearch.setText('')
                        self.insert_table(len(self.inventoryModeItemsID)-1, item)

    def search(self):
        items = []
        text = self.inpSearch.text()
        text = text.strip(' ')

        if text != '':
            while text[0] == '0':
                text = text[1:]

        type = self.db.get_type_id(self.cbTypesFilter.currentText())
        location = self.db.get_location_id(self.cbLocFilter.currentText())
        resPers = self.db.get_res_pers_id(self.cbResPersFilter.currentText())

        if type is None and location is None and resPers is None and text == '':
            items = self.db.get_items()
        else:
            if type is None:
                type = ''
            if location is None:
                location = ''
            if resPers is None:
                resPers = ''
            items = self.db.search_items(text, type, location, resPers)
        self.fill_table(items)

    def add_item(self):
        full_date = datetime.now().timetuple()
        if full_date.tm_mon < 10:
            date = str(full_date.tm_year)[2:] + '0' + str(full_date.tm_mon)
        else:
            date = str(full_date.tm_year)[2:] + str(full_date.tm_mon)

        id_item = "SY"+date
        text_characteristic = ''
        id = str(self.db.get_last_item_id(id_item)+1)
        while len(id) < 2:
            id = "0" + id
        id_item += id
        for i in range(len(self.inputsCharacteristic)):
            text_characteristic += self.labelCharacteristic[i].text() + ": " + self.inputsCharacteristic[
                i].text() + "\n"
        if self.db.get_res_pers_id(self.inputBoxResponsiblePerson.text().title()) is None:
            self.db.insert_res_pers(self.inputBoxResponsiblePerson.text().title())
            self.res_pers_model.appendRow(QStandardItem(self.inputBoxResponsiblePerson.text().title()))
        if self.db.get_location_id(self.inputBoxLocation.text().title()) is None:
            self.db.insert_location(self.inputBoxLocation.text().title())
            self.loc_model.appendRow(QStandardItem(self.inputBoxLocation.text().title()))
        item = {
            'id': id_item,
            'type': self.db.get_type_id(self.comboBoxTypes.currentText()),
            'characteristic': text_characteristic,
            'serial_number': self.inpSerialNumber.text(),
            'location': self.db.get_location_id(self.inputBoxLocation.text().title()),
            'responsible_person': self.db.get_res_pers_id(self.inputBoxResponsiblePerson.text().title())
        }
        self.db.insert_item(item)
        self.fill_table(self.db.get_items())

    def change_input(self):
        for elem in self.inputsCharacteristic:
            self.gridBox.removeWidget(elem)
        for elem in self.labelCharacteristic:
            self.gridBox.removeWidget(elem)
        self.inputsCharacteristic = []
        self.labelCharacteristic = []
        down = False
        type_id = self.db.get_type_id(self.comboBoxTypes.currentText())
        requiredCharacteristics = self.db.get_characteristics(type_id)
        if requiredCharacteristics is not None:
            requiredCharacteristics.sort(key=lambda k: k[1])
            for i, elem in enumerate(requiredCharacteristics):
                input = QLineEdit()
                label = QLabel(elem[1])
                if not down:
                    self.gridBox.addWidget(label, 0, 4 + i)
                    self.gridBox.addWidget(input, 0, 5 + i)
                    down = True
                else:
                    if not (len(requiredCharacteristics) % 2 == 0 and i == len(requiredCharacteristics) - 2):
                        self.gridBox.addWidget(label, 1, 3 + i)
                        self.gridBox.addWidget(input, 1, 4 + i)
                    else:
                        label.setAlignment(Qt.AlignCenter)
                        self.gridBox.addWidget(label, 1, 3 + i, 2, 1)
                        self.gridBox.addWidget(input, 1, 4 + i, 2, 1)
                    down = False
                self.labelCharacteristic.append(label)
                self.inputsCharacteristic.append(input)

    def table_header(self):
        self.table.setColumnCount(6)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Тип оборудования",
                "Характеристики",
                "Серийный номер",
                "Место расположение",
                "Ответственное лицо"
            ]
        )

    def fill_table(self, all_items):
        self.table.clear()
        self.table_header()

        self.comboBoxLocTabel = []
        self.comboBoxResPerTabel = []

        index = self.cbTypesFilter.currentIndex()
        id_type = self.db.get_type_id(self.cbTypesFilter.currentText())
        count = self.db.count_item_type(id_type)

        if index == 0 or count > len(all_items):
            self.table.setRowCount(len(all_items))
        else:
            self.table.setRowCount(count)
        for i, items in enumerate(all_items):
            self.insert_table(i, items)

    def insert_table(self, i, items):
        types = self.db.get_types()
        locations = self.db.get_location()
        responsible_persons = self.db.get_responsible_person()
        for j, item in enumerate(items):
            if j == 0:
                self.table.setItem(i, j, QTableWidgetItem(str(item)))
                self.table.item(i, j).setFlags(self.table.item(i, j).flags() & ~Qt.ItemIsEditable)
            elif j == 1:
                type = ''
                for elem in types:
                    if item == elem[0]:
                        type = elem[1]
                        break
                self.table.setItem(i, j, QTableWidgetItem(str(type)))
                self.table.item(i, j).setFlags(self.table.item(i, j).flags() & ~Qt.ItemIsEditable)
            elif j == 2:
                count = item.count('\n')
                if count > 0:
                    self.table.setRowHeight(i, 20 * count)
                self.table.setItem(i, j, QTableWidgetItem(str(item)))
            elif j == 4:
                comboBox = QComboBox()
                for k, loc in enumerate(locations):
                    comboBox.insertItem(k, loc[1])
                item = self.db.get_location_name(item)
                for elem in range(comboBox.count()):
                    if item == comboBox.itemText(elem):
                        comboBox.setCurrentIndex(elem)
                        break
                comboBox.setDisabled(not self.editMode)
                comboBox.currentIndexChanged.connect(self.update_row)
                self.comboBoxLocTabel.append(comboBox)
                self.table.setCellWidget(i, j, comboBox)
            elif j == 5:
                comboBox = QComboBox()
                for k, rp in enumerate(responsible_persons):
                    comboBox.insertItem(k, rp[1])
                item = self.db.get_res_pers_name(item)
                for elem in range(comboBox.count()):
                    if item == comboBox.itemText(elem):
                        comboBox.setCurrentIndex(elem)
                        break
                comboBox.setDisabled(not self.editMode)
                comboBox.currentIndexChanged.connect(self.update_row)
                self.comboBoxResPerTabel.append(comboBox)
                self.table.setCellWidget(i, j, comboBox)
            else:
                self.table.setItem(i, j, QTableWidgetItem(str(item)))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            row = self.table.currentRow()
            text = self.table.item(row, 0).text()
            reply = QMessageBox.question(self, 'Message', 'Точно удалить?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.delete_item(text)
                self.table.removeRow(row)
                self.statusBar().showMessage("Deleted", 3000)
        elif e.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.update_row()
        elif e.key() == Qt.Key_F5:
            self.fill_table(self.db.get_items())

    def update_row(self):
        row = self.table.currentRow()
        if row >= 0:
            item = {
                'id': self.table.item(row, 0).text(),
                'characteristic': self.table.item(row, 2).text(),
                'serial_number': self.table.item(row, 3).text(),
                'location': self.db.get_location_id(self.comboBoxLocTabel[row].currentText()),
                'responsible_person': self.db.get_res_pers_id(self.comboBoxResPerTabel[row].currentText())
            }
            self.db.update_item(item)
            self.statusBar().showMessage("Updated", 3000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
