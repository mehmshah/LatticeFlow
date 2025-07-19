import json
from json_persistence import load_json
import os
from typing import List, Dict

def load_memory_cards() -> List[Dict]:
    """Load memory board cards from disk (excluding script cards)."""
    try:
        if os.path.exists("memory_board_cards.json"):
            return load_json("memory_board_cards.json", default=[])
    except Exception:
        pass
    return []
