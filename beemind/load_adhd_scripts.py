import json
from json_persistence import load_json
import os
from typing import List, Dict

def load_adhd_scripts() -> List[Dict]:
    """Load ADHD scripts from beemind/adhd_scripts.json."""
    try:
        return load_json("beemind/adhd_scripts.json", default=[])
    except Exception:
        return []
