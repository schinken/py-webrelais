__author__ = 'schinken'

import helpers

from flask import Flask, render_template
from relais import SainSmart, Relais, RelaisProxy
from settings import relais

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
@helpers.output_handler
def get_relais(relais=None):

    if relais:
        return relais_proxy.get_pin(relais)
    else:
        return relais_proxy.get_pins()

@app.route("/relais/<int:relais>", methods=["POST"])
@helpers.output_handler
def set_relais(relais):

    if helpers.check_permission(relais):
        relais_proxy.set_pin(relais, True)
    else:
        return helpers.auth_required()

    return True

@app.route("/relais/<int:relais>", methods=["DELETE"])
@helpers.output_handler
def reset_relais(relais):

    if helpers.check_permission(relais):
        relais_proxy.set_pin(relais, False)
    else:
        return helpers.auth_required()

    return True

if __name__ == '__main__':
    app.run()
