from pathlib import Path

from src.config import Settings


def test_auto_falls_back_to_demo(tmp_path: Path):
    settings = Settings(
        backend="auto",
        wan_repo_dir=tmp_path / "missing-repo",
        wan_checkpoint_dir=tmp_path / "missing-model",
        output_dir=tmp_path / "out",
    )
    assert settings.resolved_backend() == "demo"


def test_auto_detects_wan(tmp_path: Path):
    repo = tmp_path / "Wan2.2"
    repo.mkdir()
    (repo / "generate.py").write_text("# stub", encoding="utf-8")
    model = tmp_path / "model"
    model.mkdir()
    settings = Settings(
        backend="auto",
        wan_repo_dir=repo,
        wan_checkpoint_dir=model,
        output_dir=tmp_path / "out",
    )
    assert settings.resolved_backend() == "wan"
