# computable.py
### Python developer library for interacting with the Computable Protocol
[![Build Status](https://travis-ci.org/computablelabs/computable.py.svg?branch=master)](https://travis-ci.org/computablelabs/computable.py)

This repo contains the Python API for interacting with
the Computable protocol. It consists of a set of
"higher-order contracts", which are object-oriented
interfaces to the core Computable contracts.

## Installation

You can install this package through `pip`. You'll need
an extra command to install `web3` properly, as shown
below.

    pip install -r requirements.txt
    pip install -U web3[tester]

## Setup for Development 

We highly recommend you set up a virtual environment to have a clean
development environment.

    git clone https://github.com/computablelabs/computable.py.git
    python setup.py install

## Running Tests

To run the tests, you simply invoke `pytest`:

    python -m pytest

## Getting Help

If you're having trouble using this library, log into the
[Computable discord server](https://discord.gg/3mFF8zy). Members of the
development team hang out there and might be able to help with your questions.
