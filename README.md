# CarparkAPI

This is a simple frontend and backend implementation of a Carpark API, designed for testing and contextualizing the backend API functionality.

## Setup

To set up the environment, run the following command in the root folder in a terminal: `pip install -r "requirements.txt"`

## Running carparkAPI Locally

To run carparkAPI locally, execute: `python carparkapi.py` from the root folder in a terminal.

## Running carparkAPI Locally using Gunicorn

To run carparkAPI locally, execute: `gunicorn -w 4 -b 0.0.0.0:8000 carparkapi:app` from the root folder in a terminal.

To terminate instances, excute `lsof -i :8000` and `kill -9 <PID>`.

## Running Unit Tests

To run unit tests for the backend API, execute: `pytest` from the root folder in a terminal.

## Frontend GitHub Pages Link:

You can view the frontend UI hosted on GitHub Pages at: [joyteoyw.github.io](https://joyteoyw.github.io/)

## Disclaimers

- The frontend UI is designed to contextualize the CarparkAPI and provide a (hopefully) more interesting experience when testing out the backend APIs.
  
- The **'GET /car/lots'** API is not part of the 3 defined API requirements and is only meant for contextualization purposes. It is not intended for grading.


