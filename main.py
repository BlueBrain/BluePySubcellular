from typing_extensions import Literal
import requests
from uuid import uuid4
import os
import time


API_HOST = "https://subcellular-rest-bsp-epfl.apps.hbp.eu"
HOST = "https://subcellular-bsp-epfl.apps.hbp.eu/api"
# HOST = "http://localhost:8888/api"
# API_HOST = "http://localhost:8001"


def create_model(path: str, name: str, user_id: str):
    with open(path) as f:
        model = requests.post(
            f"{API_HOST}/import-bngl", data={"name": name, "user_id": user_id}, files={"file": f}
        ).json()
        print(f"Created model {model['name']} with id {model['id']}")
        return model


def create_geometry(path: str, user_id: str, model_id: int):
    head, tail = os.path.split(path)
    name, _ = os.path.splitext(tail)
    files = []

    for ext in ("json", "node", "ele", "face"):
        filename = f"{name}.{ext}"
        f = os.path.join(head, filename)
        files.append((filename, open(f, "rb").read()))

    files = tuple((("files"), f) for f in files)

    r = requests.post(
        f"{API_HOST}/geometries",
        data={"name": name, "user_id": user_id, "model_id": model_id},
        files=files,
    )

    print(f"Geometry created for model {model_id}")


def download_models(user_id: str):
    return requests.get(f"{API_HOST}/models", {"user_id": user_id}).json()


def get_sim_traces(sim_id: str):
    return requests.get(f"{HOST}/get_sim_traces", {"sim_id": sim_id}).json()


class Simulation:
    def __init__(
        self,
        name: str,
        model_id: int,
        user_id: str,
        solver: Literal["tetexact", "tetopsplit", "nfsim", "ode", "ssa"],
        dt: float,
        t_end: float,
        stimuli_path="",
    ) -> None:
        self.id = str(uuid4())
        stimuli = []

        if stimuli_path:
            stimuli = import_stimuli(stimuli_path)

        self.sim_config = {
            "name": name,
            "userId": user_id,
            "status": "created",
            "solverConf": {"tEnd": t_end, "dt": dt, "stimulation": stimuli},
            "solver": solver,
            "simId": self.id,
            "id": self.id,
            "annotation": "",
            "modelId": model_id,
        }

        requests.post(f"{HOST}/create_sim", json=self.sim_config)

    def update_sim(self):
        time.sleep(5)
        self.sim_config = requests.get(f"{HOST}/get_sim", {"sim_id": self.sim_config["id"]}).json()

    @property
    def progress(self):
        self.update_sim()
        return self.sim_config["progress"]

    @property
    def status(self):
        self.update_sim()
        return self.sim_config["status"]

    def run(self):
        if self.status != "created":
            print("Simulation already started, see sim.progress or sim.status")
            return
        requests.post(f"{HOST}/run_sim", json={**self.sim_config, "simId": self.sim_config["id"]})
        return self.id

    def get_sim_traces(self):
        return requests.get(f"{HOST}/get_sim_traces", {"sim_id": self.id}).json()


def import_stimuli(path: str):
    stimuli = []

    with open(path) as f:
        for l in f.readlines():
            line = l.strip()
            if not line:
                continue

            parsed = line.split()
            stimuli.append({"t": float(parsed[0]), "type": parsed[1], "target": parsed[2], "value": float(parsed[3])})

    return stimuli
