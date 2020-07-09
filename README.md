# Jupyterlab Bot Service

This application is freely hosted on [Heroku](https://dashboard.heroku.com/apps/jupyterlab-bot).

The application can be fount at [this endpoint](https://jupyterlab-bot.herokuapp.com/).

This application is heavily inspired by [Conda Forge](https://github.com/conda-forge/conda-forge-webservices/).

## Usage

### Cancelling duplicate builds

* Duplicate builds on PRs are automatically cancelled after a timeout of some seconds to account for the time between the `pull_request` event and the start of the github actions workers.

## Development

### Conda

```bash
conda create --name jupyterlab-bot python>=3.6 pygithub tornado --channel conda-forge
conda activate jupyterlab-bot
pip install -e .
python run.py
```

Open a browser and search for `http://localhost:5000/`.

## Release

* Install [Docker](https://docs.docker.com/get-docker/).
* Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

You will need to have an account in both Heroku and Docker.

### First time

```bash
heroku login
heroku create jupyterlab-bot
heroku container:login
heroku container:push web
heroku container:release web
heroku open
```

### Next time

```bash
heroku login
heroku container:login
heroku container:push web
heroku container:release web
heroku open
```
