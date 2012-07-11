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
@app.route("/relais/<int:port>", methods=["GET"])
@check_permissions
@output_handler
def get_relais( port=None ):
    return pp.getPin( port )


@app.route("/relais", methods=["POST"])
@app.route("/relais/<int:port>", methods=["POST"])
@check_permissions
@output_handler
def set_relais( port=None ):
    pp.setPin( port )
    return True


@app.route("/relais", methods=["DELETE"])
@app.route("/relais/<int:port>", methods=["DELETE"])
@check_permissions
@output_handler
def reset_relais( port=None ):
    pp.resetPin( port )
    return True


if __name__ == '__main__':
    app.debug = True
    app.run()
