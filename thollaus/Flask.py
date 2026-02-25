from http import HTTPStatus

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
        {"monat": 5, "Mitarbeiteranzahl": 11},
        {"monat": 6, "Mitarbeiteranzahl": 14},
        {"monat": 7, "Mitarbeiteranzahl": 90},
        {"monat": 8, "Mitarbeiteranzahl": 23},
        {"monat": 9, "Mitarbeiteranzahl": 46},
        {"monat": 10, "Mitarbeiteranzahl": 98},
        {"monat": 11, "Mitarbeiteranzahl": 34},
        {"monat": 12, "Mitarbeiteranzahl": 57}
    ],
    "ubahn": [
        {"monat": 1, "Mitarbeiteranzahl": 41},
        {"monat": 2, "Mitarbeiteranzahl": 42},
        {"monat": 3, "Mitarbeiteranzahl": 48},
        {"monat": 4, "Mitarbeiteranzahl": 98},
        {"monat": 5, "Mitarbeiteranzahl": 37},
        {"monat": 6, "Mitarbeiteranzahl": 87},
        {"monat": 7, "Mitarbeiteranzahl": 94},
        {"monat": 8, "Mitarbeiteranzahl": 27},
        {"monat": 9, "Mitarbeiteranzahl": 85},
        {"monat": 10, "Mitarbeiteranzahl": 74},
        {"monat": 11, "Mitarbeiteranzahl": 84}
    ]
}



@app.route('/verkehr/<string:verkehrsmittel>', methods=['GET'])
def get_Jahresansicht_for_Verkehrsmittel(verkehrsmittel):
    if verkehrsmittel in verkehr:
        return make_response(jsonify(verkehr[verkehrsmittel]), HTTPStatus.OK)
    else:
        return make_response(jsonify({"error": "Verkehrsmittel nicht gefunden"}), HTTPStatus.NOT_FOUND)


@app.route('/verkehr/<string:verkehrsmittel>/', methods=['PUT'])
def put_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel):
    if verkehrsmittel not in verkehr:
        return make_response(jsonify({"error": "Verkehrsmittel nicht gefunden"}), HTTPStatus.NOT_FOUND)

    try:
        data = request.get_json()

        monat = data.get("monat")
        mitarbeiteranzahl = data.get("Mitarbeiteranzahl")
    except:
        return make_response(jsonify({"error": "Ungültige Eingabe"}), HTTPStatus.BAD_REQUEST)

    for eintrag in verkehr[verkehrsmittel]:
        if eintrag["monat"] == monat:
            eintrag["Mitarbeiteranzahl"] = mitarbeiteranzahl
            return make_response(jsonify({"message": "Mitarbeiteranzahl aktualisiert"}), HTTPStatus.OK)

    return make_response(jsonify({"error": "Monat im Datensatz nicht vorhanden"}), HTTPStatus.NOT_FOUND)

@app.route('/verkehr/<string:verkehrsmittel>', methods=['PATCH'])
def patch_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel):

    try:
        data = request.get_json()

        monat = data.get("monat")
        mitarbeiteranzahl = data.get("Mitarbeiteranzahl")
    except:
        return make_response(jsonify({"error": "Ungültige Eingabe"}), HTTPStatus.BAD_REQUEST)

    if not (1 <= monat <= 12) or not (-250 <= mitarbeiteranzahl <= 250):
        return make_response(jsonify({"error": "Ungültige Eingabe"}), HTTPStatus.BAD_REQUEST)

    for eintrag in verkehr[verkehrsmittel]:
        if eintrag["monat"] == monat:
            eintrag["Mitarbeiteranzahl"] += mitarbeiteranzahl
            return make_response(jsonify({"message": "Erfolgfreich erhöht"}), HTTPStatus.OK)

    return make_response(jsonify({"error": "Verkehrsmittel oder Monat nicht gefunden"}), HTTPStatus.NOT_FOUND)

@app.route('/verkehr/<string:verkehrsmittel>', methods=['POST'])
def post_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel):

    try:
        data = request.get_json()
        monat = data.get("monat")
        mitarbeiteranzahl = data.get("Mitarbeiteranzahl")
    except:
        return make_response(jsonify({"error": "Ungültige Eingabe"}), HTTPStatus.BAD_REQUEST)

    if not (1 <= monat <= 12) or not (0 <= mitarbeiteranzahl <= 250):
        return make_response(jsonify({"error": "Ungültige Eingabe"}), HTTPStatus.BAD_REQUEST)

    if verkehrsmittel not in verkehr:
        return make_response(jsonify({"error": "Verkehrsmittel nicht gefunden"}), HTTPStatus.NOT_FOUND)

    for eintrag in verkehr[verkehrsmittel]:
        if eintrag["monat"] == monat:
            return make_response(jsonify({"error": "Monat bereits vorhanden"}), HTTPStatus.CONFLICT)

    neuer_eintrag = {"monat": monat, "Mitarbeiteranzahl": mitarbeiteranzahl}
    verkehr[verkehrsmittel].append(neuer_eintrag)
    return make_response(jsonify({"message": "Erfolgreich angelegt"}), HTTPStatus.CREATED)

@app.route('/verkehr/<string:verkehrsmittel>', methods=['DELETE'])
def delete_Mitarbeiteranzahl_for_Verkehrsmittel_AND_Month(verkehrsmittel):
    try:
        data = request.get_json()
        monat = data.get("monat")
    except:
        return make_response(jsonify({"error": "Ungültige Eingabe"}), HTTPStatus.BAD_REQUEST)

    if not (1 <= monat <= 12):
        return make_response(jsonify({"error": "Ungültige Eingabe"}), HTTPStatus.BAD_REQUEST)


    for eintrag in verkehr[verkehrsmittel]:
        if eintrag["monat"] == monat:
            del eintrag["Mitarbeiteranzahl"]
            return make_response(jsonify({"message": "Erfolgreich gelöscht"}), HTTPStatus.NO_CONTENT)

    if verkehrsmittel not in verkehr:
        return make_response(jsonify({"error": "Verkehrsmittel oder Monat nicht gefunden"}), HTTPStatus.NOT_FOUND)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
