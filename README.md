# [ride_my_way_api]()

![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/Xerrex/ride_my_way_api.svg?branch=develop)](https://travis-ci.org/Xerrex/ride_my_way_api)
[![Coverage Status](https://coveralls.io/repos/github/Xerrex/ride_my_way_api/badge.svg?branch=develop)](https://coveralls.io/github/Xerrex/ride_my_way_api?branch=develop)

## Introduction
* An API for the Ride-my-way application.
* Ride-my-way App is a carpooling application that provides drivers with the ability to    
  create ride offers and passengers to join available ride offers.

## Technologies used & needed.
* **[Python3](https://www.python.org/downloads/)** - A programming language that lets you work more quickly (The universe loves speed!).
* **[Flask](flask.pocoo.org/)** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments

## Installation / Usage
1. **Clone or download repo.**
    ```
    git clone https://github.com/Xerrex/ride_my_way_api.git
    ```
2. **Create virtual environment & Activate.**
    ```
    $ virtualenv -p python3.6 Venv 
    $ source venv/bin/activate
    ```
3. **Install Dependancies.**
    ```
    (venv)$ pip install -r requirements.txt
    ```
4. **Enviroment variables.**

    ```
    (venv)$ touch .env
    ```
    * **Add the following lines to .env file**
    ```
    source venv/bin/activate
    ```
    * You can now run **source .env** to:
      * activate virtual enviroment 
