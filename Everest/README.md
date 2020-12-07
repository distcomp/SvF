# Python API for Everest

A Python wrapper around Everest REST API.

## Requirements

* Python 3 or 2.7
* [Python-Future](https://python-future.org/quickstart.html#installation)
* [Requests](http://docs.python-requests.org/en/latest/)
    * For Python 2.7.9+ simply run `pip install requests`
    * For Python <2.7.9 use `pip install requests[security]` to avoid SSL warnings (check [this answer](http://stackoverflow.com/a/29202163) for more info) 

## Installation

Not needed, just place everest.py in your project.

## Quick Start

1. Use provided CLI to obtain authentication token:

```
python everest.py get-token -u EVEREST_USER -l TOKEN_LABEL
```
By default, the token will be valid in for 7 days. You can request for a variable valid period token by `-t` option, where you can set token's lifespan in seconds. E.g. the following command give you 30 days token

```
python everest.py get-token -server_uri https://optmod.distcomp.org -u EVEREST_USER -l TOKEN_LABEL -t 2592000 | tee .token30d
```


2. See test.py for examples of API usage.
