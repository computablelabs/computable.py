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

## Running Tests

To run the tests, you simply invoke `pytest`:

    pytest
