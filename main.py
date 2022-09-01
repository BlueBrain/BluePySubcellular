from typing_extensions import Literal, TypedDict
import requests
from uuid import UUID, uuid4
import os


HOST = "http://localhost:8001"


def create_model(path: str, name: str, user_id: str):
    with open(path) as f:
        model = requests.post(f"{HOST}/import-bngl", data={"name": name, "user_id": user_id}, files={"file": f}).json()
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
        f"{HOST}/geometries",
        data={"name": name, "user_id": user_id, "model_id": model_id},
        files=files,
    )

    print(f"Geometry created for model {model_id}")


def download_models(user_id: str):
    return requests.get(f"https://{HOST}/models", {"user_id": user_id}).json()


def get_sim_traces(sim_id: str):
    return requests.get(f"https://{HOST}/get_sim_traces", {"sim_id": sim_id}).json()


class SimulationConf(TypedDict):
    userId: UUID
    tEnd: float
    dt: float
    solver: Literal["tetexact", "nfsim", "ode", "ssa"]
    modelId: int


class Simulation:
    def __init__(self, model_id: int, user_id: str) -> None:
        self.model_id = model_id
        self.id = str(uuid4())
        self.user_id = user_id

    def run(self, t_end: float, dt: float, solver: Literal["tetexact", "nfsim", "ode", "ssa"], stimuli_path=""):

        stimuli = []
        if stimuli_path:
            stimuli = import_stimuli(stimuli_path)

        sim_config = {
            "userId": self.user_id,
            "status": "created",
            "solverConf": {"tEnd": t_end, "dt": dt, "stimulation": stimuli},
            "solver": solver,
            "simId": self.id,
            "name": "",
            "id": self.id,
            "annotation": "",
            "modelId": self.model_id,
        }

        requests.post(f"https://{HOST}/run_sim", json=sim_config)

        return self.id

    def get_sim_traces(self):
        return requests.get(f"https://{HOST}/get_sim_traces", {"sim_id": self.id}).json()


def import_stimuli(path: str):
    stimuli = []

    with open(path) as f:
        for l in f.readlines():
            line = l.strip()
            if not line:
                continue

            parsed = line.split()
            stimuli.append({"t": parsed[0], "type": parsed[1], "target": parsed[2], "value": parsed[3]})

    return stimuli
