# REST API for Q&AProject.
* [Installation](#installation)
* [Setup](#setup)
* [Usage](#usage)
* [Related repositories](#related-repositories)
## Installation

#### Install Python >= 3.7
#### Install docker and docker-compose
#### Clone this repository
git clone https://github.com/unbrokenguy/Q-n-A-rest-api.git
#### Or download zip archive and unzip it
https://github.com/unbrokenguy/Q-n-A-rest-api/archive/refs/heads/master.zip
#### Install poetry
```shell
pip install poetry
```

#### Install the project dependencies
```shell
cd src
poetry install 
```

## Setup

### Start current server
#### Spawn a shell within the virtual environment
```shell
poetry shell
```

#### Add environments
* SECRET_KEY: Your secret key for django application.

#### Start server
```shell
python manage.py runserver
```
Server will be available at this url  `http://localhost:8000/` or `http://127.0.0.1:8000/`

## Usage

## Related repositories
1. [Telegram bot](https://github.com/unbrokenguy/Q-n-A-telegram-bot)