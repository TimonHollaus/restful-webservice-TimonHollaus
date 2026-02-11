from PyQt6.QtWidgets import QMainWindow,
from PyQt6 import uic


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)

        self.comboBox_2.addItems(["Ubahn", "Bus", "Straßenban", "SBahn"])
        self.spinBox.setRange(1, 12)
        self.spinBox.setValue(1)


    def get_verkehrsmittel(self):
        return self.comboBox_2.currentText()

    def get_monat(self):
        return self.spinBox.value()

    def  get_Jahresausgabe(self):
        return self.checkBox.isChecked()

    def set_text(self, message):
        self.textBrowser.setText(message)

    def set_status(self, message):
        """Setzt die Statusbar-Nachricht"""
        self.statusbar.showMessage(message)


    def clear_inputs(self):
        """Setzt alle Eingabefelder zurück"""
        self.setValue(0.0)
        self.comboBox_2.clear()
        self.spinbox.clear()
        self.statusbar.clearMessage()