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
            # Zeige alle Monate an (Jahresansicht)
            formatted_text = self.model.format_to_html(data, current_Verkehrsmittel)
        else:
            # Zeige nur einen spezifischen Monat an
            monat_index = self.view.get_Monat_tab1()
            formatted_text = self.model.format_to_html(data, current_Verkehrsmittel, monat=monat_index)

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

        """ Error handling """
        if result:
            if "error" in result:
                error_msg = result.get('error', 'Unbekannter Fehler')
                details = result.get('details', result.get('message', ''))
                if details:
                    formatted_text = f"<b style='color:red;'>Fehler:</b> {error_msg}<br/><b>Details:</b> {details}"
                else:
                    formatted_text = f"<b style='color:red;'>Fehler:</b> {error_msg}"
            elif "message" in result:
                formatted_text = f"<b style='color:green;'>Erfolg:</b> {result['message']}"
            else:
                formatted_text = f"<b>Antwort:</b> {str(result)}"
        else:
            formatted_text = "<b style='color:red;'>Keine Antwort erhalten</b>"
            
        self.view.set_Result_for_verkehrsmittel(verkehrsmittel, formatted_text)
        
        # StatusBar-Information hinzufügen
        if "error" in result:
            self.view.set_status(f"Fehler bei {aktion} für {verkehrsmittel}")
        else:
            self.view.set_status(f"{aktion} für {verkehrsmittel}, Monat {monat} erfolgreich")


    def reset(self):
        self.view.reset_inputs()
        self.model.reset()

    def exit(self):
        self.view.close()
