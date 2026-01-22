# RPGeet Project - Version 1.0

This project, realised both as a personnal project and as part of the Computer Science : Exercises course at Keio University, proposes a tool to manage extensive ruleset TTRPG systems.

From here on, I will call "project root" the "RPGeet/RPGeet - V1(MVC)/RPGeet" folder.

## Run the project

Once the project is fully configured (see the section below), you can run it in terminal with the simple command `flask run` at the root.

/!\/!\/!\
CERTAIN FUNCTIONNALITIES DONT WORK PROPERLY UNTIL THE DATABASE HAS A MINIMAL POPULATION.

ESPECIALLY, THERE HAS TO BE AT LEAST ONE GAME SYSTEM IN IT WITH ONE SOURCE.

THE PROJECT DOESN'T LET ANYONE BECOME ADMIN FROM THE UI PART, YOU HAVE TO SET IT YOURSELF DIRECTLY ON THE DATABASE BY TOGGLING "core.users.admin" ON THE USER YOU WANT TO BE ADMIN.

WITHOUT IT, YOU CAN'T CREATE THE FIRST GAME SYSTEM AND SOURCE AS YOU CAN'T ACCESS THE ADMIN PAGE.

Note : It is possible that I forgot to link properly the core and system_schema, so you should check that the system_schema has actually been properly created/updated on the first source. You should also note that, for now, the only working schema will probably be pathfinder1 by first creating it on admin page, then executing Pathfinder DB.sql and populate_pathfinder_v0. 
/!\/!\/!\

## Configuration

In order to properly launch and test the project on your own computer, you need to check some configuration requirements, listed below.

### Configuration files

For the project to run, you have to add 2 environment files at the project root. They are both read by the config.py file to set up the connection to the database and the hosting parameters of the server.

#### .env

This file sets up the connection to the database.

IT SHOULD REMAIN SECRET AND UNSHARED FOR SECURITY PURPOSES.

Its main attributes are as follows, WITHOUT COMMENTS OR SPACES NEXT TO THE EQUAL SIGN :

```
SECRET_KEY=random_one_time_generated_key # e.g, cdb723bbb10dbcf37c17580497117f1e2e5d6f4a9e75c
DB_HOST=db_ip_adress # e.g, localhost
DB_PORT=db_port # e.g, 5432
DB_NAME=db_name # e.g, RPGeetDB
DB_USER=db_user # e.g, RPGeetAdmin
DB_PASS=super_secret_password_of_db_user
```

Apart from the "SECRET_KEY", these fields correspond to that of the actual database that you must setup beforehand.

#### .flaskenv

This file sets up the parameters of the webserver.

It follows the same constraints as .env (see above).

```
FLASK_APP=app
FLASK_RUN_HOST=server_wanted_ip_address # e.g, 0.0.0.0 to allow LAN or localhost (127.0.0.1)
FLASK_RUN_PORT=5000
FLASK_DEBUG=1
```

### Requirements

#### DBMS

The project originally uses PostgreSQL 18 as its DBMS. Most of the SQL scripts should probably work on other DBMS like MySQL or SQLite, but I didn't test them.

In order for them to correctly execute, you simply have to update the config.py as such :
line 38 - SQLALCHEMY_DATABASE_URI = "[correct_dbms]://..."

#### Python

The project is developped using 3.13.0 and pip 25.3 for packages setup.

The project uses multiple python package to ensure a better code maintainability :

- os, pathlib, urllib, functools, werkzeug, json, random, typing (normally available by default on any python installation)
- flask (main framework of the project)
- sqlalchemy (orm of the project)
- flask_sqlalchemy (/!\ it is not the same as the 2 above)
- dotenv (for the easy .env and .flaskenv import)

## Miscellaneous

In addition to the real setup of the code, I used several tools to design, manage and edit my project :

- SQL Power Architect : When setting up a connection to the database, you can display its architecture. You can also edit a structure before exporting the SQL code generated (it helps, but the code often require some minor adjustments by digging into it. Besides, it is very poor at displaying interschema connexions)
- pgAdmin 4 : If using PostgreSQL, this helps set up the database (create database, create users) as well as displaying its rows and complete parameters (constraints, functions, ...). It can also easily export SQL scripts to save them.
- Visual Studio Code as an IDE, with Python (by Microsoft) package, Python Indent and SonarQube for IDE.
