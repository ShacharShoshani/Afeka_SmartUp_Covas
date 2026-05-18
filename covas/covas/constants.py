from pathlib import Path

HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
COVAS_DIR = HOME / ".covas"
STATE_FILE = HOME / ".covas_state.json"
SECRETS_FILE = COVAS_DIR / "donttell.env"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = PROJECT_ROOT / "profiles"

MANAGED_ITEMS = [
    "CLAUDE.md",
    "mcp.json",
    "skills"
]
