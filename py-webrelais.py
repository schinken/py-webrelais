__author__ = 'schinken'

from parport import Parport
from flask import Flask, render_template,jsonify

app = Flask(__name__)

pp = Parport()

@app.route("/")
def page_main():
    return render_template('index.html')


@app.route("/ports", methods=["GET"])
def get_ports():
    return jsonify( response=pp.getPins() )


@app.route("/ports/<int:number>", methods=["GET"])
def get_port(number):

    try:
        return jsonify( response=pp.getPin( number ) )
    except Exception:
        return Exception.message, 404


@app.route("/ports", methods=["POST"])
def set_ports():
    pp.setPins()
    return jsonify( response=True )


@app.route("/ports/<int:number>", methods=["POST"])
def set_port(number):

    try:
        pp.setPin( number )
        return jsonify( response=True )
    except Exception:
        return Exception.message, 404


@app.route("/ports", methods=["DELETE"])
def reset_ports():
    pp.resetPins()
    return jsonify( response=True )


@app.route("/ports/<int:number>", methods=["DELETE"])
def reset_port(number):
    try:
        pp.resetPin( number )
        return jsonify( response=True )
    except Exception:
        return Exception.message, 404


if __name__ == '__main__':
    app.debug = True
    app.run()