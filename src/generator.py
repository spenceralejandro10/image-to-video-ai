from __future__ import annotations

import math
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageEnhance

from .config import Settings
from .validation import validate_generation_params, validate_image


@dataclass(frozen=True)
class GenerationResult:
    video_path: Path
    backend: str
    message: str


def _safe_output_path(settings: Settings, prefix: str) -> Path:
    settings.ensure_dirs()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return settings.output_dir / f"{prefix}-{stamp}-{uuid.uuid4().hex[:8]}.mp4"


def build_wan_command(
    *,
    settings: Settings,
    image_path: Path,
    prompt: str,
    size: str,
    frame_num: int,
    seed: int,
    output_path: Path,
) -> list[str]:
    generate_py = settings.wan_repo_dir / "generate.py"
    if not generate_py.exists():
        raise RuntimeError(f"No encuentro Wan2.2 en {settings.wan_repo_dir}.")
    if not settings.wan_checkpoint_dir.exists():
        raise RuntimeError(f"No encuentro los pesos del modelo en {settings.wan_checkpoint_dir}.")

    return [
        sys.executable,
        str(generate_py),
        "--task",
        "ti2v-5B",
        "--size",
        size,
        "--ckpt_dir",
        str(settings.wan_checkpoint_dir),
        "--offload_model",
        "True",
        "--convert_model_dtype",
        "--t5_cpu",
        "--image",
        str(image_path),
        "--prompt",
        prompt,
        "--frame_num",
        str(frame_num),
        "--base_seed",
        str(seed),
        "--save_file",
        str(output_path),
    ]


def generate_with_wan(
    settings: Settings,
    image_path: Path,
    prompt: str,
    size: str,
    frame_num: int,
    seed: int,
) -> GenerationResult:
    output = _safe_output_path(settings, "wan")
    cmd = build_wan_command(
        settings=settings,
        image_path=image_path,
        prompt=prompt,
        size=size,
        frame_num=frame_num,
        seed=seed,
        output_path=output,
    )
    proc = subprocess.run(
        cmd,
        cwd=settings.wan_repo_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.returncode != 0 or not output.exists():
        tail = "\n".join(proc.stdout.splitlines()[-30:])
        raise RuntimeError(f"Wan2.2 no pudo generar el video.\n\n{tail}")
    return GenerationResult(output, "wan", "Video generado con Wan2.2 TI2V-5B.")


def _cover_resize(image: Image.Image, width: int, height: int) -> Image.Image:
    image = image.convert("RGB")
    ratio = max(width / image.width, height / image.height)
    resized = image.resize(
        (math.ceil(image.width * ratio), math.ceil(image.height * ratio)),
        Image.Resampling.LANCZOS,
    )
    left = max(0, (resized.width - width) // 2)
    top = max(0, (resized.height - height) // 2)
    return resized.crop((left, top, left + width, top + height))


def generate_demo_motion(
    settings: Settings,
    image_path: Path,
    prompt: str,
    size: str,
    frame_num: int,
    seed: int,
) -> GenerationResult:
    """CPU-only fallback that proves the complete upload→MP4 flow without claiming AI inference."""
    output = _safe_output_path(settings, "demo")
    width, height = (640, 352) if size == "1280*704" else (352, 640)
    fps = 24
    rng = np.random.default_rng(None if seed == -1 else seed)
    phase = float(rng.uniform(0, math.tau))

    with Image.open(image_path) as source:
        source = _cover_resize(source, width + 96, height + 96)
        writer = imageio.get_writer(
            output,
            fps=fps,
            codec="libx264",
            quality=7,
            macro_block_size=None,
        )
        try:
            for i in range(frame_num):
                t = i / max(1, frame_num - 1)
                zoom = 1.0 + 0.07 * t
                frame_w = int(width / zoom)
                frame_h = int(height / zoom)
                cx = source.width / 2 + math.sin(phase + t * math.pi) * 20
                cy = source.height / 2 + math.cos(phase + t * math.pi) * 14
                left = int(np.clip(cx - frame_w / 2, 0, source.width - frame_w))
                top = int(np.clip(cy - frame_h / 2, 0, source.height - frame_h))
                frame = source.crop((left, top, left + frame_w, top + frame_h)).resize(
                    (width, height),
                    Image.Resampling.LANCZOS,
                )
                frame = ImageEnhance.Contrast(frame).enhance(1.01)
                writer.append_data(np.asarray(frame))
        finally:
            writer.close()

    return GenerationResult(
        output,
        "demo",
        "Flujo validado en modo DEMO (movimiento CPU). Instala Wan2.2 para generación IA real.",
    )


def generate_video(
    *,
    settings: Settings,
    image_path: str | Path,
    prompt: str,
    size: str = "1280*704",
    frame_num: int = 81,
    seed: int = -1,
) -> GenerationResult:
    image = validate_image(image_path, settings.max_upload_mb)
    validate_generation_params(prompt, size, frame_num, seed)

    backend = settings.resolved_backend()
    if backend == "wan":
        return generate_with_wan(settings, image, prompt.strip(), size, frame_num, seed)
    return generate_demo_motion(settings, image, prompt.strip(), size, frame_num, seed)
