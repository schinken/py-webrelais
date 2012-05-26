__author__ = 'schinken'

from parport import Parport
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

pp = Parport()

@app.route("/")
def page_main():
    return render_template('index.html')


@app.route("/ports", methods=["GET"])
def get_ports():
    return output_data( pp.getPins() )


@app.route("/ports/<int:number>", methods=["GET"])
def get_port(number):

    try:
        return output_data( pp.getPin( number ) )
    except Exception:
        return Exception.message, 404


@app.route("/ports", methods=["POST"])
def set_ports():
    pp.setPins()
    return output_data( True )


@app.route("/ports/<int:number>", methods=["POST"])
def set_port(number):

    try:
        pp.setPin( number )
        return output_data( True )
    except Exception:
        return Exception.message, 404


@app.route("/ports", methods=["DELETE"])
def reset_ports():
    pp.resetPins()
    return output_data( True )


@app.route("/ports/<int:number>", methods=["DELETE"])
def reset_port(number):
    try:
        pp.resetPin( number )
        return output_data( True )
    except Exception:
        return Exception.message, 404

def output_data( data ):

    format = request.args.get('format', 'json')

    if format == 'json':
        return jsonify( response=data )
    elif format == 'raw':

        if type(data) != list:
            data = [data]

        str = ''
        for d in data:
            if d:
                str += '1'
            else:
                str += '0'

        return str
            

if __name__ == '__main__':
    app.run()
