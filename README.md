# py-webrelais

## What it does

py-webrelais offers a REST-API to control the K8IO Relais-Card, connected to the
parallel port.

## Basic Usage

* GET / Shows a page to control the LED Board

* POST /relais/[0-7]? Set a portbin
* GET /relais/[0-7]? Get the state of a specific relais
* DELETE /relais/[0-7]? Set relais to off

If no number is given, it will return/set/reset all relais


## Dependencies

* flask
* portio
