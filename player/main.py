# setup fastapi app code
import importlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import dotenv

from models.Action import Action
from utils import *

dotenv.load_dotenv('dev.env')

args = get_command_line_args()
validate_command_line_args(args)

env = get_env_vars(args.player)

player_file = importlib.import_module(f"players.player_{args.player}")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/tick")
@authorized(token=env['token'])
@pre_check()
def tick(body: dict):
    try:
        state: State = generate_state(body['state'])

        try:
            actions: List[Action] = player_file.tick(state)
        except Exception as e:
            print(e, "Error in player file")
            actions = []

        if not actions:
            actions = []

        serialized_actions = [action.__dict__ for action in actions]
        response_body = {
            "actions": serialized_actions
        }

        return response_body
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something Went Wrong")


@app.get("/health")
def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host=env['host'], port=env['port'])
