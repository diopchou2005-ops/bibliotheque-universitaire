import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
CSV_FILE = BASE / "data" / "benchmark.csv"
OUT_DIR = BASE / "graphs"
OUT_DIR.mkdir(exist_ok=True)


def load_data():
    data = {"insertion": {}, "recherche": {}, "tri": {}}
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            op = row["operation"]
            profile = row["profile"]
            structure = row["structure"]
            n = int(row["n"])
            mean = float(row["mean_ms"])
            std = float(row["std_ms"])
            data.setdefault(op, {}).setdefault(profile, {}).setdefault(structure, []).append((n, mean, std))
    return data


def average_points(points):
    xs = sorted({n for n, _, _ in points})
    ys = []
    errs = []
    for n in xs:
        vals = [m for (nn, m, _) in points if nn == n]
        stds = [s for (nn, _, s) in points if nn == n]
        ys.append(sum(vals) / len(vals))
        errs.append(sum(stds) / len(stds))
    return xs, ys, errs


def plot_structure_comparison(op, title):
    data = load_data()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ordered_structures = ("statique", "dynamique", "liste_chainee")
    structure_labels = {
        "statique": "Tableau statique",
        "dynamique": "Tableau dynamique",
        "liste_chainee": "Liste chaînée",
    }
    style_map = {
        "statique": {"marker": "o", "linestyle": "-", "color": "#1f77b4"},
        "dynamique": {"marker": "s", "linestyle": "--", "color": "#ff7f0e"},
        "liste_chainee": {"marker": "^", "linestyle": ":", "color": "#2ca02c"},
    }

    for structure in ordered_structures:
        all_points = []
        for profile in ("uniforme", "gaussienne", "tri"):
            all_points.extend(data.get(op, {}).get(profile, {}).get(structure, []))

        if not all_points:
            continue

        xs, ys, errs = average_points(all_points)
        style = style_map.get(structure, {})
        ax.errorbar(
            xs,
            ys,
            yerr=errs,
            marker=style.get("marker", "o"),
            linestyle=style.get("linestyle", "-"),
            color=style.get("color"),
            linewidth=1.8,
            label=structure_labels.get(structure, structure),
            capsize=3,
            elinewidth=1.0,
        )

    ax.set_title(f"Comparaison des structures — {title}")
    ax.set_xlabel("Nombre d’ouvrages n")
    ax.set_ylabel("Temps moyen (ms)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"{op}_comparison.png", dpi=150)
    plt.close(fig)


def plot_profile_comparison(op, title):
    data = load_data()
    for profile in ("uniforme", "gaussienne", "tri"):
        fig, ax = plt.subplots(figsize=(9, 5.5))

        ordered_structures = ("statique", "dynamique", "liste_chainee")
        structure_labels = {
            "statique": "Tableau statique",
            "dynamique": "Tableau dynamique",
            "liste_chainee": "Liste chaînée",
        }
        style_map = {
            "statique": {"marker": "o", "linestyle": "-", "color": "#1f77b4"},
            "dynamique": {"marker": "s", "linestyle": "--", "color": "#ff7f0e"},
            "liste_chainee": {"marker": "^", "linestyle": ":", "color": "#2ca02c"},
        }

        for structure in ordered_structures:
            points = data.get(op, {}).get(profile, {}).get(structure, [])
            if not points:
                continue
            xs, ys, errs = average_points(points)
            style = style_map.get(structure, {})
            ax.errorbar(
                xs,
                ys,
                yerr=errs,
                marker=style.get("marker", "o"),
                linestyle=style.get("linestyle", "-"),
                color=style.get("color"),
                linewidth=1.8,
                label=structure_labels.get(structure, structure),
                capsize=3,
                elinewidth=1.0,
            )

        ax.set_title(f"{title} — profil {profile}")
        ax.set_xlabel("Nombre d’ouvrages n")
        ax.set_ylabel("Temps moyen (ms)")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=9)
        fig.tight_layout()
        fig.savefig(OUT_DIR / f"{op}_{profile}.png", dpi=150)
        plt.close(fig)


if __name__ == "__main__":
    for op, title in [
        ("insertion", "Insertion"),
        ("recherche", "Recherche"),
        ("tri", "Tri"),
    ]:
        plot_structure_comparison(op, title)
        plot_profile_comparison(op, title)
    print("Courbes generees dans", OUT_DIR)
