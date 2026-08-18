#!/usr/bin/env python3
"""Prepare small, frozen datasets used by the Fall 2026 homework notebooks.

The script intentionally separates one-time instructor data preparation from
student notebook execution.  It downloads official/public source snapshots,
reduces them to the columns needed by the assignments, records provenance, and
writes deterministic CSV files under ``lecturebook/data/homework``.
"""

from __future__ import annotations

import hashlib
import io
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "lecturebook" / "data"
OUT = DATA / "homework"
RETRIEVED = "2026-08-17"
EXPECTED_SHA256 = {
    "hw02_bh_curves.csv": "e6f152fe81c94abff46da59a0bb50804a7d620b455dc8d80502a9d280ea011ca",
    "hw04_southern_california_earthquakes.csv": "a4e7fb0d2a99fc81cf0f309e13a853b6025413e84d61ab82f18cc8c43ec37072",
    "hw05_stress_strain.csv": "47eae40e4dd333f3e582e836d6b5995c440cfb633aaf5ad6a7b56f54125da41b",
    "hw06_steel_plate_faults.csv": "e180d3fba194926e14b8a968a9d4e96a529fc1083a255d6c933725fff3c0c01a",
    "hw11_airfoil_self_noise.csv": "7e11e5f828924249f00f60419b42bb31039460d9197541c62e4eb90b0031bb60",
    "hw13_challenger_prelaunch.csv": "126230dfcaefd987249d34f48759714614121793e7430db586cbe0a3df535357",
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Purdue-ME539-course-materials/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(frame: pd.DataFrame, name: str) -> Path:
    path = OUT / name
    payload = frame.to_csv(
        index=False, lineterminator="\n", float_format="%.12g"
    ).encode("utf-8")
    actual = hashlib.sha256(payload).hexdigest()
    expected = EXPECTED_SHA256[name]
    if actual != expected:
        raise RuntimeError(
            f"Refusing to overwrite frozen {name}: expected SHA-256 "
            f"{expected}, but refreshed data produced {actual}. Review the "
            "upstream change and deliberately update the snapshot metadata."
        )
    path.write_bytes(payload)
    return path


def prepare_bh_curves() -> Path:
    raw = np.loadtxt(DATA / "B_data.csv")
    assert raw.shape == (200, 1500) and np.isfinite(raw).all()
    # Keep every curve and every tenth recorded field point.  The source file
    # does not contain physical H values, so the assignment uses a normalized
    # acquisition coordinate rather than inventing units.
    reduced = raw[:, ::10]
    columns = [f"u_{j:03d}" for j in range(reduced.shape[1])]
    frame = pd.DataFrame(reduced, columns=columns)
    frame.insert(0, "sample_id", np.arange(reduced.shape[0], dtype=int))
    return write_csv(frame, "hw02_bh_curves.csv")


def prepare_earthquakes() -> Path:
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
        "&starttime=1900-01-01&endtime=2026-01-01"
        "&minlatitude=32&maxlatitude=37&minlongitude=-122&maxlongitude=-114"
        "&minmagnitude=6.5&orderby=time-asc"
    )
    frame = pd.read_csv(io.BytesIO(fetch(url)))
    keep = ["time", "latitude", "longitude", "depth", "mag", "place", "id"]
    frame = frame.loc[:, keep].sort_values("time", kind="stable")
    assert len(frame) == 18 and frame["id"].is_unique
    assert pd.to_numeric(frame["mag"]).ge(6.5).all()
    assert pd.to_numeric(frame["latitude"]).between(32, 37).all()
    assert pd.to_numeric(frame["longitude"]).between(-122, -114).all()
    return write_csv(frame, "hw04_southern_california_earthquakes.csv")


def prepare_stress_strain() -> Path:
    raw = np.loadtxt(DATA / "stress_strain.txt")
    assert raw.shape == (1001, 2) and np.isfinite(raw).all()
    assert np.all(np.diff(raw[:, 0]) > 0)
    frame = pd.DataFrame(
        {"strain": raw[:, 0], "stress_mpa": raw[:, 1]}
    )
    return write_csv(frame, "hw05_stress_strain.csv")


def prepare_steel_faults() -> Path:
    url = (
        "https://archive.ics.uci.edu/static/public/198/"
        "steel%2Bplates%2Bfaults.zip"
    )
    feature_names = [
        "X_Minimum", "X_Maximum", "Y_Minimum", "Y_Maximum",
        "Pixels_Areas", "X_Perimeter", "Y_Perimeter", "Sum_of_Luminosity",
        "Minimum_of_Luminosity", "Maximum_of_Luminosity",
        "Length_of_Conveyer", "TypeOfSteel_A300", "TypeOfSteel_A400",
        "Steel_Plate_Thickness", "Edges_Index", "Empty_Index",
        "Square_Index", "Outside_X_Index", "Edges_X_Index", "Edges_Y_Index",
        "Outside_Global_Index", "LogOfAreas", "Log_X_Index", "Log_Y_Index",
        "Orientation_Index", "Luminosity_Index", "SigmoidOfAreas",
    ]
    target_names = [
        "Pastry", "Z_Scratch", "K_Scatch", "Stains", "Dirtiness", "Bumps",
        "Other_Faults",
    ]
    archive = zipfile.ZipFile(io.BytesIO(fetch(url)))
    member = next(name for name in archive.namelist() if name.endswith("Faults.NNA"))
    frame = pd.read_csv(
        archive.open(member), sep=r"\s+", header=None,
        names=feature_names + target_names,
    )
    assert frame.shape == (1941, 34)
    assert frame[target_names].isin([0, 1]).all().all()
    assert frame[target_names].sum(axis=1).eq(1).all()
    target = frame[target_names].idxmax(axis=1)
    result = frame[feature_names].copy()
    result["fault_type"] = target
    return write_csv(result, "hw06_steel_plate_faults.csv")


