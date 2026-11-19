from __future__ import annotations
import hashlib, json, os, re, time
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
DATA = ROOT / "data"
def load_env(path: Path | None = None) -> dict[str, str]:
    values: dict[str, str] = {}
    path = path or ROOT / ".env"
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
    values.update({k: v for k, v in os.environ.items() if k in {"OPENAI_BASE_URL", "OPENAI_API_KEY", "OPENAI_MODEL", "POLLINATIONS_BASE_URL"}})
    return values
def stable_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)
def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))
def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_").lower()
def retry(operation, attempts: int = 3, delay: float = 1.0):
    last_error = None
    for index in range(attempts):
        try:
            return operation()
        except Exception as exc:
            last_error = exc
            if index + 1 < attempts:
                time.sleep(delay * (index + 1))
    raise last_error
