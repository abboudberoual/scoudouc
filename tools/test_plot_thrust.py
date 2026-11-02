"""Run with:  python -m pytest tools/   (or just: python tools/test_plot_thrust.py)"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import plot_thrust as p


def synthetic():
    # flat 10 N for 1.0 s starting at t=0.5, sampled at 80 Hz, with quiet before and after. Impulse = 10 N·s.
    t = [i / 80 for i in range(240)]
    f = [10.0 if 0.5 <= x < 1.5 else 0.0 for x in t]
    return t, f


def test_metrics():
    t, f = synthetic()
    m = p.metrics(t, f)
    assert m["peak_n"] == 10.0
    assert abs(m["burn_s"] - 1.0) < 0.02
    assert abs(m["impulse_ns"] - 10.0) < 0.2


def test_load_skips_header_and_comments():
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
        fh.write("# IGNITION\ntime_s,thrust_n\n0.0,0.0\n0.1,5.0\n# END\n0.2,0.0\n")
    t, f = p.load(fh.name)
    os.unlink(fh.name)
    assert t == [0.0, 0.1, 0.2] and f == [0.0, 5.0, 0.0]


if __name__ == "__main__":
    test_metrics(); test_load_skips_header_and_comments(); print("ok")
