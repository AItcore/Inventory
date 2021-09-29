from datetime import datetime
import threading

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QGridLayout, QLineEdit, QMessageBox

from labelPrint import printLabel


class PrintDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление оборудования")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()

        self.labelInfo = QLabel("Введите с какого по какой номер распечатать")

        self.labelFrom = QLabel("С")
        self.inpFrom = QLineEdit()
        self.inpFrom.textChanged.connect(self.change_input)

        self.labelTo = QLabel("По")
        self.inpTo = QLineEdit()
        self.inpTo.textChanged.connect(self.change_input)

        self.layout.addWidget(self.labelInfo, 0, 0, 1, 2)
        self.layout.addWidget(self.labelFrom, 1, 0)
        self.layout.addWidget(self.inpFrom, 1, 1)
        self.layout.addWidget(self.labelTo, 2, 0)
        self.layout.addWidget(self.inpTo, 2, 1)

        self.layout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.setLayout(self.layout)

    def change_input(self, text):
        if len(text) > 3:
            self.inpTo.setText(self.inpTo.text()[:3])
            self.inpFrom.setText(self.inpFrom.text()[:3])

    def printing(self, start, end):
        date = datetime.now().timetuple()
        self.thread = threading.Thread(target=printLabel, args=(date.tm_year, date.tm_mon, start, end))
        self.thread.start()
        self.hide()

    def accept(self):
        start = int(self.inpFrom.text())
        end = int(self.inpTo.text())
        if start <= end:
            if end-start > 30:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Предупреждение')
                dlg.setText('Будет распечатано более 30 этикеток.\nВы уверены?')
                dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dlg.setDefaultButton(QMessageBox.No)
                dlg.setIcon(QMessageBox.Warning)
                res = dlg.exec()
                if res == QMessageBox.Yes:
                    self.printing(start, end)
            else:
                self.printing(start, end)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Неверные данные")
            dlg.setText("Введите корректные данные")
            dlg.exec()

    def reject(self):
        self.hide()
