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
        self.view.pushButton_start_tab2.clicked.connect(self.start)
        self.view.pushButton_reset_tab2.clicked.connect(self.reset)
        self.view.pushButton_exit_tab2.clicked.connect(self.exit)



    def start(self):
        current_Verkehrsmittel = self.view.get_Verkehrsmittel_tab1()
        
        data = self.model.get_Jahresansicht_for_Verkehrsmittel(current_Verkehrsmittel)

        if self.view.get_Jahresansicht_tab1():
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

        self.view.set_Result(formatted_text)


    def reset(self):
        self.view.reset_inputs()
        self.model.reset()

    def exit(self):
        self.view.close()
