import requests
import json
from datetime import datetime



class Toggl():
    def __init__(self, token: str, verbose :bool = True) -> None:
        self.auth = (token, "api_token")
        self.verbose = verbose
        self.basev9 = "https://api.track.toggl.com/api/v9"

    def me(self):
        r = requests.get(
            "https://api.track.toggl.com/api/v9/me",
            auth=self.auth
            )
        print(pretty_response(r))

    def get_current_entry(self):
        r = self.__toggl_get("me/time_entries/current")
        return json.loads(r.content)
    
    def workspaces(self):
        print(pretty_response(self.__toggl_get(
            "workspaces"
        )))

    def start(self):
        entry = self.get_current_entry()
        if entry != None:
            print(f"Entry is already started! Ignoring...")
            if self.verbose: 
                print(json.dumps(entry), indent=2)
            return
        else:
            self.__start_new_entry()

    def stop(self):
        entry = self.get_current_entry()
        if entry == None:
            print(f"No entry started! Ignoring...")
            return
        else:
            if self.verbose:
                print(json.dumps(entry, indent=2))
            self.__stop_entry(entry["workspace_id"], entry["id"])


    def __mk_start_time_entry_request(self, workspace_id: int):
        data = {
            "created_with": "tog CLI tool",
            "description": "hello toggl!",
            "tags": [],
            "billable": False,
            "workspace_id": workspace_id,
            "duration": -1,
            "start": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "stop": None
        }

        print(json.dumps(data, indent=2))

        return data

    def __start_new_entry(self, workspace_id: int = 6880206):
        self.__toggl_post(
            f"workspaces/{workspace_id}/time_entries", 
            self.__mk_start_time_entry_request(workspace_id))

    def __stop_entry(self, workspace_id: int, time_entry_id: int):
        self.__toggl_patch(f"workspaces/{workspace_id}/time_entries/{time_entry_id}/stop")

    def __toggl_patch(self, resource: str):
        r = requests.patch(
            f"{self.basev9}/{resource}",
            headers= {"Content-Type": "application/json"},
            auth= self.auth
        )

        return self.__verify_response(r)

    def __toggl_post(self, resource: str, data: dict):
        url = f"{self.basev9}/{resource}"
        r = requests.post(
            url, 
            headers={"Content-Type": "application/json"}, 
            auth=self.auth,
            data=json.dumps(data))

        return self.__verify_response(r)

    
    def __verify_response(self, response: requests.Response):
        r = response
        if r.status_code not in range(200, 300):
            raise(RuntimeError("\n\n".join([
                f"[{r.status_code}]",
                str(r.content),
                str(r.headers)
            ])))
        
        return r


    def __toggl_get(self, resource: str, require_json: bool=True):
        if require_json: 
            headers = {"Content-Type": "application/json"}
        else:
            headers = None
        
        r = requests.get(
            f"{self.basev9}/{resource}",
            headers=headers,
            auth=self.auth)
        
        return self.__verify_response(r)
        


    



def pretty_response(r: requests.Response) -> str:
    if r.status_code != 200:
        return f"[{r.status_code}] Bad status!\n{str(r.content)}"
    
    return "\n\n".join([
        f"[{r.status_code}]",
        "JSON: " + json.dumps(json.loads(r.content), indent=2),
        f"RAW: {r.content}"
    ])
