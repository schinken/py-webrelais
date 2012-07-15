__author__ = 'schinken'

from helpers import *
from parport import Parport
from flask import Flask, render_template

app = Flask(__name__)
pp = Parport()

@app.route("/")
def page_main():
    return render_template('index.html')


@app.route("/relais", methods=["GET"])
@app.route("/relais/<int:relais>", methods=["GET"])
@output_handler
def get_relais( relais=None ):
    return pp.getPin( relais )


@app.route("/relais", methods=["POST"])
@app.route("/relais/<int:relais>", methods=["POST"])
@output_handler
def set_relais( relais=None ):

    mask = get_relais_mask(relais, True)
    if all(x is None for x in mask):
        return auth_required()

    pp.setMask( mask )
    return True


@app.route("/relais", methods=["DELETE"])
@app.route("/relais/<int:relais>", methods=["DELETE"])
@output_handler
def reset_relais( relais=None ):

    mask = get_relais_mask(relais, False)
    if all(x is None for x in mask):
        return auth_required()

    pp.setMask( mask )
    return True


if __name__ == '__main__':
    app.run()
