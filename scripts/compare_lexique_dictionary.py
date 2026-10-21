#!/usr/bin/env python3
"""Compare a dictionary extraction with the project lexicon without importing data.

The report is deliberately review-only: it preserves each source row and its
provenance, flags existing lemmas for enrichment/merging, and marks absent
lemmas as candidates requiring linguistic review. It never edits the lexicon.
"""
from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path

PROJECT_COLUMNS = {"id", "soninke", "francais", "categorie", "source", "statut"}
SOURCE_COLUMNS = {
    "lemme", "variante", "glose_extraite_automatiquement",
    "texte_source", "paragraphe_source", "source",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "")
    return re.sub(r"\s+", " ", value.strip()).casefold()


def read_csv(path: Path, delimiter: str) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=delimiter)
        rows = list(reader)
        columns = set(reader.fieldnames or [])
    return rows, sorted(columns)


def compare(project_path: Path, source_path: Path, output_path: Path) -> tuple[int, int]:
    project_rows, project_columns = read_csv(project_path, ";")
    source_rows, source_columns = read_csv(source_path, ",")
    missing_project = PROJECT_COLUMNS - set(project_columns)
    missing_source = SOURCE_COLUMNS - set(source_columns)
    if missing_project:
        raise ValueError(f"Colonnes manquantes dans le lexique projet: {', '.join(sorted(missing_project))}")
    if missing_source:
        raise ValueError(f"Colonnes manquantes dans l'extraction: {', '.join(sorted(missing_source))}")

    project_by_lemma: dict[str, list[dict[str, str]]] = {}
    for row in project_rows:
        key = normalize(row.get("soninke", ""))
        if key:
            project_by_lemma.setdefault(key, []).append(row)

    source_counts = Counter(normalize(row.get("lemme", "")) for row in source_rows)
    report_fields = [
        "decision_provisoire", "lemme", "variante", "glose_extraite_automatiquement",
        "texte_source", "paragraphe_source", "source", "occurrences_lemme_dans_source",
        "ids_projet_correspondants", "traductions_projet_existantes", "consigne",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=report_fields, delimiter=";")
        writer.writeheader()
        for row in source_rows:
            lemma = row.get("lemme", "")
            key = normalize(lemma)
            matches = project_by_lemma.get(key, [])
            if matches:
                decision = "LEMME_EXISTANT_A_ENRICHIR_OU_FUSIONNER"
                ids = " | ".join(item.get("id", "") for item in matches)
                translations = " | ".join(item.get("francais", "") for item in matches)
                note = "Ne pas créer une deuxième fiche; examiner sens, variante et exemple puis enrichir la fiche existante."
            else:
                decision = "LEMME_CANDIDAT_NOUVEAU_A_VALIDER"
                ids = ""
                translations = ""
                note = "Candidat seulement; vérifier la graphie, les renvois « See main entry » et la validité linguistique avant import."
            writer.writerow({
                "decision_provisoire": decision,
                "lemme": lemma,
                "variante": row.get("variante", ""),
                "glose_extraite_automatiquement": row.get("glose_extraite_automatiquement", ""),
                "texte_source": row.get("texte_source", ""),
                "paragraphe_source": row.get("paragraphe_source", ""),
                "source": row.get("source", ""),
                "occurrences_lemme_dans_source": source_counts[key],
                "ids_projet_correspondants": ids,
                "traductions_projet_existantes": translations,
                "consigne": note,
            })
    return len(source_rows), sum(1 for row in source_rows if normalize(row.get("lemme", "")) in project_by_lemma)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="CSV du lexique projet, séparateur ;")
    parser.add_argument("--source", type=Path, required=True, help="CSV extrait du dictionnaire, séparateur ,")
    parser.add_argument("--output", type=Path, default=Path("build/revue-enrichissement-soninke.csv"))
    args = parser.parse_args()
    try:
        rows, existing = compare(args.project, args.source, args.output)
    except (OSError, csv.Error, ValueError) as exc:
        parser.error(str(exc))
    print(f"Rapport créé: {args.output} — {rows} lignes source, {existing} lignes associées à un lemme déjà présent.")
    print("Aucune entrée du lexique projet n'a été modifiée.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