def prepare_airfoil() -> Path:
    url = (
        "https://archive.ics.uci.edu/static/public/291/"
        "airfoil%2Bself%2Bnoise.zip"
    )
    archive = zipfile.ZipFile(io.BytesIO(fetch(url)))
    member = next(
        name for name in archive.namelist()
        if name.lower().endswith("airfoil_self_noise.dat")
    )
    columns = [
        "frequency_hz", "angle_of_attack_deg", "chord_length_m",
        "free_stream_velocity_mps", "displacement_thickness_m",
        "sound_pressure_db",
    ]
    frame = pd.read_csv(archive.open(member), sep=r"\s+", header=None, names=columns)
    assert frame.shape == (1503, 6) and np.isfinite(frame.to_numpy()).all()
    return write_csv(frame, "hw11_airfoil_self_noise.csv")


def prepare_challenger() -> Path:
    frame = pd.read_csv(DATA / "challenger_data.csv", skipinitialspace=True)
    temperature = pd.to_numeric(frame["Temperature"], errors="coerce")
    incident = pd.to_numeric(frame["Damage Incident"], errors="coerce")
    result = pd.DataFrame(
        {"temperature_f": temperature, "damage_incident": incident}
    ).dropna()
    result["damage_incident"] = result["damage_incident"].astype(int)
    assert len(result) == 23
    assert result["damage_incident"].isin([0, 1]).all()
    return write_csv(result.reset_index(drop=True), "hw13_challenger_prelaunch.csv")


def write_sources(paths: list[Path]) -> None:
    by_name = {path.name: sha256(path) for path in paths}
    text = f"""# Homework data provenance

Frozen snapshots prepared on {RETRIEVED}.  Student notebooks load these local
files first and use the course GitHub copy only as a Google Colab fallback.

| File | Source and preparation | License/status | SHA-256 |
|---|---|---|---|
| `hw02_bh_curves.csv` | Reduced from the legacy course file `lecturebook/data/B_data.csv`: all 200 curves and every tenth recorded point. The source contains no physical applied-field coordinates, so the notebook uses a normalized acquisition coordinate. | Existing course asset; original provenance/license should be confirmed before redistribution outside this course. | `{by_name['hw02_bh_curves.csv']}` |
| `hw04_southern_california_earthquakes.csv` | [USGS ComCat FDSN event query](https://earthquake.usgs.gov/fdsnws/event/1/), 1900-01-01 through 2025-12-31, magnitude at least 6.5, latitude 32--37 N and longitude 122--114 W. Selected columns only. | U.S. Government work/public domain; attribute USGS. Catalogs may be revised, hence this frozen snapshot. | `{by_name['hw04_southern_california_earthquakes.csv']}` |
| `hw05_stress_strain.csv` | Column-labeled copy of the legacy course file `lecturebook/data/stress_strain.txt`; strain is dimensionless and stress is MPa. | Existing course asset; molecular-dynamics data attributed in the legacy assignment to Alejandro Strachan's group. | `{by_name['hw05_stress_strain.csv']}` |
| `hw06_steel_plate_faults.csv` | [UCI Steel Plates Faults](https://doi.org/10.24432/C5J88N). All 27 predictors plus the derived seven-class label. | CC BY 4.0. | `{by_name['hw06_steel_plate_faults.csv']}` |
| `hw11_airfoil_self_noise.csv` | [UCI Airfoil Self-Noise](https://doi.org/10.24432/C5VW2C), with descriptive column names added and no row filtering. | CC BY 4.0. | `{by_name['hw11_airfoil_self_noise.csv']}` |
| `hw13_challenger_prelaunch.csv` | Numeric pre-launch rows from the legacy course file `lecturebook/data/challenger_data.csv`; the accident row with no damage observation is excluded. | Existing course teaching asset; trace the historical source before redistribution outside the course. | `{by_name['hw13_challenger_prelaunch.csv']}` |

Homework 7 does not use a redistributed course snapshot. Its notebook downloads
the [NIST Chwirut1 ASCII file](https://www.itl.nist.gov/div898/strd/nls/data/LINKS/DATA/Chwirut1.dat)
directly from NIST (accessed 2026-08-17) and requires SHA-256
`d9a055dfe5af71a8754c00f073ef00f8fed2e3fd1c6fd20cea8fd62d7cc3ed84`.
The data are from a NIST ultrasonic reference-block calibration study. NIST
does not provide an explicit redistribution license on the dataset page, so the
course records the official source and checksum without storing a copy.
"""
    # Use .txt so the classic Jupyter Book builder does not publish this
    # instructor provenance record as an unlisted HTML page.
    (OUT / "SOURCES.txt").write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        prepare_bh_curves(),
        prepare_earthquakes(),
        prepare_stress_strain(),
        prepare_steel_faults(),
        prepare_airfoil(),
        prepare_challenger(),
    ]
    write_sources(paths)
    for path in paths:
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
