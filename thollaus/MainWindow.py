from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('.\GUI.ui', self)
        # Tab 1
        self.comboBox_Verkehrsmittel_tab1.addItems(["bus", "ubahn", "tram"])
        self.spinBox_monat_tab1.setRange(1, 12)
        self.spinBox_monat_tab1.setValue(1)

        # Tab2
        self.comboBox_Aktion_fuer.addItems(["bus", "ubahn", "tram"])
        self.comboBox_Aktion.addItems(["PUT", "PATCH", "POST", "DELETE"])
        self.spinBox_monat_tab2.setRange(1, 12)
        self.spinBox_monat_tab2.setValue(1)


    def get_Verkehrsmittel(self):
        return self.comboBox_Verkehrsmittel.currentText()

    def get_Monat(self):
        return self.spinBox_monat.value()

    def get_Jahresansicht(self):
        return self.checkBox_jahresansicht.isChecked()

    def set_Result(self, message):
        self.textBrowser.setText(message)
        self.set_status("Anzeige aktualisiert")

    def set_status(self, message):
        """Setzt die Statusbar-Nachricht"""
        self.statusbar.showMessage(message)


    def reset_inputs(self):
        """Setzt alle Eingabefelder zurück"""
        self.comboBox_Verkehrsmittel.setCurrentIndex(0)
        self.spinBox_monat.setValue(1)
        self.checkBox_jahresansicht.setChecked(False)
        self.textBrowser.clear()
        self.set_status("Eingaben zurückgesetzt")



