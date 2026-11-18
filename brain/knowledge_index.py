#!/usr/bin/env python3
"""The knowledge index: Swiss federal law and the bank's internal documents.

Strict mapping, one keyword field per language with its own analyzer, a semantic_text field
for multilingual search by meaning, and an ingest pipeline that detects the language.
Used by setup_brain.py.
"""

import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = "albisgrat-knowledge"
PIPELINE = INDEX + "-ingest"
INFERENCE_ID = os.environ.get("INFERENCE_ID", ".jina-embeddings-v5-text-small")

# Words the German decompounder may split compounds into ("Kundendaten" -> kunden + daten).
DE_WORDS = [
    "auslagerung", "kunde", "kunden", "daten", "dienstleister", "genehmigung", "geldwäscherei",
    "bank", "geheimnis", "schutz", "sicherheit", "bearbeitung", "auftrag", "bearbeiter",
    "bekanntgabe", "ausland", "vertrag", "risiko", "analyse", "meldung", "pflicht", "konto",
    "eröffnung", "aufbewahrung", "frist", "löschung", "anbieter", "beziehung", "geschäft",
    "verdacht", "identifizierung", "video", "sanktion", "berater", "person", "sorgfalt",
    "prüfung", "personen", "verletzung", "auskunft", "begehren", "transaktion", "überwachung",
    "berechtigte", "wirtschaftlich", "vermögen", "herkunft", "interessen", "konflikt",
]


def index_body():
    text = lambda analyzer: {"type": "text", "analyzer": analyzer}
    keyword = {"type": "keyword"}
    return {
        "settings": {
            "default_pipeline": PIPELINE,
            "analysis": {
                "filter": {
                    "de_stop": {"type": "stop", "stopwords": "_german_"},
                    "de_decompound": {"type": "dictionary_decompounder", "word_list": DE_WORDS,
                                      "min_subword_size": 4},
                    "de_stem": {"type": "stemmer", "language": "light_german"},
                    "fr_elision": {"type": "elision", "articles_case": True,
                                   "articles": ["l", "m", "t", "qu", "n", "s", "j", "d", "c",
                                                "jusqu", "quoiqu", "lorsqu", "puisqu"]},
                    "fr_stop": {"type": "stop", "stopwords": "_french_"},
                    "fr_stem": {"type": "stemmer", "language": "light_french"},
                    "it_elision": {"type": "elision", "articles_case": True,
                                   "articles": ["c", "l", "all", "dall", "dell", "nell", "sull",
                                                "coll", "pell", "gl", "agl", "dagl", "degl", "negl",
                                                "sugl", "un", "m", "t", "s", "v", "d"]},
                    "it_stop": {"type": "stop", "stopwords": "_italian_"},
                    "it_stem": {"type": "stemmer", "language": "light_italian"},
                },
                "analyzer": {
                    # German: split compounds, fold umlauts, stem.
                    "de_text": {"type": "custom", "tokenizer": "standard",
                                "filter": ["lowercase", "de_stop", "de_decompound",
                                           "german_normalization", "de_stem"]},
                    # French and Italian: remove elisions (l'avion -> avion), stem, fold accents.
                    "fr_text": {"type": "custom", "tokenizer": "standard",
                                "filter": ["fr_elision", "lowercase", "fr_stop", "fr_stem",
                                           "asciifolding"]},
                    "it_text": {"type": "custom", "tokenizer": "standard",
                                "filter": ["it_elision", "lowercase", "it_stop", "it_stem",
                                           "asciifolding"]},
                    "title_text": {"type": "custom", "tokenizer": "standard",
                                   "filter": ["lowercase", "asciifolding"]},
                },
            },
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": keyword,
                "title": text("title_text"),
                # The original text. Copied into the semantic field, which chunks and embeds it.
                "body": {"type": "text", "index": False, "copy_to": "body_semantic"},
                "body_de": text("de_text"),
                "body_fr": text("fr_text"),
                "body_it": text("it_text"),
                "body_en": text("english"),
                "body_semantic": {
                    "type": "semantic_text",
                    "inference_id": INFERENCE_ID,
                    "chunking_settings": {"strategy": "sentence", "max_chunk_size": 250,
                                          "sentence_overlap": 1},
                },
                "language": keyword,
                "language_detected": keyword,
                "language_confidence": {"type": "float"},
                "doc_type": keyword,
                "source": keyword,
                "source_url": keyword,
                "section": keyword,
                "law": keyword,
                "law_title": {"type": "text", "index": False},
                "sr_number": keyword,
                "doc_number": keyword,
                "version": keyword,
                "department": keyword,
                "supersedes": keyword,
                "valid_from": {"type": "date"},
                "valid_to": {"type": "date"},
                "is_current": {"type": "boolean"},
                "allowed_groups": keyword,
            },
        },
    }


def pipeline_body():
    return {
        "description": "Detect the language, then copy the text into the field for that language.",
        "processors": [
            {"inference": {
                "model_id": "lang_ident_model_1",
                "field_map": {"body": "text"},
                "target_field": "_lang",
                "inference_config": {"classification": {"num_top_classes": 1}},
                "ignore_failure": True,
            }},
            {"script": {
                "description": "Use the detected language when it is one of ours and confident. "
                               "Otherwise keep the language the source system declared.",
                "source": """
                    String declared = ctx.language;
                    String detected = null;
                    double conf = 0;
                    if (ctx._lang != null && ctx._lang.predicted_value != null) {
                      detected = ctx._lang.predicted_value;
                      if (ctx._lang.prediction_probability != null) {
                        conf = ((Number) ctx._lang.prediction_probability).doubleValue();
                      }
                    }
                    ctx.language_detected = detected;
                    ctx.language_confidence = conf;
                    String lang = declared;
                    if (detected != null && conf >= 0.8 && ['de','fr','it','en'].contains(detected)) {
                      lang = detected;
                    }
                    if (lang == null) { lang = 'de'; }
                    ctx.language = lang;
                    ctx['body_' + lang] = ctx.body;
                    ctx.remove('_lang');
                """,
            }},
        ],
    }


def load_documents():
    docs = []
    with open(os.path.join(ROOT, "data", "public", "fedlex.jsonl"), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "internal", "*.json"))):
        with open(path, encoding="utf-8") as f:
            docs.append(json.load(f))
    return docs
