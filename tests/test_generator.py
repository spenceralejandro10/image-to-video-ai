from pathlib import Path

from PIL import Image

from src.config import Settings
from src.generator import build_wan_command, generate_video


def test_demo_generates_mp4(tmp_path: Path):
    image = tmp_path / "input.jpg"
    Image.new("RGB", (320, 240), (60, 100, 160)).save(image)
    settings = Settings(backend="demo", output_dir=tmp_path / "out")

    result = generate_video(
        settings=settings,
        image_path=image,
        prompt="Movimiento suave de cámara",
        size="1280*704",
        frame_num=49,
        seed=42,
    )

    assert result.backend == "demo"
    assert result.video_path.exists()
    assert result.video_path.suffix == ".mp4"
    assert result.video_path.stat().st_size > 1000


def test_build_wan_command(tmp_path: Path):
    repo = tmp_path / "Wan2.2"
    repo.mkdir()
    (repo / "generate.py").write_text("print('stub')", encoding="utf-8")
    model = tmp_path / "model"
    model.mkdir()
    image = tmp_path / "in.png"
    Image.new("RGB", (32, 32)).save(image)
    settings = Settings(
        backend="wan",
        wan_repo_dir=repo,
        wan_checkpoint_dir=model,
        output_dir=tmp_path / "out",
    )
    out = tmp_path / "out.mp4"

    cmd = build_wan_command(
        settings=settings,
        image_path=image,
        prompt="camera motion",
        size="1280*704",
        frame_num=81,
        seed=123,
        output_path=out,
    )

    joined = " ".join(cmd)
    assert "--task ti2v-5B" in joined
    assert "--image" in cmd
    assert "--save_file" in cmd
    assert "--t5_cpu" in cmd
    assert "--convert_model_dtype" in cmd
