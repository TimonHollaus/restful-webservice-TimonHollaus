import json


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Tab1
        self.view.pushButton_start_tab1.clicked.connect(self.start)
        self.view.pushButton_reset_tab1.clicked.connect(self.reset)
        self.view.pushButton_exit_tab1.clicked.connect(self.exit)


        # Tab2
        self.view.pushButton_start_tab2.clicked.connect(self.start_tab2)
        self.view.pushButton_reset_tab2.clicked.connect(self.reset)
        self.view.pushButton_exit_tab2.clicked.connect(self.exit)



    def start(self):
        current_Verkehrsmittel = self.view.get_Verkehrsmittel_tab1()
        
        data = self.model.get_Jahresansicht_for_Verkehrsmittel(current_Verkehrsmittel)

        if self.view.get_Jahresansicht():
            # Zeige alle Monate an
            formatted_text = self.model.format_to_html(data, current_Verkehrsmittel)
        else:
            # Zeige nur einen spezifischen Monat an
            monat_index = self.view.get_Monat_tab1()
            monate = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
            
            if isinstance(data, dict) and "error" in data:
                formatted_text = self.model.format_to_html(data, current_Verkehrsmittel)
            elif isinstance(data, list):
                monat_name = monate[monat_index - 1]
                mitarbeiteranzahl = "kein Eintrag"
                
                for eintrag in data:
                    if eintrag["monat"] == monat_index:
                        mitarbeiteranzahl = eintrag["Mitarbeiteranzahl"]
                        break
                
                formatted_text = f"Für das Verkehrsmittel <b>{current_Verkehrsmittel}</b> wurden folgende Mitarbeiterdaten erhoben:<br/><br/><b>{monat_name}:</b> {mitarbeiteranzahl} Beschäftigte"
            else:
                formatted_text = self.model.format_to_html(data, current_Verkehrsmittel)

        self.view.set_Result_tab1(formatted_text)
        self.view.set_status(f"Daten für {current_Verkehrsmittel} abgerufen")

    def start_tab2(self):
        verkehrsmittel = self.view.get_Verkehrsmittel_tab2()
        aktion = self.view.get_Aktion_tab2()
        monat = self.view.get_Monat_tab2()
        mitarbeiteranzahl = self.view.get_Mitarbeiteranzahl_tab2()
        
        # Für Jahresansicht: Alle 3 Verkehrsmittel in separaten TextBrowser anzeigen
        if aktion == "Jahresansicht":
            self.view.clear_all_results_tab2()
            
            # Daten für alle 3 Verkehrsmittel abrufen
            bus_data = self.model.get_Jahresansicht_for_Verkehrsmittel("bus")
            tram_data = self.model.get_Jahresansicht_for_Verkehrsmittel("tram")
            ubahn_data = self.model.get_Jahresansicht_for_Verkehrsmittel("ubahn")
            
            # HTML für jedes Verkehrsmittel erstellen
            bus_html = self.model.format_to_html(bus_data, "bus")
            tram_html = self.model.format_to_html(tram_data, "tram")
            ubahn_html = self.model.format_to_html(ubahn_data, "ubahn")
            
            # Alle 3 TextBrowser setzen
            success = self.view.set_all_verkehrsmittel_results(bus_html, tram_html, ubahn_html)
            
            self.view.set_status(f"Jahresübersicht geladen für: {', '.join(success)}")
            return
        
        # Standard CRUD-Operationen
        result = None
        
        if aktion == "PUT":
            result = self.model.put_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel, monat, mitarbeiteranzahl)
        elif aktion == "PATCH":
            result = self.model.patch_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel, monat, mitarbeiteranzahl)
        elif aktion == "POST":
            result = self.model.post_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel, monat, mitarbeiteranzahl)
        elif aktion == "DELETE":
            result = self.model.delete_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel, monat)
        else:
            result = {"error": f"Unbekannte Aktion '{aktion}'"}
        
        if result:
            if "error" in result:
                formatted_text = f"<b style='color:red;'>Fehler:</b> {result.get('error', 'Unbekannter Fehler')}<br/>{result.get('details', result.get('message', ''))}"
            elif "message" in result:
                formatted_text = f"<b style='color:green;'>Erfolg:</b> {result['message']}"
            else:
                formatted_text = f"<b>Antwort:</b> {str(result)}"
        else:
            formatted_text = "<b style='color:red;'>Keine Antwort erhalten</b>"
            
        self.view.set_Result_tab2(formatted_text)
        
        # StatusBar-Information hinzufügen
        if "error" in result:
            self.view.set_status(f"Fehler bei {aktion} für {verkehrsmittel}")
        else:
            self.view.set_status(f"{aktion} für {verkehrsmittel}, Monat {monat} erfolgreich")
    
    def format_all_verkehrsmittel_overview(self, all_data):
        """Formatiert Übersicht aller 3 Verkehrsmittel"""
        html = "<h2 style='text-align: center; color: #2c5282;'>Jahresübersicht aller Verkehrsmittel</h2>"
        html += "<div style='display: flex; justify-content: space-around;'>"
        
        verkehrsmittel_namen = {"bus": "🚌 Bus", "tram": "🚊 Tram", "ubahn": "🚇 U-Bahn"}
        monate = ["Jän", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        
        for vm, data in all_data.items():
            html += f"<div style='margin: 10px; padding: 15px; border: 2px solid #4a90e2; border-radius: 8px;'>"
            html += f"<h3 style='text-align: center; color: #4a90e2; margin-bottom: 15px;'>{verkehrsmittel_namen[vm]}</h3>"
            
            if isinstance(data, dict) and "error" in data:
                html += f"<p style='color: red;'>❌ Fehler: {data['error']}</p>"
            elif isinstance(data, list):
                html += "<table style='width: 100%; border-collapse: collapse;'>"
                for eintrag in data:
                    monat_idx = eintrag.get("monat", 0) - 1
                    if 0 <= monat_idx < 12:
                        monat_name = monate[monat_idx]
                        anzahl = eintrag.get("Mitarbeiteranzahl", "N/A")
                        html += f"<tr><td style='padding: 3px; border-bottom: 1px solid #ddd;'><b>{monat_name}:</b></td><td style='padding: 3px; text-align: right;'>{anzahl}</td></tr>"
                html += "</table>"
            else:
                html += f"<p style='color: orange;'>⚠️ Unbekanntes Datenformat</p>"
            
            html += "</div>"
        
        html += "</div>"
        return html


    def reset(self):
        self.view.reset_inputs()
        self.model.reset()

    def exit(self):
        self.view.close()
