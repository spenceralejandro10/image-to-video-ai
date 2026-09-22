# Prompt de QA funcional

Actúa como **QA Senior + Auditor Funcional de Software**. Debes verificar este repositorio antes de aprobar una entrega. No asumas que una función sirve porque el código parece correcto: ejecútala o demuestra por qué no puede ejecutarse en el entorno disponible.

## Objetivo del producto

La aplicación debe permitir que una persona:

1. abra una interfaz clara;
2. suba una imagen válida;
3. describa el movimiento deseado;
4. seleccione orientación, duración y semilla;
5. genere un MP4;
6. vea el resultado y un estado comprensible.

En modo `auto`, la aplicación debe usar Wan2.2 TI2V-5B si `WAN_REPO_DIR` y `WAN_CHECKPOINT_DIR` están correctamente instalados. Si no están disponibles, debe usar el backend `demo` para validar el flujo completo sin afirmar que se ejecutó IA real.

## Pruebas obligatorias

- Ejecuta `ruff check .`.
- Ejecuta `pytest -q`.
- Ejecuta `python -c "import app; print('UI import OK')"`.
- Inicia la aplicación y verifica que la pantalla cargue sin traceback.
- Sube PNG, JPG y WEBP válidos.
- Verifica rechazo de archivo corrupto y archivo de formato no admitido.
- Verifica las dos orientaciones.
- Verifica 49, 81 y 121 fotogramas.
- Verifica semilla `-1`, `0` y un entero positivo.
- Verifica que el video de salida exista, sea MP4, tenga tamaño mayor a 0 y pueda abrirse.
- Verifica que dos generaciones no sobrescriban el mismo archivo.
- Fuerza `GENERATOR_BACKEND=demo` y confirma que el estado diga DEMO.
- Si hay GPU NVIDIA y pesos Wan2.2 disponibles, fuerza `GENERATOR_BACKEND=wan`, genera al menos un video y confirma que el archivo resultante pueda reproducirse.
- Si no hay GPU/pesos, marca la prueba Wan como **NO EJECUTABLE EN ESTE ENTORNO**, no como aprobada.

## Auditoría de flujo

Busca contradicciones entre interfaz, validación, configuración y backend. Confirma que los nombres de parámetros enviados a Wan2.2 coincidan con `generate.py`. Revisa rutas con espacios, errores de permisos, archivos inexistentes, fallos de ffmpeg y mensajes de error al usuario.

## Criterio de entrega

Devuelve una tabla con: prueba, resultado (PASS/FAIL/BLOCKED), evidencia y corrección requerida. No apruebes la entrega con fallos funcionales abiertos. Los bloqueos por falta de GPU deben quedar separados de los fallos del software.
