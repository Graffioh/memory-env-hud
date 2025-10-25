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


class ActionRequest(BaseModel):
    action: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/act")
def act(request: ActionRequest):
    move_result = game_env.move(request.action)

    # Sparse rewarding scheme
    reward_map = {
        MoveResult.MATCHING: 5.0,
        MoveResult.NO_MATCH: 0.0,
        MoveResult.INVALID: -1.0,
        MoveResult.ERROR: -5.0,
        MoveResult.GAME_OVER: 20.0,
    }

    reward = reward_map.get(move_result, 0.0)
    game_env.last_accumulated_reward += reward

    return {
        "step_reward": reward,
        "last_accumulated_reward": game_env.last_accumulated_reward,
        "done": bool(game_env.game_over),
        "board": game_env.get_board_ascii(debug=False),
    }


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
