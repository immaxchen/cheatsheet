import os
import re
from html import unescape
from pathlib import Path
from subprocess import PIPE, run

root = ".test"
pmap = {"py": "python", "perl": "perl", "bash": "bash", "php": "php", "js": "node"}
cptn = re.compile(
    """<file>(?P<file>.+?)</file>
<pre><code class="lang-(?P<lang>.+?)">(?P<code>.+?)</code></pre>""",
    re.DOTALL,
)
sptn = re.compile(
    """<file>(?P<file>.+?)</file>
<pre><code class="lang-(?P<lang>.+?)">(?P<code>.+?)</code></pre>
<samp><div>(?P<samp>.*?)</div></samp>""",
    re.DOTALL,
)


def make_code(code):
    file = code["file"]
    lang = code["lang"]
    code = code["code"]
    if file != "shell":
        fdir = os.path.dirname(file)
        Path(root, fdir).mkdir(parents=True, exist_ok=True)
        Path(root, file).write_text(unescape(code))


def make_samp(samp):
    file = samp["file"]
    lang = samp["lang"]
    code = samp["code"]
    samp = samp["samp"]
    prog = pmap[lang]
    args = (
        re.sub(r"^\$ ", "", code) if file == "shell" else [prog, str(Path(root, file))]
    )
    result = run(args, stdout=PIPE).stdout.decode().replace("\r", "").rstrip()
    expect = unescape(samp)
    if result == expect:
        global pcnt
        pcnt += 1
        print("pass")
    else:
        print("[result]\n", result, "\n[expect]\n", expect)


fcnt = tcnt = pcnt = 0
for pchap in [d for d in Path().iterdir() if d.is_dir()]:
    for pfile in pchap.glob("**/*.html"):
        print(f"================== {pfile} ".ljust(78, "="))
        fcnt += 1
        content = pfile.read_text()
        codes = [m.groupdict() for m in cptn.finditer(content)]
        samps = [m.groupdict() for m in sptn.finditer(content)]
        for code in codes:
            make_code(code)
        for samp in samps:
            tcnt += 1
            make_samp(samp)
print(f"\npassed {pcnt} tests, total {tcnt} tests collected in {fcnt} files.\n")
