# MotionLab AI — Image to Video

Aplicación web sencilla para convertir una imagen en video. El backend de IA objetivo es **Wan2.2 TI2V-5B**, ejecutado en infraestructura propia. El proyecto no usa Supabase ni requiere una API comercial para generar.

## Estado

- ✅ Interfaz Gradio lista.
- ✅ Flujo completo imagen → MP4 validable sin GPU mediante backend `demo`.
- ✅ Backend Wan2.2 integrado mediante el `generate.py` oficial.
- ✅ Selección automática de backend.
- ✅ Pruebas unitarias + lint + importación de UI en GitHub Actions.
- ✅ Prompt de QA funcional en `QA_PROMPT.md`.

> El backend `demo` solo genera movimiento de cámara para probar el producto de extremo a extremo. No se presenta como inferencia de IA. La generación IA real necesita una GPU NVIDIA y los pesos de Wan2.2.

## Requisitos rápidos

### Probar interfaz y flujo sin GPU

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abre `http://localhost:7860`.

### Instalar Wan2.2 TI2V-5B

En un equipo Linux con GPU NVIDIA compatible:

```bash
python scripts/setup_wan.py
python app.py
```

El instalador clona el repositorio oficial `Wan-Video/Wan2.2`, instala sus dependencias y descarga `Wan-AI/Wan2.2-TI2V-5B` (aprox. 34 GB). La configuración por defecto usa:

```text
WAN_REPO_DIR=vendor/Wan2.2
WAN_CHECKPOINT_DIR=models/Wan2.2-TI2V-5B
GENERATOR_BACKEND=auto
```

Wan2.2 TI2V-5B soporta generación imagen→video; el comando oficial utiliza `--task ti2v-5B`, `--image`, `--prompt`, offload de modelo y T5 en CPU para reducir VRAM.

## Configuración

Copia `.env.example` como referencia. Las variables disponibles son:

| Variable | Valor por defecto | Uso |
|---|---|---|
| `GENERATOR_BACKEND` | `auto` | `auto`, `demo` o `wan` |
| `WAN_REPO_DIR` | `vendor/Wan2.2` | código oficial de Wan2.2 |
| `WAN_CHECKPOINT_DIR` | `models/Wan2.2-TI2V-5B` | pesos del modelo |
| `OUTPUT_DIR` | `outputs` | videos generados |
| `MAX_UPLOAD_MB` | `20` | límite de imagen |

## QA

```bash
pip install -r requirements-dev.txt
ruff check .
pytest -q
python -c "import app; print('UI import OK')"
```

La auditoría completa está definida en [`QA_PROMPT.md`](QA_PROMPT.md).

## Arquitectura

```text
Gradio UI
   │
   ▼
Validación de imagen/parámetros
   │
   ▼
Selector de backend
   ├── demo → CPU → MP4
   └── wan  → Wan2.2 TI2V-5B → GPU → MP4
```

## Modelo

El proyecto apunta a **Wan-AI/Wan2.2-TI2V-5B**, publicado con licencia Apache-2.0. El repositorio oficial indica 720p y un modo de ejecución en una GPU de 24 GB con offloading.

## Uso responsable

Procesa únicamente contenido que tengas derecho a utilizar. Respeta privacidad, consentimiento, derechos de autor y la legislación aplicable.
