#!/usr/bin/env python3
"""Validate the Soninke–French lexical CSV and reject duplicate headwords.

Normalization is intentionally conservative: Unicode NFC, surrounding/repeated
whitespace, and letter case are normalized. Diacritics, apostrophes, and
hyphens are preserved so that potentially meaningful Soninke distinctions are
not silently erased.
"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from pathlib import Path

REQUIRED_COLUMNS = {"id", "soninke", "francais", "categorie", "source", "statut"}


def normalize_headword(value: str) -> str:
    """Return a comparison key without stripping linguistically meaningful marks."""
    value = unicodedata.normalize("NFC", value or "")
    value = re.sub(r"\s+", " ", value.strip())
    return value.casefold()


def validate(path: Path) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            columns = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - columns
            if missing:
                return [f"Colonnes manquantes: {', '.join(sorted(missing))}"], warnings, 0

            seen_ids: dict[str, int] = {}
            seen_headwords: dict[str, tuple[int, str]] = {}
            count = 0
            for line_number, row in enumerate(reader, start=2):
                count += 1
                for column in REQUIRED_COLUMNS:
                    if not (row.get(column) or "").strip():
                        errors.append(f"Ligne {line_number}: champ vide « {column} »")

                entry_id = (row.get("id") or "").strip()
                if entry_id in seen_ids:
                    errors.append(
                        f"Ligne {line_number}: identifiant dupliqué « {entry_id} » "
                        f"(première occurrence ligne {seen_ids[entry_id]})"
                    )
                else:
                    seen_ids[entry_id] = line_number

                raw_headword = (row.get("soninke") or "").strip()
                headword = normalize_headword(raw_headword)
                if headword:
                    if headword in seen_headwords:
                        first_line, first_spelling = seen_headwords[headword]
                        errors.append(
                            f"Ligne {line_number}: lemme soninké dupliqué "
                            f"« {raw_headword} » (première occurrence "
                            f"« {first_spelling} », ligne {first_line}). "
                            "Ne pas créer une seconde fiche : fusionner les sens "
                            "dans l'entrée existante ou examiner la variante avant import."
                        )
                    else:
                        seen_headwords[headword] = (line_number, raw_headword)

            if count == 0:
                errors.append("Aucune entrée de données.")
    except OSError as exc:
        return [f"Impossible de lire {path}: {exc}"], warnings, 0
    except csv.Error as exc:
        return [f"Erreur CSV: {exc}"], warnings, 0

    return errors, warnings, count


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/lexique-soninke-fr-base.csv")
    errors, warnings, count = validate(path)
    if errors:
        print(f"ÉCHEC — {len(errors)} erreur(s), {count} entrée(s) lue(s) :")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"AVERTISSEMENT — {warning}")
        return 1

    print(f"OK — {count} entrée(s) lue(s), aucun lemme dupliqué : {path}")
    for warning in warnings:
        print(f"AVERTISSEMENT — {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
