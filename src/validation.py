from __future__ import annotations

from pathlib import Path

from PIL import Image

ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_SIZES = {"1280*704", "704*1280"}
ALLOWED_FRAME_COUNTS = {49, 81, 121}


def validate_image(path: str | Path, max_upload_mb: int = 20) -> Path:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise ValueError("La imagen no existe o no se pudo leer.")
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError("Formato no soportado. Usa PNG, JPG, JPEG o WEBP.")
    if p.stat().st_size > max_upload_mb * 1024 * 1024:
        raise ValueError(f"La imagen supera el límite de {max_upload_mb} MB.")
    try:
        with Image.open(p) as im:
            im.verify()
    except Exception as exc:
        raise ValueError("El archivo no es una imagen válida.") from exc
    return p


def validate_generation_params(prompt: str, size: str, frame_num: int, seed: int) -> None:
    if not prompt or not prompt.strip():
        raise ValueError("Describe brevemente el movimiento que quieres generar.")
    if len(prompt) > 1200:
        raise ValueError("La descripción es demasiado larga (máximo 1200 caracteres).")
    if size not in ALLOWED_SIZES:
        raise ValueError("Resolución no soportada.")
    if frame_num not in ALLOWED_FRAME_COUNTS or (frame_num - 1) % 4 != 0:
        raise ValueError("El número de fotogramas debe ser 49, 81 o 121.")
    if seed < -1 or seed > 2_147_483_647:
        raise ValueError("La semilla debe estar entre -1 y 2147483647.")
