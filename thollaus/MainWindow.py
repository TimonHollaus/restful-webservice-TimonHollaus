from PyQt6.QtWidgets import *
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./GUI.ui', self)
        
        # Sinnvoller Window-Titel setzen
        self.setWindowTitle("Wiener Verkehrsbetriebe - Mitarbeiter Management")
        
        # Tab 1
        self.comboBox_Verkehrsmittel_tab1.addItems(["bus", "ubahn", "tram"])
        self.spinBox_monat_tab1.setRange(1, 12)
        self.spinBox_monat_tab1.setValue(1)

        # Tab2
        self.comboBox_Aktion_fuer.addItems(["bus", "ubahn", "tram"])
        self.comboBox_Aktion.addItems(["Jahresansicht", "PUT", "PATCH", "POST", "DELETE"])
        self.spinBox_monat_tab2.setRange(1, 12)
        self.spinBox_monat_tab2.setValue(1)
        self.spinBox.setRange(-250, 250)
        self.spinBox.setValue(0)
        self.set_status("Noch keien Abfrage durchgeführt")


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
        # Tab 1 Reset
        self.comboBox_Verkehrsmittel_tab1.setCurrentIndex(0)
        self.spinBox_monat_tab1.setValue(1)
        self.checkBox_jahresansicht_tab1.setChecked(False)
        self.textBrowser_tab1.clear()
        
        # Tab 2 Reset
        self.comboBox_Aktion_fuer.setCurrentIndex(0)
        self.comboBox_Aktion.setCurrentIndex(0)
        self.spinBox_monat_tab2.setValue(1)
        self.spinBox.setValue(0)

        self.clear_all_results_tab2()

        self.set_status("Eingaben zurückgesetzt")

    # Tab 2 Methods
    def get_Verkehrsmittel_tab2(self):
        return self.comboBox_Aktion_fuer.currentText()
    
    def get_Aktion_tab2(self):
        return self.comboBox_Aktion.currentText()
    
    def get_Monat_tab2(self):
        return self.spinBox_monat_tab2.value()
    
    def get_Mitarbeiteranzahl_tab2(self):
        return self.spinBox.value()

    # Neue Methoden für 3 separate TextBrowser
    def set_Result_bus(self, message):
        self.textBrowser_tab2_1.setHtml(message)
        return True

    def set_Result_tram(self, message):
        self.textBrowser_tab2_2.setHtml(message)
        return True

    def set_Result_ubahn(self, message):
        self.textBrowser_tab2_3.setHtml(message)
        return True


    def set_Result_for_verkehrsmittel(self, verkehrsmittel, message):
        """Setzt das Ergebnis im passenden TextBrowser für das Verkehrsmittel"""
        if verkehrsmittel.lower() == "bus":
            success = self.set_Result_bus(message)
        elif verkehrsmittel.lower() == "tram":
            success = self.set_Result_tram(message)
        elif verkehrsmittel.lower() == "ubahn":
            success = self.set_Result_ubahn(message)
        else:
            success = False

        self.set_status("Anzeige aktualisiert")
        return success

    def clear_all_results_tab2(self):

        """Löscht alle TextBrowser im Admin-Dashboard"""
        self.textBrowser_tab2_1.clear()
        self.textBrowser_tab2_2.clear()
        self.textBrowser_tab2_3.clear()

    def set_all_verkehrsmittel_results(self, bus_text, tram_text, ubahn_text):
        """Setzt alle 3 Verkehrsmittel-Ergebnisse gleichzeitig"""
        success = []
        
        # Setze alle Werte in die TextBrowser
        if self.set_Result_bus(bus_text):
            success.append("Bus")
        if self.set_Result_tram(tram_text):
            success.append("Tram")  
        if self.set_Result_ubahn(ubahn_text):
            success.append("U-Bahn")
            
        return success


