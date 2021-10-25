from typing_extensions import Literal
import requests
from uuid import uuid4


HOST = "subcellular-bsp-epfl.apps.hbp.eu/api"


def download_models(user_id: str):
    return requests.get(f"https://{HOST}/models", {"user_id": user_id}).json()


def get_sim_traces(sim_id: str):
    return requests.get(f"https://{HOST}/get_sim_traces", {"sim_id": sim_id}).json()


class Simulation:
    def __init__(self, model_path: str, user_id: str = "") -> None:
        with open(model_path) as model_file:
            self.model_str = model_file.read()
        self.id = str(uuid4())
        self.user_id = user_id

    def run(self, t_end: float, dt: float, solver: Literal["nfsim", "ode", "ssa"]):
        requests.post(
            f"https://{HOST}/run_sim",
            json={
                "userId": self.user_id,
                "status": "",
                "solverConf": {"tEnd": t_end, "dt": dt},
                "solver": solver,
                "simId": "",
                "name": "",
                "id": self.id,
                "annotation": "",
                "model_str": self.model_str,
            },
        )

        return self.id

    def get_sim_traces(self):
        return requests.get(
            f"https://{HOST}/get_sim_traces", {"sim_id": self.id}
        ).json()

