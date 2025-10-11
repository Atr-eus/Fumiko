#!/usr/bin/bash

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
