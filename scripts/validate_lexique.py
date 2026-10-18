#!/usr/bin/env python3
"""Validate the Soninke–French lexical CSV without changing source spellings."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REQUIRED_COLUMNS = {"id", "soninke", "francais", "categorie", "source", "statut"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            columns = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - columns
            if missing:
                return [f"Colonnes manquantes: {', '.join(sorted(missing))}"]

            seen_ids: set[str] = set()
            seen_pairs: dict[tuple[str, str], int] = {}
            count = 0
            for line_number, row in enumerate(reader, start=2):
                count += 1
                for column in REQUIRED_COLUMNS:
                    if not (row.get(column) or "").strip():
                        errors.append(f"Ligne {line_number}: champ vide « {column} »")

                entry_id = (row.get("id") or "").strip()
                if entry_id in seen_ids:
                    errors.append(f"Ligne {line_number}: identifiant dupliqué « {entry_id} »")
                seen_ids.add(entry_id)

                pair = ((row.get("soninke") or "").strip(), (row.get("categorie") or "").strip())
                if pair in seen_pairs:
                    # Duplicate forms can be legitimate across categories or sources.
                    # Warn only when the same form and category repeat; do not auto-delete.
                    errors.append(
                        f"Ligne {line_number}: forme/catégorie répétée {pair!r} "
                        f"(première ligne {seen_pairs[pair]}); vérifier sans supprimer automatiquement"
                    )
                else:
                    seen_pairs[pair] = line_number

            if count == 0:
                errors.append("Aucune entrée de données.")
    except OSError as exc:
        return [f"Impossible de lire {path}: {exc}"]
    except csv.Error as exc:
        return [f"Erreur CSV: {exc}"]

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/lexique-soninke-fr-base.csv")
    errors = validate(path)
    if errors:
        print(f"Contrôle terminé avec {len(errors)} remarque(s)/erreur(s) :")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK — fichier valide : {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
