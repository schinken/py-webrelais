__author__ = 'schinken'

import json
from parport import Parport
from flask import Flask

app = Flask(__name__)

pp = Parport()

@app.route("/")
def page_main():
    return "hai"


@app.route("/ports", methods=["GET"])
def get_ports():
    return json.dumps( pp.getPins() )


@app.route("/ports/<int:number>", methods=["GET"])
def get_port(number):

    try:
        return json.dumps( pp.getPin( number ) )
    except Exception:
        return Exception.message, 404


@app.route("/ports", methods=["POST"])
def set_ports():
    pp.setPins()
    return json.dumps( True )


@app.route("/ports/<int:number>", methods=["POST"])
def set_port(number):

    try:
        pp.setPin( number )
        return json.dumps( True )
    except Exception:
        return Exception.message, 404


@app.route("/ports", methods=["DELETE"])
def reset_ports():
    pp.resetPins()
    return json.dumps( True )


@app.route("/ports/<int:number>", methods=["DELETE"])
def reset_port(number):
    try:
        pp.resetPin( number )
        return json.dumps( True )
    except Exception:
        return Exception.message, 404


if __name__ == '__main__':
    app.debug = True
    app.run()