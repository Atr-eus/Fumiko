#!/usr/bin/bash

# INSTALL DEPTS
# if ! pacman -Q grim slurp imagemagick manga-ocr-git &> /dev/null; then
if ! pacman -Q grim slurp imagemagick &> /dev/null; then
  if command -v pacman &> /dev/null && command -v doas &> /dev/null; then
    printf "[WORKER] Installing required packages...\n\n"
  
    # doas pacman -S grim slurp imagemagick manga-ocr-git
    doas pacman -S grim slurp imagemagick
  else
    printf "[ERROR] doas and/or pacman not found, please install the dependencies manually. exitting..."
    exit 1
  fi
  else
    printf "[WORKER] Required packges are already installed.\n\n"
fi

# PARAMETERS
WEBLIVE="$PWD/index.html"
OUTFILE="$PWD/out.txt"
TEMPIMG="/tmp/fumiko-$(uuidgen).png"

# SAVE THE SCREENSHOT
grim -g "$(slurp -d)" "$TEMPIMG" || exit 1;

# RUN MANGA-OCR ON THE TAKEN SS
out="$(manga_ocr "$TMPIMG" || python -m manga_ocr "$TMPIMG" || true)"
out="$(echo "$text" | sed '/^\s*$/d')"

# printf "$out"
# WRITE OUTPUT TEXT TO FILE (TO BE SERVED BY A WEB SERVER)
tmpout="$(mktemp "${OUTFILE}.tmp.XXXXXX")"
printf '%s\n' "$text" > "$tmpout"
mv "$tmpout" "$OUTFILE"
