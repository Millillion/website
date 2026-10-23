"""Print a JavaScript snippet that checks the open YouTube Studio edit page against the expected text.

  python3 episodes-src/youtube_verify_js.py NNN <slug|full>

Run check_text.py first (it writes episodes-src/NNN/youtube/). Paste the output into javascript_exec on
https://studio.youtube.com/video/<id>/edit (after clicking "Show more" so tags render). It returns "OK" or
the exact differences, character for character.
"""
import json, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1], "youtube"); k = sys.argv[2]
want = {f: open(f"{D}/{k}.{f}.txt").read().strip() for f in ("title", "description", "tags")}
print(f"""(() => {{
  const want = {json.dumps(want, ensure_ascii=False)};
  const got = {{
    title: document.querySelector('#title-textarea #textbox')?.innerText.trim(),
    description: document.querySelector('#description-textarea #textbox')?.innerText.trim(),
    tags: [...document.querySelectorAll('ytcp-chip')].map(c => c.innerText.trim()).filter(Boolean).join(', '),
  }};
  const out = [];
  for (const f of ['title', 'description', 'tags']) {{
    const a = want[f], b = got[f] || '';
    if (f === 'tags' ? a.toLowerCase().split(/,\\s*/).sort().join() !== b.toLowerCase().split(/,\\s*/).sort().join() : a !== b) {{
      let i = 0; while (i < a.length && a[i] === b[i]) i++;
      out.push(`${{f}} differs at char ${{i}}: want "${{a.slice(Math.max(0, i - 20), i + 40)}}" got "${{b.slice(Math.max(0, i - 20), i + 40)}}"`);
    }}
  }}
  return out.length ? out.join('\\n') : 'OK';
}})()""")
