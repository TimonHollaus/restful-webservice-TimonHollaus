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
        result = "Für das Verkehrsmittel " + current_Verkehrsmittel + " wurden folgende Mitarbeiterdaten erhoben: \n"
        result += self.model.Jahresansicht_for_Verkehrsmittel(current_Verkehrsmittel)

        json_string = json.dumps(result, indent=2, sort_keys=True)
        self.view.set_Result(json_string)


        #self.view.set_Result(current_Verkehrsmittel)

        #if(self.view.get_Jahresansicht):
        #        result = self.model.Jahresansicht_for_Verkehrsmittel(current_Verkehrsmittel)
        #        self.view.set_Result(result)
        #else:
        #    self.view.set_Result("ist nicht angehakt")

    def reset(self):
        self.view.reset_inputs()
        self.model.reset()

    def exit(self):
        self.view.close()
