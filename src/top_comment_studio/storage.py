import json
from pathlib import Path

from .schemas import EpisodeRecord


class ChainStore:
    def __init__(self, root: Path, series_id: str = "main") -> None:
        self.root = root
        self.series_id = series_id
        self.chain_dir = self.root / "chains" / series_id

    def next_episode_id(self) -> str:
        self.chain_dir.mkdir(parents=True, exist_ok=True)
        existing = sorted(self.chain_dir.glob("episode_*.json"))
        return f"episode_{len(existing) + 1:03d}"

    def path_for(self, episode_id: str) -> Path:
        return self.chain_dir / f"{episode_id}.json"

    def save(self, record: EpisodeRecord) -> Path:
        self.chain_dir.mkdir(parents=True, exist_ok=True)
        path = self.path_for(record.episode_id)
        path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
        return path

    def get(self, episode_id: str) -> EpisodeRecord | None:
        if "/" in episode_id or "\\" in episode_id:
            return None
        self.chain_dir.mkdir(parents=True, exist_ok=True)
        path = self.path_for(episode_id)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return EpisodeRecord.model_validate(data)

    def latest(self) -> EpisodeRecord | None:
        self.chain_dir.mkdir(parents=True, exist_ok=True)
        records = sorted(self.chain_dir.glob("episode_*.json"))
        if not records:
            return None
        data = json.loads(records[-1].read_text(encoding="utf-8"))
        return EpisodeRecord.model_validate(data)
