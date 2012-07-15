# py-webrelais

## What it does

py-webrelais offers a REST-API to control the [1] K8IO Relais-Card from Pollin, connected to the
parallel port.
Its developed explicitly for Linux, but should run on Windows, too (not tested)

## Basic Usage

* GET / Shows a page to control the relais card

* POST /relais/[0-7]? Set a relais
* GET /relais/[0-7]? Get the state of a specific relais
* DELETE /relais/[0-7]? Set relais to off

If no number is given, it will return/set/reset all relais


## Dependencies

* flask
* pyparallel

## Troubleshooting

If you see some parallel port "permission denied" error messages, check that flask is NOT in debug mode (app.debug=True)

## Installation

    sudo apt-get install python-parallel python-flask

You need to do this to get the parallel library to work:

    sudo rmmod lp
    sudo modprobe ppdev

Add your user to the lp group or change the permissions on /dev/parport0

Now everything should work fine

[1] http://www.pollin.de/shop/dt/NzcyOTgyOTk-/Bausaetze_Module/Bausaetze/Bausatz_PC_Relaiskarte_K8IO.html
