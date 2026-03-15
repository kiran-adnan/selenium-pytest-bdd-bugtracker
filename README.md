# Selenium Pytest BDD Automation Framework

Mini automation framework demonstrating:

- Selenium UI automation
- Pytest framework
- BDD using pytest-bdd
- API testing using requests
- Page Object Model
- Allure reporting
- Screenshot on failure
- Logging

## Structure

backend/ - Flask API server  
features/ - BDD feature files  
steps/ - Step definitions  
pages/ - Page Object Model  
tests/ - API tests  
reports/ - Test reports

## Run tests

Start backend:

python backend/app.py

Run tests:

pytest

Generate Allure report:

allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

![Automation Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/automation.yml/badge.svg)