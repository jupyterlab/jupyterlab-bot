# -*- coding: utf-8 -*-
"""JupyterLab Bot."""
# Standard library imports
import json
import os
import re

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web
from github import Github
from tornado import gen
from tornado.log import enable_pretty_logging

import jupyterlab_bot.config as config
from jupyterlab_bot.workflows import Workflows

# Third party imports
# Local imports


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
        full_name = repo["full_name"]
        repo_id = repo.get("id", None)
        issue = body.get("issue", {})
        pull_request = body.get("pull_request", {})
        ref = body.get("ref", {})
        issue_number = issue.get("number", None)

        gh = Github(config.GH_TOKEN)
        wf = Workflows(config.GH_TOKEN)

        print("\n\n")
        print("######################################################################")
        print(event_type)
        print("######################################################################")
        print(json.dumps(body, indent=4, sort_keys=True))
        print("\n\n")

        branch = None

        if event_type == "ping":
            self.write("pong")

        elif event_type == "pull_request":
            branch = pull_request["head"]["ref"]

        elif event_type == "push":
            match = re.match(r"refs/heads/(\S+)", ref)
            if match:
                branch = match.groups()[0]
            else:
                print("skipping push event for", ref)

        if branch:
            # Sleep for 15 seconds so builds have time to start
            # Cancel duplicate builds
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.call_later(15, wf.cancel_dup_builds, full_name, branch, event_type)


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
