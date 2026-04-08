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

    def put_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(self, verkehrsmittel, monat, Mitarbeiteranzahl):
        url = f"http://localhost:5000/verkehr/{verkehrsmittel}/"
        try:
            response = requests.put(url, json={"monat": monat, "Mitarbeiteranzahl": Mitarbeiteranzahl}, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Server nicht erreichbar", "details": "Der Endpoint unter localhost:5000 antwortet nicht."}
        except requests.exceptions.Timeout:
            return {"error": "Zeitüberschreitung", "details": "Die Anfrage hat zu lange gedauert."}
        except requests.exceptions.HTTPError as e:
            return {"error": "HTTP-Fehler", "status_code": e.response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Allgemeiner Fehler", "message": str(e)}


    def patch_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(self, verkehrsmittel, monat, Mitarbeiteranzahl):
        url = f"http://localhost:5000/verkehr/{verkehrsmittel}"
        try:
            response = requests.patch(url, json={"monat": monat, "Mitarbeiteranzahl": Mitarbeiteranzahl}, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Server nicht erreichbar", "details": "Der Endpoint unter localhost:5000 antwortet nicht."}
        except requests.exceptions.Timeout:
            return {"error": "Zeitüberschreitung", "details": "Die Anfrage hat zu lange gedauert."}
        except requests.exceptions.HTTPError as e:
            return {"error": "HTTP-Fehler", "status_code": e.response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Allgemeiner Fehler", "message": str(e)}

    def post_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(self, verkehrsmittel, monat, Mitarbeiteranzahl):
        url = f"http://localhost:5000/verkehr/{verkehrsmittel}"
        try:
            response = requests.post(url, json={"monat": monat, "Mitarbeiteranzahl": Mitarbeiteranzahl}, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Server nicht erreichbar", "details": "Der Endpoint unter localhost:5000 antwortet nicht."}
        except requests.exceptions.Timeout:
            return {"error": "Zeitüberschreitung", "details": "Die Anfrage hat zu lange gedauert."}
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                return {"error": f"HTTP-Fehler {e.response.status_code}", "message": error_data.get("error", "Unbekannter Fehler")}
            except:
                return {"error": f"HTTP-Fehler {e.response.status_code}", "status_code": e.response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Allgemeiner Fehler", "message": str(e)}

    def delete_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(self, verkehrsmittel, monat):
        url = f"http://localhost:5000/verkehr/{verkehrsmittel}"
        try:
            response = requests.delete(url, json={"monat": monat}, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Server nicht erreichbar", "details": "Der Endpoint unter localhost:5000 antwortet nicht."}
        except requests.exceptions.Timeout:
            return {"error": "Zeitüberschreitung", "details": "Die Anfrage hat zu lange gedauert."}
        except requests.exceptions.HTTPError as e:
            return {"error": "HTTP-Fehler", "status_code": e.response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Allgemeiner Fehler", "message": str(e)}


    def format_to_html(self, data, verkehrsmittel="", monat=None):
        """Formatiert die Daten aus der API für HTML-Anzeige"""
        if "error" in data:
            return f"<b style='color:red;'>Fehler:</b> {data['error']}<br/>{data.get('details', data.get('message', ''))}"

        monate = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        
        if isinstance(data, list):
            # Einzelmonats-Anzeige
            if monat is not None:
                monat_name = monate[monat - 1] if 1 <= monat <= 12 else "Unbekannt"
                mitarbeiteranzahl = "kein Eintrag"
                print(data)
                for eintrag in data:
                    if eintrag.get("monat") == monat:
                        mitarbeiteranzahl = eintrag.get("Mitarbeiteranzahl", "kein Eintrag")
                        break
                
                return f"Für das Verkehrsmittel <b>{verkehrsmittel}</b> wurden folgende Mitarbeiterdaten erhoben:<br/><br/><b>{monat_name}:</b> {mitarbeiteranzahl} Beschäftigte"
            
            # Jahresansicht (alle Monate)
            text = f"Für das Verkehrsmittel <b>{verkehrsmittel}</b> wurden folgende Mitarbeiterdaten erhoben:<br/><br/>"
            
            for eintrag in data:
                monat_index = eintrag.get("monat", 0)
                if 1 <= monat_index <= 12:
                    monat_name = monate[monat_index - 1]
                    mitarbeiteranzahl = eintrag.get("Mitarbeiteranzahl", "kein Eintrag")
                    text += f"<b>{monat_name}:</b> {mitarbeiteranzahl} Beschäftigte<br/>"
            
            return text
        else:
            return f"<b>Unerwartetes Datenformat:</b> {str(data)}"


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


def test_format_to_html():
    model = Model()
    
    # Test mit gültigen Daten
    test_data = [
        {"monat": 1, "Mitarbeiteranzahl": 45},
        {"monat": 2, "Mitarbeiteranzahl": 50}
    ]
    result = model.format_to_html(test_data, "bus")
    assert "bus" in result, "Verkehrsmittel soll im Result stehen"
    assert "Jänner" in result, "Monatsname soll formatiert werden"
    assert "45 Beschäftigte" in result, "Mitarbeiteranzahl soll angezeigt werden"
    
    # Test mit Fehler-Daten
    error_data = {"error": "Test Fehler", "details": "Test Details"}
    result = model.format_to_html(error_data, "bus")
    assert "Fehler:" in result, "Fehler soll angezeigt werden"
    assert "Test Fehler" in result, "Fehlermeldung soll enthalten sein"
    
    print("test_format_to_html passed")


def test_crud_operations_without_server():
    """Testet die CRUD-Operationen ohne laufenden Server (erwartet Fehler)"""
    model = Model()
    
    # Alle sollten Server-Fehler zurückgeben
    put_result = model.put_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month("bus", 1, 100)
    assert "error" in put_result, "PUT sollte Fehler zurückgeben ohne Server"
    
    patch_result = model.patch_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month("bus", 1, 10)
    assert "error" in patch_result, "PATCH sollte Fehler zurückgeben ohne Server"
    
    post_result = model.post_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month("bus", 13, 50)
    assert "error" in post_result, "POST sollte Fehler zurückgeben ohne Server"
    
    delete_result = model.delete_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month("bus", 1)
    assert "error" in delete_result, "DELETE sollte Fehler zurückgeben ohne Server"
    
    print("test_crud_operations_without_server passed")


if __name__ == '__main__':
    print("Running tests...")
    test_get_bekanntes_verkehrsmittel_gibt_liste_zurueck()
    test_get_unbekanntes_verkehrsmittel_gibt_fehler_zurueck()
    test_get_alle_verkehrsmittel()
    test_format_to_html()
    test_crud_operations_without_server()
