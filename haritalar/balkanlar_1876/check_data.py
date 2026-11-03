#!/usr/bin/env python3
"""data/*.json küme verisini denetler: koordinat kara/bölge dışında mı,
paylar toplamı, aşırı/eksik yarıçap, bölge içi kapsanmayan alanlar."""
import sys
import numpy as np
import shapely
from shapely.geometry import Point

import render as R


def main(paths=None):
    cl = R.load_clusters(paths)
    countries = R.ne_layer("countries")
    region = shapely.make_valid(R.data_region(countries))
    xs, ys = R.TO_XY.transform([c["lon"] for c in cl], [c["lat"] for c in cl])
    bad = 0
    for c, x, y in zip(cl, xs, ys):
        p = Point(x, y)
        d = region.distance(p) / 1000
        tot = c["turk"] + c["muslim_other"] + c["christian"]
        msg = []
        if d > 3:
            msg.append(f"bölge/kara dışında ({d:.0f} km)")
        if abs(tot - 100) > 2:
            msg.append(f"pay toplamı {tot}")
        if not (2 <= c["radius_km"] <= 45):
            msg.append(f"yarıçap {c['radius_km']}")
        if msg:
            bad += 1
            print(f"[{c['src']}] {c['name']} ({c['lat']:.2f},{c['lon']:.2f}): " + "; ".join(msg))
    # kapsama: bölge içindeki 5 km ızgarada en yakın normalize mesafe
    x0, x1, y0, y1 = R.frame()
    gx, gy = np.meshgrid(np.arange(x0, x1, 5000), np.arange(y0, y1, 5000))
    inside = shapely.contains_xy(region, gx.ravel(), gy.ravel())
    px, py = gx.ravel()[inside], gy.ravel()[inside]
    cx, cy = np.asarray(xs), np.asarray(ys)
    r = np.array([c["radius_km"] for c in cl]) * 1000
    q = np.min(np.hypot(px[:, None] - cx[None], py[:, None] - cy[None]) / r[None], axis=1)
    gap = q > 1.6
    print(f"{len(cl)} küme, {bad} sorunlu; bölge içi kapsanmayan alan: %{100 * gap.mean():.1f}")
    if gap.any():
        lon, lat = R.Transformer.from_crs(R.CRS, "EPSG:4326", always_xy=True).transform(px[gap], py[gap])
        # boşlukları 0.5° hücrelerde özetle
        cells = {}
        for a, b in zip(lon, lat):
            k = (round(b * 2) / 2, round(a * 2) / 2)
            cells[k] = cells.get(k, 0) + 1
        for (b, a), n in sorted(cells.items(), key=lambda t: -t[1])[:25]:
            print(f"  boşluk ~ lat {b:.1f} lon {a:.1f}: {n * 25} km²")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
