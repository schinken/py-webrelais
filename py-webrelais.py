__author__ = 'schinken'

from helpers import check_permission, auth_required, relay_result
from flask import Flask, render_template, jsonify
from relays import SainSmart, Relay, RelaysProxy
from settings import relay_cards

app = Flask(__name__)

relays_proxy = RelaysProxy()

for entry in relay_cards:
    sainsmart = SainSmart(entry['serial'])
    wrapper = Relay(sainsmart)
    relays_proxy.add_relay(entry['start'], entry['relays'], wrapper)

@app.route("/")
def page_main():
    return render_template('index.html')


@app.route("/relais", methods=["GET"])
@app.route("/relais/<int:relay>", methods=["GET"])
def get_relais(relay=None):

    if relay is None:
        response = []
        for relay, status in enumerate(relays_proxy.get_relays()):
            response.append(relay_result(relay, status))
    else:
        response = relay_result(relay, relais_proxy.get_relay(relay))

    return jsonify(payload=response)

@app.route("/relais/<int:relay>", methods=["POST"])
def set_relais(relay):

    if check_permission(relay):
        relays_proxy.set_relay(relay, True)
    else:
        return auth_required()

    return jsonify(payload=relay_result(relay, True))

@app.route("/relais/<int:relay>", methods=["DELETE"])
def reset_relais(relay):

    if check_permission(relay):
        relays_proxy.set_relay(relay, False)
    else:
        return auth_required()

    return jsonify(payload=relay_result(relay, False))

if __name__ == '__main__':
    app.run()
