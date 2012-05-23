# py-webrelais

## What it does

py-webrelais offers a REST-API to control the K8IO Relais-Card, connected to the
parallel port.

## Basic Usage

* GET / Shows a page to control the relais card

* POST /ports/[0-7]? Set a relais
* GET /ports/[0-7]? Get the state of a specific relais
* DELETE /ports/[0-7]? Set relais to off

If no number is given, it will return/set/reset all relais


## Dependencies

* flask
* pyparallel
