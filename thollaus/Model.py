import requests

class Model:

    def __init__(self):
        self.reset()

    def reset(self):
        self.verkehrsmittel = None
        self.monat = None
        self.jahresausgabe = False

    def Jahresansicht_for_Verkehrsmittel(self, verkehrsmittel):
        url = f"http://localhost:5000/verkehr/{verkehrsmittel}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return "keine Daten gefunden"
        except requests.RequestException as e:
            return f"Fehler bei der Anfrage: {e}"

    def put_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(self, verkehrsmittel, monat, Mitarbeiteranzahl):
        url = f"http://localhost:5000/verkehr/{verkehrsmittel}"
        try:
            response = requests.put(url, json={"monat": monat, "Mitarbeiteranzahl": Mitarbeiteranzahl}, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return "Fehler beim Aktualisieren der Daten"
        except requests.RequestException as e:
            return f"Fehler bei der Anfrage: {e}"




# ---Testcases ---
def test_Jahresansicht_for_Verkehrsmittel():
    model = Model()
    result = model.Jahresansicht_for_Verkehrsmittel("bus")
    assert isinstance(result, list), "Erwartet eine Liste von Daten"
    assert len(result) > 0, "Erwartet mindestens einen Eintrag in der Liste"
    assert "monat" in result[0] and "Mitarbeiteranzahl" in result[0], "Erwartet 'monat' und 'Mitarbeiteranzahl' in den Einträgen"
    print(result)
    print("passed")



if __name__ == '__main__':
    print("Running tests...")
    test_Jahresansicht_for_Verkehrsmittel()
