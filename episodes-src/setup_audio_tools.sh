#!/usr/bin/env bash
# One-time (idempotent) setup of the audio toolchain into ~/.cache/millillion/pylib.
# Prints the PYTHONPATH to use with enhance_voice.py.
set -euo pipefail
LIB="$HOME/.cache/millillion/pylib"
mkdir -p "$LIB"
command -v ffmpeg >/dev/null || { echo "install ffmpeg"; exit 1; }
command -v whisper >/dev/null || { echo "install openai-whisper (pip install -U openai-whisper)"; exit 1; }
python3 -c "import torch" || { echo "install torch"; exit 1; }
if [ ! -d "$LIB/df" ]; then
  pip install -q --target "$LIB" --no-deps deepfilternet deepfilterlib
  pip install -q --target "$LIB" --no-deps loguru appdirs
  TV=$(python3 -c "import torch;print(torch.__version__.split('+')[0])")
  pip install -q --target "$LIB" --no-deps "torchaudio==$TV"
  # deepfilternet 0.5.6 imports a module torchaudio removed; it is only used for type hints
  sed -i 's/^from torchaudio.backend.common import AudioMetaData/try:\n    from torchaudio.backend.common import AudioMetaData\nexcept Exception:\n    AudioMetaData = object/' "$LIB/df/io.py"
fi
PYTHONPATH="$LIB" python3 -c "from df.enhance import enhance, init_df" && echo "PYTHONPATH=$LIB"
