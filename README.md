# Jupyterlab Bot Service

This application is freely hosted on [Heroku](https://dashboard.heroku.com/apps/jupyterlab-bot).

The application can be fount at [this endpoint](https://jupyterlab-bot.herokuapp.com/).

This application is heavily inspired by [Conda Forge](https://github.com/conda-forge/conda-forge-webservices/).

## Usage

### Cancelling duplicate builds

* Duplicate builds on PRs are automatically cancelled after a timeout of some seconds to account for the time between the `pull_request` event and the start of the github actions workers.

### Installing the WebHook

Install a [webhook](https://docs.github.com/en/developers/webhooks-and-events/creating-webhooks) on your repo:

* Payload URL: `https://jupyterlab-bot.herokuapp.com/hooks/github`
* Content Type: `application/json`
* Select `Let me select invidual events`
* Select `Pull requests` and `Pushes`
* Ensure `Active` is checked
* Click `Update webhook`

## Development

### Installation

```bash
conda create --name jupyterlab-bot python>=3.6 pygithub tornado --channel conda-forge
conda activate jupyterlab-bot
pip install -e .
```

### Local Usage

```bash
python run.py
```

Open a browser and search for `http://localhost:5000/`.

Also browse to `/hooks/github` and verify page render.

## Release

* Install [Docker](https://docs.docker.com/get-docker/).
* Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

You will need to have an account in both Heroku and Docker.

Log in to Heroku and get Docker credentials:

```bash
heroku login
heroku container:login
```

If creating, run:

```bash
heroku create jupyterlab-bot
```

Otherwise, run:

```bash
heroku git:remote -a jupyterlab-bot
```

Then run:

```
heroku container:push web
heroku container:release web
heroku open
```

Browse to `/hooks/github` and verify page render.
