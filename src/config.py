from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    backend: str = os.getenv("GENERATOR_BACKEND", "auto").strip().lower()
    wan_repo_dir: Path = Path(os.getenv("WAN_REPO_DIR", "vendor/Wan2.2"))
    wan_checkpoint_dir: Path = Path(os.getenv("WAN_CHECKPOINT_DIR", "models/Wan2.2-TI2V-5B"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "outputs"))
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "20"))

    def resolved_backend(self) -> str:
        if self.backend in {"demo", "wan"}:
            return self.backend
        if self.wan_repo_dir.joinpath("generate.py").exists() and self.wan_checkpoint_dir.exists():
            return "wan"
        return "demo"

    def ensure_dirs(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
