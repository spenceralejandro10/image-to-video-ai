from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Instala el backend local Wan2.2 TI2V-5B.")
    parser.add_argument("--repo-dir", default="vendor/Wan2.2")
    parser.add_argument("--model-dir", default="models/Wan2.2-TI2V-5B")
    parser.add_argument("--skip-deps", action="store_true", help="No instala las dependencias upstream.")
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir)
    model_dir = Path(args.model_dir)
    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    model_dir.parent.mkdir(parents=True, exist_ok=True)

    if not repo_dir.exists():
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/Wan-Video/Wan2.2.git",
                str(repo_dir),
            ]
        )
    else:
        print(f"Wan2.2 ya existe en {repo_dir}; no se vuelve a clonar.")

    if not args.skip_deps:
        run([sys.executable, "-m", "pip", "install", "-r", str(repo_dir / "requirements.txt")])

    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        run([sys.executable, "-m", "pip", "install", "huggingface_hub>=0.27"])
        from huggingface_hub import snapshot_download

    print("Descargando Wan-AI/Wan2.2-TI2V-5B (aprox. 34 GB)...")
    snapshot_download(
        repo_id="Wan-AI/Wan2.2-TI2V-5B",
        local_dir=str(model_dir),
        local_dir_use_symlinks=False,
    )

    print("\nBackend listo.")
    print("Ejecuta: python app.py")
    print("El modo 'auto' detectará Wan2.2 automáticamente.")


if __name__ == "__main__":
    main()
