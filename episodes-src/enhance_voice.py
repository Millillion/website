"""Speech enhancement with DeepFilterNet3: removes rustling, handling noise and room noise.

Reads any audio via ffmpeg, processes at 48 kHz mono in chunks, and writes a 48 kHz WAV.
  PYTHONPATH=<deepfilternet>:<torchaudio> python3 episodes-src/enhance_voice.py in.m4a out.wav [atten_db]
"""
import subprocess, sys, wave
import numpy as np
import torch
from df.enhance import enhance, init_df

src, dst = sys.argv[1], sys.argv[2]
atten = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0  # cap suppression so the voice stays natural

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                     check=True, capture_output=True).stdout
audio = np.frombuffer(raw, dtype=np.float32).copy()

model, state, _ = init_df()  # DeepFilterNet3, default weights
sr = state.sr()
chunk, overlap = sr * 30, sr // 2
out = np.zeros_like(audio)
pos = 0
while pos < len(audio):
    a, b = max(0, pos - overlap), min(len(audio), pos + chunk + overlap)
    seg = torch.from_numpy(audio[a:b]).unsqueeze(0)
    enh = enhance(model, state, seg, atten_lim_db=atten).squeeze(0).numpy()
    s0, s1 = pos - a, pos - a + min(chunk, len(audio) - pos)
    out[pos:pos + (s1 - s0)] = enh[s0:s1]
    pos += chunk
    print(f"{pos / sr / 60:5.1f} / {len(audio) / sr / 60:.1f} min", flush=True)

pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
with wave.open(dst, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
print("wrote", dst)
