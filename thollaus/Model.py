import requests

class Model:

    def __init__(self):
        self.reset()

    def reset(self):
        self.verkehrsmittel = None
        self.monat = None
        self.jahresausgabe = False

    def get_Jahresansicht_for_Verkehrsmittel(self, verkehrsmittel):
        url = f"http://localhost:5000/verkehr/{verkehrsmittel}"
        try:
            response = requests.get(url, timeout=5)
            # Prüft auf HTTP-Fehler (4xx, 5xx)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            return {"error": "Server nicht erreichbar", "details": "Der Endpoint unter localhost:5000 antwortet nicht."}

        except requests.exceptions.Timeout:
            return {"error": "Zeitüberschreitung", "details": "Die Anfrage hat zu lange gedauert."}

        except requests.exceptions.HTTPError as e:
            return {"error": "HTTP-Fehler", "status_code": e.response.status_code}

        except requests.exceptions.RequestException as e:
            # Fängt alle übrigen requests-Fehler ab
            return {"error": "Allgemeiner Fehler", "message": str(e)}


#    def put_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(self, verkehrsmittel, monat, Mitarbeiteranzahl):
#        url = f"http://localhost:5000/verkehr/{verkehrsmittel}/"
#        try:
#            response = requests.put(url, json={"monat": monat, "Mitarbeiteranzahl": Mitarbeiteranzahl}, timeout=5)
#            if response.status_code == 200:
#                return response.json()
#            else:
#                return "Fehler beim Aktualisieren der Daten"
#        except requests.RequestException as e:
#            return f"Fehler bei der Anfrage: {e}"
#
#    def patch_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(self, verkehrsmittel, monat, Mitarbeiteranzahl):
#        url = f"http://localhost:5000/verkehr/{verkehrsmittel}"


# ---Testcases ---
def test_Jahresansicht_for_Verkehrsmittel():
    model = Model()
    result = model.Jahresansicht_for_Verkehrsmittel("bus")
    assert isinstance(result, list), "Erwartet eine Liste von Daten"
    assert len(result) > 0, "Erwartet mindestens einen Eintrag in der Liste"
    assert "monat" in result[0] and "Mitarbeiteranzahl" in result[0], "Erwartet 'monat' und 'Mitarbeiteranzahl' in den Einträgen"
    print(result)
    print("passed")


def test_get_bekanntes_verkehrsmittel_gibt_liste_zurueck():
    model = Model()
    result = model.get_Jahresansicht_for_Verkehrsmittel("bus")
    assert isinstance(result, list), f"Erwartet eine Liste, bekam: {type(result)}"
    assert len(result) == 12, f"Erwartet 12 Monate, bekam: {len(result)}"
    assert all("monat" in eintrag for eintrag in result), "Jeder Eintrag muss 'monat' enthalten"
    print("test_get_bekanntes_verkehrsmittel_gibt_liste_zurueck passed")


def test_get_unbekanntes_verkehrsmittel_gibt_fehler_zurueck():
    model = Model()
    result = model.get_Jahresansicht_for_Verkehrsmittel("auto")
    assert isinstance(result, dict), "Erwartet ein Dict mit Fehler"
    assert "error" in result
    assert result["status_code"] == 404
    print("test_get_unbekanntes_verkehrsmittel_gibt_fehler_zurueck passed")


def test_get_alle_verkehrsmittel():
    model = Model()
    for vm in ["bus", "tram", "ubahn"]:
        result = model.get_Jahresansicht_for_Verkehrsmittel(vm)
        assert isinstance(result, list), f"Erwartet eine Liste für {vm}"
        assert len(result) == 12, f"Erwartet 12 Einträge für {vm}, bekam: {len(result)}"
        assert all("monat" in e for e in result), f"Jeder Eintrag von {vm} muss 'monat' enthalten"
    print("test_get_alle_verkehrsmittel passed")


if __name__ == '__main__':
    print("Running tests...")
    test_get_bekanntes_verkehrsmittel_gibt_liste_zurueck()
    test_get_unbekanntes_verkehrsmittel_gibt_fehler_zurueck()
    test_get_alle_verkehrsmittel()
