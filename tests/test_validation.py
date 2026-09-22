from pathlib import Path

import pytest
from PIL import Image

from src.validation import validate_generation_params, validate_image


def test_valid_image(tmp_path: Path):
    path = tmp_path / "photo.png"
    Image.new("RGB", (64, 64), "white").save(path)
    assert validate_image(path) == path


def test_rejects_non_image(tmp_path: Path):
    path = tmp_path / "fake.png"
    path.write_text("not an image", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_image(path)


def test_generation_params():
    validate_generation_params("Movimiento natural", "1280*704", 81, -1)
    with pytest.raises(ValueError):
        validate_generation_params("", "1280*704", 81, -1)
    with pytest.raises(ValueError):
        validate_generation_params("ok", "1920*1080", 81, -1)
    with pytest.raises(ValueError):
        validate_generation_params("ok", "1280*704", 80, -1)
