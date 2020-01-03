# Flux Project Bot

This project is designed to help create and manage Flux projects. The process to submit a project is:
* Fill out a form: https://voteflux.org/volunteer-project-form/
* The data gets sent to a google sheet
* Gspread is used to collect the data from sheet
* A Discord.py bot sends the data to the Flux community Discord server for discussion

## Setup

```
pip install -r requirements.txt
```

## Run

During testing:

```
python3 projectbot.py
```

Run on server

```
chmod +x run-cicd.sh
```

Then (on startup)

```
./run-cicd.h
```

Users on the Discord server can interact with the bot by calling the command:
```
!project [num]
```
Where [num] is the project number

by Kipling Crossing
