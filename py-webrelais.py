__author__ = 'schinken'

from helpers import check_permission, auth_required, relais_result
from flask import Flask, render_template, jsonify
from relais import SainSmart, Relais, RelaisProxy
from settings import relais_cards

app = Flask(__name__)

relais_proxy = RelaisProxy()

for entry in relais_cards:
    print entry
    sainsmart = SainSmart(entry['serial'])
    wrapper = Relais(sainsmart)
    relais_proxy.add_relais(entry['start'], entry['relais'], wrapper)

@app.route("/")
def page_main():
    return render_template('index.html')


@app.route("/relais", methods=["GET"])
@app.route("/relais/<int:relais>", methods=["GET"])
def get_relais(relais=None):

    if relais is None:
        response = []
        for pin, status in enumerate(relais_proxy.get_pins()):
            response.append(relais_result(pin, status))
    else:
        response = relais_result(relais, relais_proxy.get_pin(relais))

    return jsonify(payload=response)

@app.route("/relais/<int:relais>", methods=["POST"])
def set_relais(relais):

    if check_permission(relais):
        relais_proxy.set_pin(relais, True)
    else:
        return auth_required()

    return jsonify(payload=relais_result(relais, True))

@app.route("/relais/<int:relais>", methods=["DELETE"])
def reset_relais(relais):

    if check_permission(relais):
        relais_proxy.set_pin(relais, False)
    else:
        return auth_required()

    return jsonify(payload=relais_result(relais, False))

if __name__ == '__main__':
    app.run()
