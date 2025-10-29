"""Minimal FastAPI environment server (HTTP-based)."""

import logging
import sys
from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from game import GameMemory
from enums import MoveResult

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Memory Game Environment API")

game_env = GameMemory()

# Reward mapping for different move results
REWARD_MAP: Dict[MoveResult, float] = {
    MoveResult.MATCHING: 5.0,
    MoveResult.NO_MATCH: 0.0,
    MoveResult.INVALID: -1.0,
    MoveResult.ERROR: -5.0,
    MoveResult.GAME_OVER: 20.0,
}


class ActionRequest(BaseModel):
    """Request model for game actions."""
    action: str


class SetupRequest(BaseModel):
    """Request model for game setup."""
    size: int = Field(gt=0, description="Board size (must be positive and even for pairs)")


@app.get("/health")
def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/act")
def act(request: ActionRequest) -> Dict[str, Any]:
    """Execute a game action and return the result."""
    move_result = game_env.move(request.action)
    board_snapshot = game_env.get_board_ascii(debug=False)

    # If no match, hide the cards again
    if move_result == MoveResult.NO_MATCH:
        try:
            r1, c1, r2, c2 = map(int, request.action.split())
            game_env.shown[r1, c1] = False
            game_env.shown[r2, c2] = False
        except (ValueError, IndexError):
            # Action string was invalid, but game.py already handled it
            logger.warning(f"Failed to parse action for card hiding: {request.action}")

    reward = REWARD_MAP.get(move_result, 0.0)
    game_env.last_accumulated_reward += reward

    return {
        "step_reward": reward,
        "last_accumulated_reward": game_env.last_accumulated_reward,
        "done": bool(game_env.game_over),
        "board": board_snapshot,
    }


@app.post("/setup")
def setup(request: SetupRequest) -> Dict[str, Any]:
    """Initialize or reset the game with a new board size."""
    game_env.setup(request.size)
    return {"ok": True, "board": game_env.get_board_ascii(debug=False)}


@app.get("/state")
def state() -> Dict[str, Any]:
    """Get the current game state."""
    return game_env.get_state()


@app.get("/board")
def board() -> Dict[str, str]:
    """Get the current board state with debug information."""
    return {"board": game_env.get_board_ascii(debug=True)}
