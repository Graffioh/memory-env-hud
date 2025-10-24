"""Minimal FastAPI environment server (HTTP-based)."""

from fastapi import FastAPI
from pydantic import BaseModel

import logging
import sys

from .game import GameMemory

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)

app = FastAPI(title="Memory Game Environment API")

game_env = GameMemory()

class ActRequest(BaseModel):
    action: str

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/act")
def act(request: ActRequest):
    reward = 0
    success = game_env.move(request.action)

    if not success:
        reward = -1.0
    else:
        reward = 5

    # Add bonus if game finishes
    if game_env.game_over:
        reward += 10

    return {"reward": reward, "board": game_env.get_board_ascii()}


@app.post("/reset")
def reset():
    game_env.reset()
    return {"ok": True, "board": game_env.get_board_ascii()}


@app.get("/state")
def state():
    state_dict = game_env.get_state()
    return state_dict


@app.get("/board")
def board():
    return {"board": game_env.get_board_ascii()}
