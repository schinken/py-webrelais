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

If no number is given, it will return/set/reset all relais.
For relais with restricted access you have to set the BasicAuthentication Header (user:password).

## Dependencies

* flask
* pyparallel

## Troubleshooting

If you see some parallel port "permission denied" error messages, check that flask is NOT in debug mode (app.debug=True)

## Permission Checks

You can easly define permissions for each relais. This is important if you control security-related projects with that relai API like door-control. 

Just take a look at the acl.py example. Its also possible to limit the access to a specific host-ip.

If a user performs a POST /relais (to set all relais), or DELETE /relais (to reset all relais), the operation is restricted to the relais for which the user has permission to (depending on the user:password which has been sent through BasicAuthentication)

## Installation

    sudo apt-get install python-parallel python-flask

You need to do this to get the parallel library to work:

    sudo rmmod lp
    sudo modprobe ppdev

Add your user to the lp group or change the permissions on /dev/parport0

Now everything should work fine

[1] http://www.pollin.de/shop/dt/NzcyOTgyOTk-/Bausaetze_Module/Bausaetze/Bausatz_PC_Relaiskarte_K8IO.html
