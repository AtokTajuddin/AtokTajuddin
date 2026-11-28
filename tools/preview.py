#!/usr/bin/env python3
"""Pratinjau README di localhost dengan tampilan mirip halaman profil GitHub.

README dirender ulang di setiap request, jadi cukup refresh browser setelah
mengubah README.md atau menjalankan ulang generator aset.

Pakai:  python3 tools/preview.py [port]   lalu buka http://127.0.0.1:8765

Varian alternatif ada di variants/<nama>/README.md dan dilayani di /<nama>/.
"""

import http.server
import os
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARIANTS_DIR = os.path.join(ROOT, "variants")
RAW_OUTPUT = "https://raw.githubusercontent.com/AtokTajuddin/AtokTajuddin/output/"


def variants():
    if not os.path.isdir(VARIANTS_DIR):
        return []
    return sorted(d for d in os.listdir(VARIANTS_DIR) if os.path.isfile(os.path.join(VARIANTS_DIR, d, "README.md")))

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AtokTajuddin · README preview</title>
<style>
:root{--bg:#0d1117;--fg:#e6edf3;--muted:#9198a1;--border:#3d444d;--box:#0d1117;--chip:#151b23}
:root[data-theme=light]{--bg:#ffffff;--fg:#1f2328;--muted:#59636e;--border:#d1d9e0;--box:#ffffff;--chip:#f6f8fa}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif}
.top{height:64px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 24px;background:var(--chip)}
.top b{font-weight:600}
.nav{display:flex;gap:4px;flex-wrap:wrap}.nav a{color:var(--muted);text-decoration:none;padding:4px 10px;border-radius:6px;font-size:13px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.nav a[aria-current]{color:var(--fg);background:var(--bg);box-shadow:0 0 0 1px var(--border)}
.toggle{display:flex;gap:4px;border:1px solid var(--border);border-radius:8px;padding:3px}
.toggle button{all:unset;cursor:pointer;padding:4px 12px;border-radius:6px;color:var(--muted);font-size:13px}
.toggle button[aria-pressed=true]{background:var(--bg);color:var(--fg);box-shadow:0 0 0 1px var(--border)}
.wrap{max-width:1280px;margin:0 auto;padding:32px 24px;display:flex;gap:24px}
aside{width:296px;flex:none}
.avatar{width:296px;height:296px;border-radius:50%;border:1px solid var(--border);display:grid;place-items:center;font-size:84px;font-weight:600;color:var(--muted);background:var(--chip)}
aside h1{margin:16px 0 0;font-size:24px;line-height:1.25;font-weight:600}
aside .login{font-size:20px;font-weight:300;color:var(--muted)}
aside .follow{margin-top:16px;border:1px solid var(--border);border-radius:6px;text-align:center;padding:5px;font-weight:500;background:var(--chip)}
main{flex:1;min-width:0}
.box{border:1px solid var(--border);border-radius:6px;background:var(--box);padding:24px}
.box .crumb{font-size:12px;color:var(--muted);margin-bottom:16px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.md p{margin:0 0 16px}
.md img{max-width:100%;box-sizing:content-box;vertical-align:middle}
.md a{color:#4493f8;text-decoration:none}
.md sub{font-size:85%;color:var(--muted)}
@media (max-width:1012px){aside{display:none}}
</style></head>
<body>
<div class="top"><nav class="nav">%NAV%</nav>
<div class="toggle"><button data-t="auto">Auto</button><button data-t="dark">Dark</button><button data-t="light">Light</button></div></div>
<div class="wrap">
<aside><div class="avatar">AT</div><h1>Atok Tajuddin</h1><div class="login">AtokTajuddin</div><div class="follow">Follow</div></aside>
<main><div class="box"><div class="crumb">AtokTajuddin / README.md &middot; %NAME%</div><article class="md">
%README%
</article></div></main></div>
<script>
const pics=[...document.querySelectorAll('picture')].map(p=>({p,img:p.querySelector('img'),src:[...p.querySelectorAll('source')].map(s=>({s,media:s.media,srcset:s.srcset}))}));
function apply(mode){
  const sys=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
  const eff=mode==='auto'?sys:mode;
  document.documentElement.dataset.theme=eff;
  for(const {img,src} of pics){
    const hit=src.find(x=>x.media.includes(eff));
    for(const x of src){x.s.media=x.media;}
    if(mode!=='auto'&&hit){for(const x of src){x.s.media='not all';} img.src=hit.srcset;}
  }
  document.querySelectorAll('.toggle button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.t===mode));
  try{localStorage.setItem('readme-theme',mode)}catch(e){}
}
document.querySelectorAll('.toggle button').forEach(b=>b.onclick=()=>apply(b.dataset.t));
let saved='auto';try{saved=localStorage.getItem('readme-theme')||'auto'}catch(e){}
const q=new URLSearchParams(location.search).get('theme');if(q)saved=q;
apply(saved);
// ?still=detik: ganti <img> dengan iframe SVG dan bekukan animasinya di detik itu (cek keadaan akhir)
const still=new URLSearchParams(location.search).get('still');
if(still!==null){addEventListener('load',()=>{Promise.all([...document.querySelectorAll('.md img')].map(img=>new Promise(ok=>{
  const f=document.createElement('iframe');const r=img.getBoundingClientRect();
  f.style.cssText=`width:${r.width}px;height:${r.height}px;border:0;vertical-align:middle;background:transparent`;f.setAttribute('allowtransparency','true');
  f.onload=()=>{const sv=f.contentDocument.documentElement;sv.setAttribute('width','100%');sv.setAttribute('height','100%');
    try{sv.pauseAnimations();sv.setCurrentTime(+still)}catch(e){};ok()};
  f.src=img.currentSrc||img.src;(img.closest('picture')||img).replaceWith(f);}))).then(()=>document.title='ready')});}
</script>
</body></html>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def render(self, md_path, name):
        with open(md_path, encoding="utf-8") as f:
            body = markdown.markdown(f.read(), extensions=["tables", "fenced_code"])
        links = [("/", "bento")] + [("/%s/" % v, v) for v in variants()]
        nav = "".join('<a href="%s"%s>%s</a>' % (h, " aria-current=page" if n == name else "", n) for h, n in links)
        # snake ada di branch output; di preview disajikan dari salinan lokal tools/.preview-cache/
        body = body.replace(RAW_OUTPUT, "/_output/")
        data = PAGE.replace("%README%", body).replace("%NAV%", nav).replace("%NAME%", name).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return self.render(os.path.join(ROOT, "README.md"), "bento")
        parts = path.strip("/").split("/")
        if parts[0] == "_output":
            self.path = "/tools/.preview-cache/" + "/".join(parts[1:])
            return super().do_GET()
        if parts[0] in variants():
            if len(parts) == 1:
                if not path.endswith("/"):
                    self.send_response(301)
                    self.send_header("Location", path + "/")
                    self.end_headers()
                    return
                return self.render(os.path.join(VARIANTS_DIR, parts[0], "README.md"), parts[0])
            self.path = "/variants/" + "/".join(parts)
        super().do_GET()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print("preview: http://127.0.0.1:%d" % port)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
