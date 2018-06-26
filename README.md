# [ride_my_way_api]()

![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/Xerrex/ride_my_way_api.svg?branch=develop)](https://travis-ci.org/Xerrex/ride_my_way_api)
[![Coverage Status](https://coveralls.io/repos/github/Xerrex/ride_my_way_api/badge.svg?branch=develop)](https://coveralls.io/github/Xerrex/ride_my_way_api?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/2c6b807869eebb4c226b/maintainability)](https://codeclimate.com/github/Xerrex/ride_my_way_api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2c6b807869eebb4c226b/test_coverage)](https://codeclimate.com/github/Xerrex/ride_my_way_api/test_coverage)

## Introduction
* An API for the Ride-my-way application.
* Ride-my-way App is a carpooling application that provides drivers with the ability to    
  create ride offers and passengers to join available ride offers.

## Technologies used & needed.
* **[Python3](https://www.python.org/downloads/)** - A programming language that lets you work more quickly (The universe loves speed!).
* **[Flask](flask.pocoo.org/)** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments

## Table of contents
* [Available endpoints](#available-endpoints)
  * [User Registration](#user-Registration)
  * [User Login](#user-login)
  * [User Logout](#user-logout)
  * [Creates a ride offer](#creates-a-ride-offer)
  * [Get available rides](#get-available-rides)
  * [Get a specific ride](#get-a-specific-ride)
  * [Make requests to join a ride](#make-requests-to-join-a-ride)
  * [Retract request to join a ride](#retract-request-to-join-a-ride)

* [Installation and Usage](#installation-and-usage)
  * [Get Repo](#clone-or-download-repo)
  * [Virtual environment & activation](#create-virtual-environment-&-Activate)
  * [Install Dependancies](#install-dependancies)
  * [Enviroment variables](#enviroment-variables)
  * [Run the app](#run-the-app)
  * [Run tests](#run-tests)

## Available endpoints
*  #### User Registration. 

    `POST /api/v1/auth/register`: 
    ```
    content_type="application/json"

    {
        "name": "alex dev",
        "email: "alex@dev.com",
        "password: "eleganttests11"
    }
    ```

* #### User Login.
    `POST /api/v1/auth/login`: 
    ```
    content_type="application/json"

    {
        "email":"alex@dev.com",
        "password": "eleganttests11"
    }
    ```

* #### User Logout. 
    `POST /api/v1/auth/logout`
    

* #### Creates a ride offer.
    `POST /api/v1/rides`: 
    ```
    content_type="application/json"

    {
        "starting_point": "Nairobi-Kencom",
        "destination": "Taita-wunda",
        "depart_time": "26-06-2018 21:00",
        "eta": "27-06-2018 03:00",
        "seats": 4,
        "vehicle": "KCH 001"
    }
    ```
* #### Get available rides.
    `GET /api/v1/rides`


* #### Get a specific ride.
    `GET /api/v1/rides/<rideId>` 

* #### Make requests to join a ride.
    `POST /api/v1/rides/<rideId>/requests`:
    ```
    content_type="application/json"

    {
        "destination": "Voi"
    }
    ```
* #### Retract request to join a ride
    `DELETE /api/v1/rides/<rideId>/requests`

## Installation and usage

**NB** 
* Run the command after **$**:
* **$** and anything before it, shows prompt status.

1. #### **Clone or download repo.**
    ```
    $ git clone https://github.com/Xerrex/ride_my_way_api.git
    ```
2. #### **Create virtual environment & Activate.**
    ```
    $ virtualenv -p python3.6 Venv 
    $ source venv/bin/activate
    ```
3. #### **Install Dependancies.**
    ```
    (venv)$ pip install -r requirements.txt
    ```
4. #### **Enviroment variables.**

    ```
    (venv)$ touch .env
    ```
    * **Add the following lines to .env file**
    ```
    source venv/bin/activate
    export export FLASK_APP="run.py"
    export SECRET_KEY="[replace with phrase]"
    export FLASK_ENV=development
    ```
    * You can now run **source .env** to:
      * activate virtual enviroment
      * export the FLASK_APP - enables flask run
      * export the SECRET_KEY - Creates secret key
      * export FLASK_ENV - enables the development environment

5. #### **Run the app**
   ```
    (venv)$ flask run
   ```
6. #### **Run Tests**
  ```
  (venv)$ pytest
  ```