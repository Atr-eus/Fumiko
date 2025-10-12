#!/usr/bin/python3

import subprocess
import os
import sys
import tempfile
from argparse import ArgumentParser
from datetime import datetime

OUT_FILE = "out.txt"


def slurp():
    """Run slurp and return geometry string (stdout stripped)."""

    try:
        res = subprocess.run(
            ["slurp", "-d"], capture_output=True, text=True, check=True
        )
        gm = res.stdout.strip()

        if not gm:
            raise RuntimeError("slurp returned empty geometry")
        return gm
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"slurp failed: {e.stderr or e}") from e
    except FileNotFoundError:
        raise RuntimeError("slurp not found. Install slurp and run under Wayland.")


def grim(gm, out_path):
    """Run grim with geometry returned by slurp to save screenshot to out_path."""

    try:
        subprocess.run(["grim", "-g", gm, out_path], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"grim failed: {e}") from e
    except FileNotFoundError:
        raise RuntimeError(
            "grim not found. Install grim to capture Wayland screenshots."
        )


def ocr(image_path):
    """OCR using MangaOcr."""

    try:
        from manga_ocr import MangaOcr

        mocr = MangaOcr()
        out = mocr(image_path)

        print(f"\033[92m[{datetime.now()}]", end=" ")
        print("\033[96m" + out)
        return out
    except Exception as e:
        raise RuntimeError(f"manga-ocr failure: {e}") from e


def write_output(out_path, txt):
    tmp = out_path + ".tmp"

    with open(tmp, "w", encoding="utf-8") as f:
        f.write(txt)
    os.replace(tmp, out_path)


def main():
    parser = ArgumentParser(
        description="Select region -> capture -> OCR -> write out.txt"
    )
    parser.add_argument(
        "--out", "-o", default="out.txt", help="Output text file (default: out.txt)"
    )
    args = parser.parse_args()

    try:
        gm = slurp()
    except Exception as e:
        print(f"[ERROR] slurp: {e}", file=sys.stderr)
        sys.exit(2)

    tmpf = tempfile.NamedTemporaryFile(prefix="fumiko-", suffix=".png", delete=False)
    img_path = tmpf.name
    tmpf.close()

    try:
        grim(gm, img_path)
    except Exception as e:
        print(f"[ERROR] grim: {e}", file=sys.stderr)

        if not args.img and os.path.exists(img_path):
            try:
                os.unlink(img_path)
            except:
                pass
        sys.exit(3)

    ocr_txt = ""
    try:
        ocr_txt = ocr(img_path)
    except Exception as imp_err:
        print("[ERROR] OCR failed (import):", file=sys.stderr)
        print(str(imp_err), file=sys.stderr)

        print(f"[INFO] Captured image kept at: {img_path}", file=sys.stderr)
        sys.exit(4)

    if ocr_txt is None:
        ocr_txt = ""
    ocr_txt_lines = [line.rstrip() for line in ocr_txt.splitlines()]

    while ocr_txt_lines and ocr_txt_lines[0].strip() == "":
        ocr_txt_lines.pop(0)
    while ocr_txt_lines and ocr_txt_lines[-1].strip() == "":
        ocr_txt_lines.pop()
    final_txt = "\n".join(ocr_txt_lines)

    try:
        write_output(args.out, final_txt)
    except Exception as e:
        print(f"[ERROR] writing {args.out}: {e}", file=sys.stderr)
        sys.exit(5)

    try:
        import socket

        sock = socket.socket()
        sock.settimeout(0.5)
        try:
            sock.connect(("127.0.0.1", 8765))
            sock.close()
            subprocess.Popen(
                ["xdg-open", "http://127.0.0.1:8765/"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass
    except Exception:
        pass


if __name__ == "__main__":
    main()
