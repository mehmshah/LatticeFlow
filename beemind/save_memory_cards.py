import json
from json_persistence import atomic_save_json
import os
from typing import List, Dict

def save_memory_cards(cards: List[Dict]):
    """Persist memory board cards to disk (excluding script cards)."""
    atomic_save_json("memory_board_cards.json", cards)
