## Version
- Python 3.8.7
- Flask 1.1.2

## Overview
Notifier fitbit's activity info for AWS Lambda, deploying zappa.
with management, https://github.com/KaitakuShiba/fitbit.

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
            "expression": "cron(50 14 * * ? *)"
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

## For Pixela
ref: https://docs.pixe.la
```bash
# create user
curl -X POST https://pixe.la/v1/users -d '{"token":"token", "username":"username", "agreeTermsOfService":"yes", "notMinor":"yes"}'

# create graph
curl -X POST https://pixe.la/v1/users/username/graphs -H 'X-USER-TOKEN: token' -d '{"id":"grassgraph","name":"run-graph","unit":"achievement_rate","type":"int","color":"shibafu"}'

# check create graph
https://pixe.la/v1/users/username/graphs/grassgraph.html
```

## Slack Notify Example
<img width="683" alt="スクリーンショット 2023-04-01 14 24 10" src="https://user-images.githubusercontent.com/38932286/229267316-49de2b5f-a858-40db-9ed6-8cfc2eb01fd4.png">
