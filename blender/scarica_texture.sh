#!/bin/sh
# Scarica le texture CC0 di Poly Haven usate dalla scena (2K, JPG).
cd "$(dirname "$0")/tex" || exit 1
for i in decrepit_wallpaper damaged_plaster grey_plaster white_plaster_02 terrazzo_tiles herringbone_parquet rough_linen fabric_pattern_07 painted_plaster_wall laminate_floor_02; do
  for m in diff nor_gl rough; do
    s=$m; [ "$m" = nor_gl ] && s=nor
    curl -sSf --retry 3 -C - -o "${i}_${s}.jpg" "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/${i}/${i}_${m}_2k.jpg" || true
  done
done
