"""Build an assembly guide PDF.  Usage: python3 hardware/guides/build.py stand_v3

Looks for <name>_guide.py in this folder (it defines GUIDE), runs its optional make_figures(out_dir),
then renders every step and prints the PDF to hardware/guides/out/<name>/.
"""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import guide


def main(name):
    mod = importlib.import_module(f"{name}_guide")
    out = os.path.join(HERE, "out", name)
    os.makedirs(out, exist_ok=True)
    figs = importlib.import_module(f"{name}_figures") if os.path.exists(os.path.join(HERE, f"{name}_figures.py")) else None
    if figs:
        figs.make_figures(out)
    pdf = guide.build(mod.GUIDE, out)
    print(pdf)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "stand_v3")
