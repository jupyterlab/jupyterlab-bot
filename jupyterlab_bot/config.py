# -*- coding: utf-8 -*-
"""Configuration."""
# Standard library imports
import os


# Webapp
# ------
# https://devcenter.heroku.com/articles/optimizing-dyno-usage#python
PORT = int(os.environ.get("PORT", 5000))


# Environment variables on web service infrastructure
# ---------------------------------------------------
GH_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")


# Bot configuration
# -----------------
GITHUB_BOT = "jupyterlab-bot"
GITHUB_BOT_NAME = "JupyterLab Bot"
GITHUB_EVENTS = [
    "check_run",
    "check_suite",
    "commit_comment",
    "create",
    "delete",
    "deploy_key",
    "deployment",
    "deployment_status",
    "fork",
    "gollum",
    "issue_comment",
    "issues",
    "label",
    "member",
    "meta",
    "milestone",
    "page_build",
    "project_card",
    "project_column",
    "project",
    "public",
    "pull_request",
    "pull_request_review",
    "pull_request_review_comment",
    "push",
    "package",
    "release",
    "repository",
    "repository_import",
    "repository_vulnerability_alert",
    "star",
    "status",
    "team_add",
    "watch",
]
GITHUB_HOOK_URL = "https://jupyterlab-bot.herokuapp.com/hooks/github"
