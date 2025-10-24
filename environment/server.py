"""Minimal FastAPI environment server (HTTP-based)."""

from fastapi import FastAPI
from pydantic import BaseModel

import logging
import sys

from game import GameMemory
from enums import MoveResult

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
    move_result = game_env.move(request.action)

    if move_result == MoveResult.SUCCESS:
        reward = 5.0
    elif move_result == MoveResult.INVALID:
        reward = -1.0
    elif move_result == MoveResult.ERROR:
        reward = -5.0

    # Add bonus if game finishes??
    if game_env.game_over:
        reward += 10.0

    game_env.last_reward = reward
    return {"reward": reward, "board": game_env.get_board_ascii(debug=False)}


@app.post("/reset")
def reset():
    game_env.reset()
    return {"ok": True, "board": game_env.get_board_ascii(debug=False)}


@app.get("/state")
def state():
    state_dict = game_env.get_state()
    return state_dict


@app.get("/board")
def board():
    return {"board": game_env.get_board_ascii(debug=True)}
