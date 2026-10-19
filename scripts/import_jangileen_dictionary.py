#!/usr/bin/env python3
"""Import the public French–Wolof dictionary pages from Jàngileen.

The site's legal page says the dictionary data (words, translations and examples)
may be redistributed and modified. This script keeps per-entry source URLs and
does not fetch images, courses or other non-dictionary site content.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import re
import sys
import time
import unicodedata
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

BASE = "https://jangileen.kalam-alami.net"
USER_AGENT = "Soninke-TTS-Libre-dictionary-import/1.0 (open-source educational project)"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "entry"


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with urlopen(request, timeout=25) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {url}")
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


class DictionaryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: list[dict] = []
        self.entry: dict | None = None
        self.meaning: dict | None = None
        self.example: dict | None = None
        self.stack: list[tuple[str, set[str], dict[str, str]]] = []
        self.anchor: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        classes = set(attr.get("class", "").split())
        if "definition__container" in classes:
            self.entry = {"headword": "", "sourcePath": "", "meanings": []}
        if self.entry is not None and "definition-meaning" in classes:
            self.meaning = {"partOfSpeech": "", "translations": [], "comment": "", "examples": []}
        if self.meaning is not None and "definition-example" in classes:
            self.example = {"fr": "", "wolof": ""}
        ancestor_classes = set().union(*(item[1] for item in self.stack)) if self.stack else set()
        if self.meaning is not None and tag == "abbr" and "definition__term-type" in ancestor_classes:
            self.meaning["partOfSpeech"] = attr.get("title", "").strip()
        if tag == "a" and self.entry is not None:
            href = attr.get("href", "")
            if "definition__term" in ancestor_classes and "definition-meaning" not in ancestor_classes:
                self.entry["sourcePath"] = href
                self.anchor = {"kind": "headword", "text": ""}
            elif "/dictionary/word/wo/" in href and self.meaning is not None:
                self.anchor = {"kind": "translation", "text": ""}
        self.stack.append((tag, classes, attr))

    def handle_data(self, data: str) -> None:
        if not self.stack:
            return
        text = data.strip()
        if not text:
            return
        classes = set().union(*(item[1] for item in self.stack))
        if self.entry is not None and "definition__term" in classes and "definition-meaning" not in classes:
            self.entry["headword"] += text
        if self.anchor is not None:
            self.anchor["text"] += text
        if self.meaning is not None:
            if "definition__term-comment" in classes:
                self.meaning["comment"] += text
            if self.example is not None and "definition-example__translation" in classes:
                self.example["fr"] += text
            if self.example is not None and "definition-example__original" in classes:
                self.example["wolof"] += text

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        top_tag, classes, attrs = self.stack[-1]
        if top_tag == tag and tag == "a" and self.anchor is not None:
            text = self.anchor["text"].strip()
            if self.anchor["kind"] == "translation" and text and self.meaning is not None:
                if text not in self.meaning["translations"]:
                    self.meaning["translations"].append(text)
            elif self.anchor["kind"] == "headword" and self.entry is not None:
                if not self.entry["headword"].strip():
                    self.entry["headword"] = text
            self.anchor = None
        if top_tag == tag and "definition-example" in classes and self.example is not None and self.meaning is not None:
            if self.example["fr"].strip() or self.example["wolof"].strip():
                self.meaning["examples"].append({k: v.strip() for k, v in self.example.items()})
            self.example = None
        if top_tag == tag and "definition-meaning" in classes and self.meaning is not None and self.entry is not None:
            self.entry["meanings"].append(self.meaning)
            self.meaning = None
        if top_tag == tag and "definition__container" in classes and self.entry is not None:
            self.entries.append(self.entry)
            self.entry = None
            self.meaning = None
            self.example = None
        # Pop the matching open element and any malformed nested elements above it.
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def map_pos(value: str) -> str:
    lower = value.casefold()
    if "verbe" in lower:
        return "verb"
    if "nom" in lower:
        return "noun"
    if "adjectif" in lower:
        return "adjective"
    if "adverbe" in lower:
        return "adverb"
    if "préposition" in lower or "preposition" in lower:
        return "preposition"
    if "pronom" in lower:
        return "pronoun"
    if "article" in lower:
        return "article"
    if "conjonction" in lower:
        return "conjunction"
    return "other"


def normalize_entry(raw: dict, sense_index: int) -> dict | None:
    french = " ".join(raw.get("headword", "").split())
    if not french:
        return None
    meanings = raw.get("meanings") or []
    if sense_index >= len(meanings):
        return None
    meaning = meanings[sense_index]
    wolof_words = list(dict.fromkeys(" ".join(word.split()) for word in meaning.get("translations", []) if word.strip()))
    if not wolof_words:
        return None
    example = next((item for item in meaning.get("examples", []) if item.get("fr") and item.get("wolof")), None)
    source_path = raw.get("sourcePath") or "/dictionary"
    source_url = urljoin(BASE, quote(source_path, safe="/%"))
    entry_hash = hashlib.sha1(source_path.encode("utf-8")).hexdigest()[:8]
    entry_id = f"jangileen-{slugify(french)}-{sense_index + 1}-{entry_hash}"
    pos = map_pos(meaning.get("partOfSpeech", ""))
    comment = " ".join(meaning.get("comment", "").split())
    return {
        "id": entry_id,
        "soninke": {"word": "", "definition": "", "example": "", "audio_url": ""},
        "wolof": {
            "word": " / ".join(wolof_words),
            "definition": comment,
            "example": example["wolof"] if example else "",
            "audio_url": ""
        },
        "fr": {
            "word": french,
            "definition": comment,
            "example": example["fr"] if example else "",
            "audio_url": ""
        },
        "en": {"word": "", "definition": "", "example": "", "audio_url": ""},
        "grammar_category": pos,
        "category": "grammar" if pos in {"verb", "pronoun", "article", "preposition", "conjunction"} else "other",
        "source": source_url,
        "sourceName": "Jàngileen — dictionnaire français/wolof",
        "license": "Jàngileen indique que les données du dictionnaire peuvent être redistribuées et modifiées",
        "status": "draft",
        "origin": "external-dictionary",
        "pronunciationStatus": "unverified",
        "translationStatus": "source-documented"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/wolof-fr-dictionary.json")
    parser.add_argument("--delay", type=float, default=0.35)
    args = parser.parse_args()
    main_html = fetch(urljoin(BASE, "/dictionary"))
    letters = sorted(set(re.findall(r'href=["\'](/dictionary/browse/([A-Z]))["\']', main_html)))
    # Keep only the letter URL from each regex match.
    paths = sorted({match[0] for match in letters})
    if not paths:
        paths = [f"/dictionary/browse/{letter}" for letter in LETTERS]
    if len(paths) < 20:
        raise RuntimeError(f"Seulement {len(paths)} pages alphabétiques trouvées ; import refusé pour éviter un dictionnaire incomplet.")
    all_raw: list[dict] = []
    for index, path in enumerate(paths, start=1):
        url = urljoin(BASE, path)
        page = fetch(url)
        page_parser = DictionaryParser()
        page_parser.feed(page)
        if not page_parser.entries and not re.search(r"<h1>\s*0 mots français commençant", page, re.IGNORECASE):
            raise RuntimeError(f"Aucune entrée trouvée et page vide non confirmée sur {url}; import interrompu pour ne pas publier un lot partiel.")
        all_raw.extend(page_parser.entries)
        print(f"[{index}/{len(paths)}] {path}: {len(page_parser.entries)} entrées", flush=True)
        time.sleep(max(0.0, args.delay))
    normalized: dict[str, dict] = {}
    for raw in all_raw:
        for sense_index in range(max(1, len(raw.get("meanings") or []))):
            entry = normalize_entry(raw, sense_index)
            if entry:
                normalized[entry["id"]] = entry
    if len(normalized) < 500:
        raise RuntimeError(f"Seulement {len(normalized)} fiches normalisées ; au moins 500 sont attendues pour éviter un import partiel.")
    result = {
        "schemaVersion": 1,
        "source": "Jàngileen — dictionnaire français/wolof",
        "sourceUrl": urljoin(BASE, "/dictionary"),
        "sourceLegalUrl": urljoin(BASE, "/special/apropos"),
        "sourceLicenseNote": "Le site indique que les données du dictionnaire (mots, traductions et exemples) peuvent être redistribuées et modifiées.",
        "observedSourceCount": 911,
        "extractedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "entryCount": len(normalized),
        "entries": sorted(normalized.values(), key=lambda entry: (entry["fr"]["word"].casefold(), entry["id"]))
    }
    with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Import terminé : {len(normalized)} fiches Wolof–Français dans {args.output}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
        print(f"IMPORT INTERROMPU : {error}", file=sys.stderr)
        raise SystemExit(1)
