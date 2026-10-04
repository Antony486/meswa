#!/usr/bin/env python3
"""
Makes the name box on the first screen compulsory.
Run once, in the same folder as index.html:   python force_name.py
(A backup is saved as index.html.bak)
"""
import shutil, sys
from pathlib import Path

f = Path(__file__).resolve().parent / "index.html"
s = f.read_text(encoding="utf-8")
if "needName" in s:
    sys.exit("Already patched - nothing to do.")

OLD = """if(g)g.onclick=function(e){e.stopPropagation();var n=document.getElementById("nm");if(n&&n.value.trim()){name=n.value.trim().slice(0,24);try{localStorage.setItem("mn",name)}catch(x){}}next()};"""
NEW = """if(g)g.onclick=function(e){e.stopPropagation();var n=document.getElementById("nm"); /*needName*/
 if(n){var v=n.value.trim();
  if(v.length<2){n.classList.remove("shake");void n.offsetWidth;n.style.animationDelay="0s";n.classList.add("shake");n.placeholder="Please type your name to continue 💚";n.focus();return}
  name=v.slice(0,24);try{localStorage.setItem("mn",name)}catch(x){}}
 next()};
var nb=document.getElementById("nm");if(nb&&g)nb.onkeydown=function(e){if(e.key=="Enter")g.click()};"""
CSS = """.slide>input.shake{animation:shake .4s forwards;border-color:#ff7eb3}
@keyframes shake{0%,100%{opacity:1;transform:none}25%{opacity:1;transform:translateX(-9px)}75%{opacity:1;transform:translateX(9px)}}
</style>"""

if s.count(OLD) != 1 or s.count("</style>") != 1:
    sys.exit("Couldn't find the expected code - index.html was edited too much. Send it to Claude to patch.")

shutil.copy2(f, f.with_name("index.html.bak"))
f.write_text(s.replace(OLD, NEW).replace("</style>", CSS), encoding="utf-8")
print("Done. The name is now compulsory (min 2 characters, Enter key works too).")
