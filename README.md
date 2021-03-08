## Version
- Python 3.8.7
- Flask 1.1.2

## Overview
Notifier fitbit's activity info for AWS Lambda. Use zappa

## Premise
- Requirement fitbit.db file and set environment variable for AWS Lambda.
- ref: https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/configuration-envvars.html
- Edit IAM for zappa.
- ref: https://github.com/zappa/Zappa

## Setup
```bash
$ pip install pipenv
$ cd this_project
$ pipenv --python 3.8
$ pipenv install -r requirements.txt
$ pipenv run python migrate.py
# create zappa setting
$ pipenv run zappa init
$ pipenv run zappa deploy dev
# after edit file
$ pipenv run zappa update dev
```

After zappa init, update setting.

```zappa.settings.json
{
    "dev": {
        "app_function": "app.app",
        ..
        "events": [{
            "function": "app.check_distance_job",
            "expression": "cron(15 10 * * ? *)"
        }],
        "keep_warm": false
    }
}
```

```.env
SLACK_BOT_TOKEN = ''
SLACK_CHANNEL = ''
CLIENT_ID = ''
CLIENT_SECRET = ''
SECRET_KEY = ''
```
