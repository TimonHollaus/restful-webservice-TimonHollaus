from http import HTTPStatus
from traceback import format_list

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# Simulierte Datenbank
verkehr = {
    "bus": [
        {"monat": 1, "Mitarbeiteranzahl": 45},
        {"monat": 2, "Mitarbeiteranzahl": 45},
        {"monat": 3, "Mitarbeiteranzahl": 78},
        {"monat": 4, "Mitarbeiteranzahl": 56},
        {"monat": 5, "Mitarbeiteranzahl": 89},
        {"monat": 6, "Mitarbeiteranzahl": 34},
        {"monat": 7, "Mitarbeiteranzahl": 90},
        {"monat": 8, "Mitarbeiteranzahl": 23},
        {"monat": 9, "Mitarbeiteranzahl": 67},
        {"monat": 10, "Mitarbeiteranzahl": 45},
        {"monat": 11, "Mitarbeiteranzahl": 78},
        {"monat": 12, "Mitarbeiteranzahl": 56}
    ],
    "tram": [
        {"monat": 1, "Mitarbeiteranzahl": 45},
        {"monat": 2, "Mitarbeiteranzahl": 65},
        {"monat": 3, "Mitarbeiteranzahl": 78},
        {"monat": 4, "Mitarbeiteranzahl": 56},
        {"monat": 5, "Mitarbeiteranzahl": 89},
        {"monat": 6, "Mitarbeiteranzahl": 34},
        {"monat": 7, "Mitarbeiteranzahl": 90},
        {"monat": 8, "Mitarbeiteranzahl": 23},
        {"monat": 9, "Mitarbeiteranzahl": 67},
        {"monat": 10, "Mitarbeiteranzahl": 45},
        {"monat": 11, "Mitarbeiteranzahl": 78},
        {"monat": 12, "Mitarbeiteranzahl": 56}
    ],
    "ubahn": [
        {"monat": 1, "Mitarbeiteranzahl": 45},
        {"monat": 2, "Mitarbeiteranzahl": 65},
        {"monat": 3, "Mitarbeiteranzahl": 78},
        {"monat": 4, "Mitarbeiteranzahl": 56},
        {"monat": 5, "Mitarbeiteranzahl": 89},
        {"monat": 6, "Mitarbeiteranzahl": 34},
        {"monat": 7, "Mitarbeiteranzahl": 90},
        {"monat": 8, "Mitarbeiteranzahl": 23},
        {"monat": 9, "Mitarbeiteranzahl": 67},
        {"monat": 10, "Mitarbeiteranzahl": 45},
        {"monat": 11, "Mitarbeiteranzahl": 78},
        {"monat": 12, "Mitarbeiteranzahl": 56}
    ]
}



@app.route('/verkehr/<string:verkehrsmittel>', methods=['GET'])
def get_Jahresansicht_for_Verkehrsmittel(verkehrsmittel):
    if verkehrsmittel in verkehr:
        return make_response(jsonify(verkehr[verkehrsmittel]), HTTPStatus.OK)
    else:
        return make_response(jsonify({"error": "Verkehrsmittel nicht gefunden"}), HTTPStatus.NOT_FOUND)


@app.route('/verkehr/<string:verkehrsmittel>/', methods=['PUT'])
def set_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel):
    if verkehrsmittel not in verkehr:
        return make_response(jsonify({"error": "Verkehrsmittel nicht gefunden"}), HTTPStatus.NOT_FOUND)

    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Kein Json Body empfangen"}), HTTPStatus.BAD_REQUEST)

    mitarbeiteranzahl = data.get("Mitarbeiteranzahl")
    monat = data.get("monat")

    for eintrag in verkehr[verkehrsmittel]:
        if eintrag["monat"] == monat:
            eintrag["Mitarbeiteranzahl"] = mitarbeiteranzahl
            return make_response(jsonify({"message": "Mitarbeiteranzahl aktualisiert"}), HTTPStatus.OK)

    return make_response(jsonify({"error": "Monat im Datensatz nicht vorhanden"}), HTTPStatus.NOT_FOUND)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
