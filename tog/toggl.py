from typing import List, Optional
import requests
from pydantic import BaseModel, RootModel
from .data_types import Project, StartTimeEntryRequest, TimeEntry, Workspace, Me


class Toggl():
    def __init__(self, token: str, verbose: bool = True) -> None:
        self.auth: (str, str) = (token, "api_token")
        self.verbose: bool = verbose
        self.basev9: str = "https://api.track.toggl.com/api/v9"
        self._me: Me = self.__get_me()

    def __get_me(self):
        r = requests.get(
            "https://api.track.toggl.com/api/v9/me",
            auth=self.auth
        )

        return Me.model_validate_json(r.content)

    def me(self):
        return self._me

    def __get_current_entry(self) -> TimeEntry | None:
        r = self.__toggl_get("me/time_entries/current")
        model = RootModel[Optional[TimeEntry]]
        return model.model_validate_json(r.content).root

    def projects(self) -> List[Project]:
        r = self.__toggl_get("me/projects")
        return RootModel[List[Project]].model_validate_json(r.content).root

    def workspaces(self) -> List[Workspace]:
        response = self.__toggl_get("workspaces")
        model = RootModel[List[Workspace]]
        return model.model_validate_json(response.content).root

    def start(self):
        entry = self.__get_current_entry()
        if entry is not None:
            print("Entry is already started! Ignoring...")
            if self.verbose:
                print(entry.model_dump_json(indent=2))
            return
        else:
            self.__start_new_entry()

    def current(self):
        return self.__get_current_entry()

    def stop(self):
        entry = self.__get_current_entry()
        if entry is None:
            print("No entry started! Ignoring...")
            return
        else:
            if self.verbose:
                print(entry.model_dump_json(indent=2))
            self.__stop_entry(entry)

    def __start_new_entry(self, workspace_id: int = None):
        wid = workspace_id or self._me.default_workspace_id
        req = StartTimeEntryRequest(
            description="Hello Toggl!",
            workspace_id=workspace_id or self._me.default_workspace_id
        )

        print(req.model_dump_json(indent=2))

        r = self.__toggl_post(
            f"workspaces/{wid}/time_entries",
            req)

        print(f"Started time entry!\n{r.content}")

    def __stop_entry(self, entry: TimeEntry):
        wid = entry.workspace_id or self._me.default_workspace_id

        self.__toggl_patch(f"workspaces/{wid}/time_entries/{entry.id}/stop")

    def __toggl_patch(self, resource: str):
        r = requests.patch(
            f"{self.basev9}/{resource}",
            headers={"Content-Type": "application/json"},
            auth=self.auth
        )

        return self.__verify_response(r)

    def __toggl_post(self, resource: str, model: BaseModel):
        url = f"{self.basev9}/{resource}"
        r = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            auth=self.auth,
            data=model.model_dump_json())

        return self.__verify_response(r, url=url)

    def __toggl_get(self, resource: str):
        r = requests.get(
            f"{self.basev9}/{resource}",
            headers={"Content-Type": "application/json"},
            auth=self.auth)

        return self.__verify_response(r)

    def __verify_response(self, response: requests.Response, url=None):
        r = response
        if r.status_code not in range(200, 300):
            raise (RuntimeError("\n\n".join([
                f"[{r.status_code}] {url or ''}",
                str(r.content),
                str(r.headers)
            ])))

        return r
