"""Tools router for environment interaction."""

from hud.server import MCPRouter
from hud.tools.types import EvaluationResult
from server.shared import http_client

router = MCPRouter()


@router.tool
async def act(action: str) -> str:
    """Perform a move in the memory game by selecting two positions: 'r1 c1 r2 c2'."""
    resp = await http_client.post("/act", json={"action": action})
    data = resp.json()
    return data.get("board", "")


@router.tool
async def setup() -> str:
    """Initialize or reset the memory game to its starting state."""
    resp = await http_client.post("/reset")
    data = resp.json()
    return data.get("board", "Game reset")


@router.tool
async def show_current_board() -> str:
    """Show the current board state."""
    resp = await http_client.get("/board")
    data = resp.json()
    return data.get("board", "")


@router.tool
async def evaluate() -> EvaluationResult:
    """Evaluate the game state."""
    resp = await http_client.get("/state")
    state = resp.json()
    reward = state.get("reward", 0)
    score = state.get("score", 0)
    done = state.get("game_over", False)
    return EvaluationResult(
        reward=reward, done=done, content=f"Score: {score}, Game over: {done}"
    )
