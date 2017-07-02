# Hello Autobahn

This is a _hello world_-like Project for [crossbar](http://crossbar.io/),
[autobahn-python](https://github.com/crossbario/autobahn-python/), and
[autobahn-js](https://github.com/crossbario/autobahn-js/).

## Features

This project provides the next features:

- hello function: it recieves the name and responds with a greetings
- authentication: backend services contect to the crossbar router with
  authetnication, user client (frontend) provide authentication that verified
  in authenticator service

## Installation

I use Docker to develop and run this project.

```bash
$ docker-compose build
# Build the docker-images for the services
$ docker-compose up -d
# Open http://localhost:8080 in your browser
```
