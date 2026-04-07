from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('.\GUI.ui', self)
        
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

    # Tab 2 Methods
    def get_Verkehrsmittel_tab2(self):
        return self.comboBox_Aktion_fuer.currentText()
    
    def get_Aktion_tab2(self):
        return self.comboBox_Aktion.currentText()
    
    def get_Monat_tab2(self):
        return self.spinBox_monat_tab2.value()
    
    def get_Mitarbeiteranzahl_tab2(self):
        return self.spinBox.value()
    
    def set_Result_tab2(self, message):
        # Finde den verfügbaren TextBrowser für Tab2
        for name in ['textBrowser_tab2', 'textBrowser_tab2_1', 'textBrowser_admin', 'textBrowser']:
            if hasattr(self, name):
                getattr(self, name).setHtml(message)
                self.set_status("Anzeige aktualisiert")
                return
        print("Kein TextBrowser für Tab2 gefunden!")

    # Neue Methoden für 3 separate TextBrowser
    def set_Result_bus(self, message):
        # Versuche verschiedene mögliche Namen für Bus TextBrowser
        for name in ['textBrowser_bus', 'textBrowser_tab2_1']:
            if hasattr(self, name):
                getattr(self, name).setHtml(message)
                return True
        return False

    def set_Result_tram(self, message):
        # Versuche verschiedene mögliche Namen für Tram TextBrowser
        for name in ['textBrowser_tram', 'textBrowser_tab2_2']:
            if hasattr(self, name):
                getattr(self, name).setHtml(message)
                return True
        return False

    def set_Result_ubahn(self, message):
        # Versuche verschiedene mögliche Namen für U-Bahn TextBrowser
        for name in ['textBrowser_ubahn', 'textBrowser_tab2_3']:
            if hasattr(self, name):
                getattr(self, name).setHtml(message)  
                return True
        return False

    def clear_all_results_tab2(self):
        """Löscht alle TextBrowser im Admin-Dashboard"""
        cleared = []
        for name in ['textBrowser_tab2', 'textBrowser_tab2_1', 'textBrowser_tab2_2', 'textBrowser_tab2_3', 
                     'textBrowser_bus', 'textBrowser_tram', 'textBrowser_ubahn']:
            if hasattr(self, name):
                getattr(self, name).clear()
                cleared.append(name)
        return cleared

    def set_all_verkehrsmittel_results(self, bus_text, tram_text, ubahn_text):
        """Setzt alle 3 Verkehrsmittel-Ergebnisse gleichzeitig"""
        success = []
        
        # Versuche die separaten TextBrowser zu verwenden
        if self.set_Result_bus(bus_text):
            success.append("Bus")
        if self.set_Result_tram(tram_text):
            success.append("Tram")  
        if self.set_Result_ubahn(ubahn_text):
            success.append("U-Bahn")
            
        # Falls separate TextBrowser nicht verfügbar sind, kombiniere in einem
        if not success:
            combined_text = f"""
            <div style='display: flex; justify-content: space-around;'>
                <div style='flex: 1; margin: 10px; padding: 10px; border: 1px solid #ccc;'>
                    <h3 style='text-align: center; color: #4a90e2;'>🚌 Bus</h3>
                    {bus_text}
                </div>
                <div style='flex: 1; margin: 10px; padding: 10px; border: 1px solid #ccc;'>
                    <h3 style='text-align: center; color: #4a90e2;'>🚊 Tram</h3>
                    {tram_text}
                </div>
                <div style='flex: 1; margin: 10px; padding: 10px; border: 1px solid #ccc;'>
                    <h3 style='text-align: center; color: #4a90e2;'>🚇 U-Bahn</h3>
                    {ubahn_text}
                </div>
            </div>
            """
            self.set_Result_tab2(combined_text)
            success = ["Kombiniert"]
            
        return success


