import time
from typing import List

from models.Action import Action
from models.State import State


def tick(state: State) -> List[Action]:
    print(state)
    time.sleep(0.5)
    return []
