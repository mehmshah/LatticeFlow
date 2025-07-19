import os
import json
import shutil
from datetime import datetime
from typing import Any

def atomic_save_json(path: str, obj: Any, backup: bool = True, backup_dir: str = "backups", keep_last: int = 5):
    """
    Atomically save a JSON file with optional backup/versioning.
    - Writes to a temp file, then renames.
    - Optionally creates a timestamped backup in backup_dir.
    - Keeps only the most recent 'keep_last' backups per file.
    """
    tmp_path = path + ".tmp"
    # Write to temp file
    with open(tmp_path, "w") as f:
        json.dump(obj, f, indent=2)
    # Atomically replace
    os.replace(tmp_path, path)
    # Backup
    if backup:
        os.makedirs(backup_dir, exist_ok=True)
        base = os.path.basename(path)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{base}.{ts}.bak")
        shutil.copy2(path, backup_path)
        # Prune old backups
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith(base + ".")], reverse=True)
        for old in backups[keep_last:]:
            try:
                os.remove(os.path.join(backup_dir, old))
            except Exception:
                pass

def load_json(path: str, default: Any = None) -> Any:
    """
    Load JSON from file, return default if missing/corrupt.
    """
    if not os.path.exists(path):
        if default is not None:
            atomic_save_json(path, default, backup=False)
            return default
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        if default is not None:
            return default
        return None
