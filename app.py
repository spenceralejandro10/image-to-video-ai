from __future__ import annotations

import gradio as gr

from src.config import Settings
from src.generator import generate_video

settings = Settings()
settings.ensure_dirs()

CSS = """
:root { --radius-lg: 22px; }
.gradio-container { max-width: 1180px !important; margin: 0 auto !important; }
.hero { padding: 28px 30px; border-radius: 24px; border: 1px solid rgba(128,128,128,.22); margin-bottom: 18px; }
.hero h1 { margin: 0 0 8px 0; font-size: 2.25rem; letter-spacing: -.04em; }
.hero p { margin: 0; opacity: .78; font-size: 1.04rem; }
.panel { border-radius: 22px !important; }
.status-card { padding: 10px 14px; border-radius: 14px; border: 1px solid rgba(128,128,128,.2); }
#generate-btn { min-height: 50px; font-size: 1.05rem; font-weight: 700; }
footer { display: none !important; }
"""


def backend_label() -> str:
    backend = settings.resolved_backend()
    if backend == "wan":
        return "🟢 Motor IA: Wan2.2 TI2V-5B listo"
    return "🟡 Modo DEMO activo · instala/configura Wan2.2 para inferencia IA real"


def run_generation(image_path, prompt, orientation, duration, seed):
    if not image_path:
        raise gr.Error("Sube una imagen primero.")
    size = "1280*704" if orientation == "Horizontal 16:9" else "704*1280"
    frames = {"≈ 2 s": 49, "≈ 3.4 s": 81, "≈ 5 s": 121}[duration]
    try:
        result = generate_video(
            settings=settings,
            image_path=image_path,
            prompt=prompt,
            size=size,
            frame_num=frames,
            seed=int(seed),
        )
    except Exception as exc:
        raise gr.Error(str(exc)) from exc
    return str(result.video_path), f"{result.message}  |  Motor: {result.backend.upper()}"


with gr.Blocks(title="MotionLab AI") as demo:
    gr.HTML(
        """
        <div class="hero">
          <h1>MotionLab AI</h1>
          <p>Convierte una imagen en un video con movimiento. Sube, describe el movimiento y genera.</p>
        </div>
        """
    )
    gr.Markdown(f"**{backend_label()}**", elem_classes=["status-card"])

    with gr.Row(equal_height=True):
        with gr.Column(scale=5, elem_classes=["panel"]):
            image = gr.Image(
                type="filepath",
                label="1. Imagen de origen",
                sources=["upload"],
                height=390,
            )
            prompt = gr.Textbox(
                label="2. Describe el movimiento",
                placeholder=(
                    "Ej.: movimiento natural de cámara, el cabello se mueve suavemente "
                    "con el viento, iluminación cinematográfica..."
                ),
                lines=4,
                max_lines=7,
                value=(
                    "Movimiento natural y fluido de cámara, iluminación cinematográfica, "
                    "conservar la identidad visual y los detalles principales de la imagen."
                ),
            )
            with gr.Accordion("Ajustes", open=False):
                orientation = gr.Radio(
                    ["Horizontal 16:9", "Vertical 9:16"],
                    value="Horizontal 16:9",
                    label="Formato",
                )
                duration = gr.Radio(
                    ["≈ 2 s", "≈ 3.4 s", "≈ 5 s"],
                    value="≈ 3.4 s",
                    label="Duración",
                )
                seed = gr.Number(value=-1, precision=0, label="Semilla (-1 = aleatoria)")
            generate = gr.Button(
                "Generar video",
                variant="primary",
                elem_id="generate-btn",
            )

        with gr.Column(scale=5, elem_classes=["panel"]):
            video = gr.Video(label="Resultado", height=500, autoplay=True)
            status = gr.Textbox(label="Estado", interactive=False)

    gr.Markdown(
        "Uso responsable: utiliza imágenes que tengas derecho a procesar y respeta "
        "la privacidad, el consentimiento y la legislación aplicable."
    )

    generate.click(
        run_generation,
        inputs=[image, prompt, orientation, duration, seed],
        outputs=[video, status],
    )

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=1).launch(
        server_name="0.0.0.0",
        server_port=7860,
        css=CSS,
    )
