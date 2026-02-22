import json


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.pushButton_start.clicked.connect(self.start)
        self.view.pushButton_reset.clicked.connect(self.reset)
        self.view.pushButton_exit.clicked.connect(self.exit)


    def start(self):
        current_Verkehrsmittel = self.view.get_Verkehrsmittel()
        monate = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

        text = "Für das Verkehrsmittel " + current_Verkehrsmittel + " wurden folgende Mitarbeiterdaten erhoben: \n"

        data  = self.model.get_Jahresansicht_for_Verkehrsmittel(current_Verkehrsmittel)
        if self.view.get_Jahresansicht():
            #json_string = json.dumps(data, indent=2, sort_keys=True)
            for eintrag in data:
                monat_name = monate[eintrag["monat"] - 1]
                mitarbeiteranzahl = eintrag["Mitarbeiteranzahl"]
                text += monat_name + ": " + str(mitarbeiteranzahl) + " Beschäftigte\n"
        else:
            monat_index = self.view.get_Monat()
            monat_name = monate[monat_index -1]
            for eintrag in data:
                if eintrag["monat"] == monat_index:
                    mitarbeiteranzahl = eintrag["Mitarbeiteranzahl"]
            text += monat_name + ": " + str(mitarbeiteranzahl) + " Beschäftigte"

        self.view.set_Result(text)


    def reset(self):
        self.view.reset_inputs()
        self.model.reset()

    def exit(self):
        self.view.close()
