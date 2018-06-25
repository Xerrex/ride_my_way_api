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
* [Installation and Usage](#installation-and-usage)
  * [Get Repo](#clone-or-download-repo)
  * [Virtual environment & activation](#create-virtual-environment-&-Activate)
  * [Install Dependancies](#install-dependancies)
  * [Enviroment variables](#enviroment-variables)
  * [Run the app](#run-the-app)
  * [Run tests](#run-tests)

## Available endpoints 
* `POST /api/v1/auth/register`: User Registration
   ```
   content_type="application/json"

   {
       "name": "alex dev",
       "email: "alex@dev.com",
       "password: "eleganttests11"
   }
   ```

* `POST /api/v1/auth/login`: User Login
    ```
    content_type="application/json"

    {
        "email":"alex@dev.com",
        "password": "eleganttests11"
    }
    ```

* `POST /api/v1/auth/logout`: User Logout
    

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