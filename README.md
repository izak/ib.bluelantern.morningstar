# Morningstar plugin for BlueLantern

This is a pyramid extension. It starts up a thread that periodically queries
the MorningStar TriStar MPPT for voltage and current values. It publishes
these on the mqtt bus.

## Dependencies

This is meant to plug into ib.bluelantern, but you can run it standalone. It
depends on pymodbus, but that will be installed automatically by pip. Note
that because pymodbus depends on Twisted, you need to have a C compiler and
the relevant headers installed. Twisted is not used however, so you may
customise setup.py in pymodbus and remove this dependency.

## Configuration

Add lines similar to below to your development.ini file.

    pyramid.includes =
        ...
        ib.bluelantern.morningstar.mppt

    morningstar.instance = battery01
    morningstar.name = mppt
    morningstar.port = /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0
