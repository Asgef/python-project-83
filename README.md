<div align="center">

  <h1>Hexlet project: Page analyzer</h1>

  [Analyze web pages for SEO suitability](https://python-project-83-1-5pft.onrender.com)



### Hexlet tests and linter status:
[![Actions Status](https://github.com/Asgef/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Asgef/python-project-83/actions)  [![linter-tests](https://github.com/Asgef/python-project-83/actions/workflows/main.yml/badge.svg)](https://github.com/Asgef/python-project-83/actions/workflows/main.yml)  [![Maintainability](https://api.codeclimate.com/v1/badges/243c8fb73479ed6d03a3/maintainability)](https://codeclimate.com/github/Asgef/python-project-83/maintainability)

</div>

## Description

This project was created as part of the "Python Developer" course on the [Hexlet educational platform](https://hexlet.io).


**Page analyzer** is a small yet full-fledged web application based on the Flask framework, which evaluates websites for SEO suitability.

This project applies the fundamental principles of building modern websites based on the MVC architecture, including routing, handling requests, templating, and interacting with the database.

To create the website's appearance, Bootstrap 5 framework is used along with the Jinja2 template engine. The frontend of the page is rendered on the server side. This means that the Jinja2 backend generates the prepared HTML, which is then rendered by the server.

PostgreSQL is used as the object-relational database system with the Psycopg library, allowing direct interaction with PostgreSQL from Python.


## Features

- Check, normalize, and add a new URL to the database;
- Check the site's availability;
- Collect data such as h1 tags, title, and description, add them to the database;
- Display a list of all added sites and the dates of their last checks;
- Display detailed information for each site;

## Usage

### 1. Add URL for Analysis:
   - Submit URL for analysis; the application will automatically validate and normalize it.
   - The URL will be added to the database for further analysis.

### 2. Check site accessibility and perform SEO analysis:
   - Make sure the specified site is accessible.
   - Retrieve detailed information about the page, including SEO-related metrics.

### 3. View All Added URLs:
   - Display a list of all added URLs for quick reference.

### 4. Individual URL Details:
   - Explore specific details for each entered URL on a dedicated page.


## Built With
- Python
- Flask
- PostgreSQL
- Gunicorn
- Bootstrap 5

## Demonstration
Check out the demo version deployed on Render:
https://page-analyzer-app-yb5a.onrender.com/


## Installation

 ### Requirements
Before starting the installation, make sure you have the following components 
 installed:

- Python (version 3.10 or higher)
- PIP (version 24.0 or higher)
- PostgreSQL (version 16.2 or higher)
- Poetry (Python package installer)
- Git (version 2.43 or higher)


### Steps


#### 1. Cloning the repository.
Execute the following command in your terminal to clone the repository to your local machine:


    git clone git@github.com:Asgef/python-project-83.git


#### 2. Installing Dependencies.
Navigate to the project directory and execute the command to install dependencies:


    make install


#### 3. Setting up environment variables.
Create a .env file in the root directory of the project and specify the necessary environment variables, for example:


    DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
    SECRET_KEY = '{your secret key}'


#### 4. Creating a database.
Create a PostgreSQL database if it does not exist yet:


    make build


#### 5. Running the application.
Launch the web application using the following command:

    make start


#### 6. Running the application.
Verification:
Open a web browser and navigate to http://localhost:5000 to verify that the application has been successfully installed and is running.