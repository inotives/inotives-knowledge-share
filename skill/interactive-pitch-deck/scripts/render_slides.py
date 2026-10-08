#!/usr/bin/env python3
"""Render slides of a reveal.js deck to PNG with headless Chrome, in chosen interactive states.

Usage:
  render_slides.py DECK.html OUTDIR  SPEC [SPEC ...]

  SPEC = name=n:3                       slide 3, all fragments shown
         name=n:3,f:-1                  slide 3, no fragments shown (opening state)
         name=n:3,f:2                   slide 3, fragments up to index 2
         name=n:3,c:.tab@2              slide 3, then click the 3rd element matching .tab
         name=n:3,c:.tab@2;.fxb@0       several clicks, separated by ;

Works on a temporary copy: transitions are switched off, so fragments render in
their final state. The deck itself is never modified. Chrome is found at
$CHROME or the default macOS path.
"""
import os, re, subprocess, sys, tempfile, pathlib, urllib.parse

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
HOOK = """<script>setTimeout(function(){
var q=new URLSearchParams(location.search);
var n=+q.get('n')||1, f=q.get('f'); Reveal.slide(n-1,0,f===null?99:+f);
(q.get('c')||'').split(';').filter(Boolean).forEach(function(c){
  var p=c.split('@'); var els=document.querySelectorAll(p[0]); var i=+(p[1]||0); if(els[i]) els[i].click();
});},600);</script></body>"""
FREEZE = "<style>*{transition:none !important;animation:none !important}</style></head>"

def prepare(deck: pathlib.Path) -> pathlib.Path:
    html = deck.read_text(encoding="utf-8")
    html = re.sub(r"transition:\s*'[a-z]+'", "transition: 'none'", html)
    html = re.sub(r"backgroundTransition:\s*'[a-z]+'", "backgroundTransition: 'none'", html)
    html = html.replace("</head>", FREEZE, 1).replace("</body>", HOOK, 1)
    tmp = pathlib.Path(tempfile.mkdtemp()) / "deck-render.html"
    tmp.write_text(html, encoding="utf-8")
    return tmp

def main(argv):
    if len(argv) < 4:
        print(__doc__); return 2
    deck, out = pathlib.Path(argv[1]), pathlib.Path(argv[2])
    out.mkdir(parents=True, exist_ok=True)
    tmp = prepare(deck)
    for spec in argv[3:]:
        name, _, rest = spec.partition("=")
        params = {}
        for part in re.split(r",(?=[a-z]:)", rest):
            k, _, v = part.partition(":")
            params[k] = v
        q = {"n": params.get("n", "1")}
        if "f" in params: q["f"] = params["f"]
        if "c" in params: q["c"] = params["c"]
        url = f"file://{tmp}?{urllib.parse.urlencode(q)}"
        png = out / f"{name}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1280,720", "--virtual-time-budget=15000",
                        f"--screenshot={png}", url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        print("wrote", png)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
