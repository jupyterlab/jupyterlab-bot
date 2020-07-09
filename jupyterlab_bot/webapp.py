# -*- coding: utf-8 -*-
"""JupyterLab Bot."""

# Standard library imports
from urllib.parse import parse_qs
import json
import os

# Third party imports
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web
from github import Github
from tornado import gen
from tornado.log import enable_pretty_logging

# Local imports
from jupyterlab_bot.workflows import Workflows
import jupyterlab_bot.config as config


# Constants
HERE = os.path.abspath(os.path.dirname(__file__))


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>Welcome to the JupyterLab Bot Application!</h1>")


class GithubHandler(tornado.web.RequestHandler):
    """Handle Github events."""

    def get(self):
        self.write("<h1>Welcome to the JupyterLab Bot Application - Github hook!</h1>")

    @gen.coroutine
    def post(self, headers=None, raw_body=None):
        headers = headers if headers else self.request.headers
        raw_body = raw_body if raw_body else self.request.body

        event_type = headers.get("X-GitHub-Event", None)
        body = tornado.escape.json_decode(raw_body)

        action = body.get("action", None)
        repo = body.get("repository", {})
        repo_id = repo.get("id", None)
        issue = body.get("issue", {})
        pull_request = body.get("pull_request", {})
        issue_number = issue.get("number", None)

        # Check valid repositories
        if repo.get("full_name", "") not in config.REPOS:
            return

        gh = Github(config.GH_TOKEN)
        wf = Workflows(config.GH_TOKEN)

        print("\n\n")
        print("######################################################################")
        print(event_type)
        print("######################################################################")
        print(json.dumps(body, indent=4, sort_keys=True))
        print("\n\n")

        if event_type == "ping":
            self.write("pong")
        elif event_type == "pull_request":
            repo_full_name = repo["full_name"]
            head_branch = pull_request["head"]["ref"]

            # Sleep for 30 seconds so builds have time to start
            yield gen.sleep(30)

            # Cancel duplicate builds
            wf.cancel_dup_builds(repo_full_name, head_branch)


def create_webapp():
    enable_pretty_logging()
    application = tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/hooks/github", GithubHandler),
        ],
        debug=True,
    )
    return application


def main():
    application = create_webapp()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    port = config.PORT
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
