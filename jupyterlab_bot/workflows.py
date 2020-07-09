# -*- coding: utf-8 -*-
"""Github Worflows API."""

# Third party imports
import requests


class Workflows:
    """
    PyGithub does not yet provide handling workflows and runs so this small
    class will take care of those endpoints in the meantime.
    """
    _HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Github Python Client",
    }
    _ENDPOINT = "https://api.github.com"

    def __init__(self, token):
        self._session = requests.Session()

        # Setup
        self._session.headers.update(self._HEADERS)
        self._session.headers.update({"Authorization": f"token {token}"})

    # --- Helpers
    # ------------------------------------------------------------------------
    @staticmethod
    def _parse_response_contents(response):
        """Parse response and convert to json if possible."""
        contents = {}
        # status_code = response.status_code
        # print(status_code)
        try:
            contents = response.json()
        except Exception as err:
            print(err)

        return contents

    @classmethod
    def _make_url(cls, url):
        """Create full api url."""
        return "{}{}".format(cls._ENDPOINT, url)

    def _get(self, url, params=None):
        """Send GET request with given url."""
        response = self._session.get(url=self._make_url(url), params=params)
        return self._parse_response_contents(response)

    def _post(self, url):
        """Send POST request with given url and data."""
        response = self._session.post(url=self._make_url(url))
        return self._parse_response_contents(response)

    # --- Workflows API
    # ------------------------------------------------------------------------
    def get_repo_workflow_runs(
        self, repo_full_name, branch=None, event=None, status=None
    ):
        """
        List repository workflow runs.

        See: https://developer.github.com/v3/actions/workflow-runs/#list-repository-workflow-runs
        """
        url = f"/repos/{repo_full_name}/actions/runs"
        params = {}
        if branch is not None:
            params["branch"] = branch

        if event is not None:
            params["event"] = event

        if event is not None:
            params["status"] = status

        return self._get(url, params=params)

    def get_workflow_runs(
        self, repo_full_name, workflow_id, branch=None, event=None, status=None
    ):
        """     
        List all workflow runs for a workflow.

        See: https://developer.github.com/v3/actions/workflow-runs/#list-workflow-runs
        """
        url = f"/repos/{repo_full_name}/actions/workflows/{workflow_id}/runs"
        params = {}
        if branch is not None:
            params["branch"] = branch

        if event is not None:
            params["event"] = event

        if event is not None:
            params["status"] = status

        return self._get(url, params=params)

    def cancel_run(self, repo_full_name, run_id):
        """
        Cancels a workflow run using its `run_id`.

        See: https://developer.github.com/v3/actions/workflow-runs/#cancel-a-workflow-run
        """
        url = f"/repos/{repo_full_name}/actions/runs/{run_id}/cancel"
        return self._post(url)

    def cancel_dup_builds(self, repo_full_name, head_branch):
        """
        Cancel duplicate builds for a `repo_full_name` and a given `head_branch`.
        """
        print(
            f'Cancelling dup builds for "{repo_full_name}" and branch "{head_branch}"'
        )
        workflow_ids = set()
        workflows = self.get_repo_workflow_runs(
            repo_full_name, branch=head_branch, event="pull_request",
        )

        status = ["queued", "in_progress"]
        for workflow_run in workflows["workflow_runs"]:
            if workflow_run["status"] in status:
                workflow_ids.add(workflow_run["workflow_id"])

        for workflow_id in workflow_ids:
            workflow_runs = self.get_workflow_runs(
                repo_full_name, workflow_id, branch=head_branch, event="pull_request",
            )
            run_ids = [
                run["id"]
                for run in workflow_runs["workflow_runs"]
                if run["status"] in status
            ]
            ids = list(sorted(run_ids))
            print(f"rund ids: {ids}")

            print(f"Checking workflow id: {workflow_id}")
            if len(ids) > 1:
                cancel_ids = ids[:-1]
                for run_id in cancel_ids:
                    result = self.cancel_run(repo_full_name, run_id)
                    print(f"Cancelling run id: {run_id}", result)

            print("\n")
