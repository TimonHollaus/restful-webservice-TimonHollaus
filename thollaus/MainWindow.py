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


    def get_Verkehrsmittel_tab1(self):
        return self.comboBox_Verkehrsmittel_tab1.currentText()

    def get_Monat_tab1(self):
        return self.spinBox_monat_tab1.value()

    def get_Jahresansicht(self):
        return self.checkBox_jahresansicht_tab1.isChecked()

    def set_Result_tab1(self, message):
        self.textBrowser_tab1.setText(message)
        self.set_status("Anzeige aktualisiert")

    def set_status(self, message):
        """Setzt die Statusbar-Nachricht"""
        self.statusbar.showMessage(message)


    def reset_inputs(self):
        """Setzt alle Eingabefelder zurück"""
        self.comboBox_Verkehrsmittel_tab1.setCurrentIndex(0)
        self.spinBox_monat_tab1.setValue(1)
        self.spinBox_monat_tab2.setValue(1)
        self.checkBox_jahresansicht_tab1.setChecked(False)
        self.textBrowser_tab1.clear()
        self.textBrowser_tab2.clear()
        self.set_status("Eingaben zurückgesetzt")



