#!/usr/bin/env python3
"""Generate the ES relation vocabulary dataset from the canonical table.

The canonical table mirrors EFS 2510:2026 clause 6 (relation vocabulary).
Outputs:
  datasets/es-relation-vocabulary-2026/concepts/<identifier>.yaml
      (multi-document YAML: managed concept + English localized concept,
      the layout used by glossarist v3 and concept-browser)
  skos/relation-type.ttl
      (SKOS scheme projection)

Run from the repository root:  python3 scripts/generate.py
"""
from pathlib import Path
from datetime import date, timezone
import json

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "datasets" / "es-relation-vocabulary-2026"
URN = "urn:enosema:relation-type:{identifier}"
ACCEPTED = "2026-11-11T00:00:00+00:00"

# (identifier, family, kind, inverse or None if symmetric, definition, source)
T = []
def add(family, kind, pairs, source):
    for ident, definition, inverse in pairs:
        T.append((ident, family, kind, inverse, definition, source))

add("hierarchical-generic", "generic", [
    ("broader_generic", "The current concept is a kind of the related concept (generic/specific).", "narrower_generic"),
    ("narrower_generic", "The related concept is a kind of the current concept.", "broader_generic"),
    ("broader", "The current concept is subsumed by the related concept; coordination method not stated.", "narrower"),
    ("narrower", "The related concept is subsumed by the current concept; coordination method not stated.", "broader"),
], "ISO 25964-1 (BTG/NTG); EFS 2510:2026, 6.2")
add("hierarchical-partitive", "partitive", [
    ("broader_partitive", "The current concept is a part of the related concept (whole/part).", "narrower_partitive"),
    ("narrower_partitive", "The related concept is a part of the current concept (whole/part).", "broader_partitive"),
    ("has_part", "The current concept has the related concept as a part.", "is_part_of"),
    ("is_part_of", "The current concept is a part of the related concept.", "has_part"),
], "ISO 25964-1; ISO 19135-1; EFS 2510:2026, 6.2")
add("hierarchical-instantial", "instantial", [
    ("broader_instantial", "The current concept is an instance of the related concept.", "narrower_instantial"),
    ("narrower_instantial", "The related concept is an instance of the current concept.", "broader_instantial"),
    ("instance_of", "The current concept is an instance of the related concept.", "has_instance"),
    ("has_instance", "The current concept has the related concept as an instance.", "instance_of"),
], "ISO 25964-1; ISO 19135-1; EFS 2510:2026, 6.2")
add("equivalence-mapping", "equivalence", [
    ("equivalent", "The current concept is equivalent in denotation to the related concept.", None),
    ("exact_match", "The current concept is an exact cross-vocabulary match of the related concept, replaceable one-for-one.", None),
    ("close_match", "The current concept is approximately equivalent to the related concept.", None),
    ("broad_match", "The related concept of another vocabulary is broader than the current concept.", "narrow_match"),
    ("narrow_match", "The related concept of another vocabulary is narrower than the current concept.", "broad_match"),
    ("related_match", "The current concept is associatively related to a concept of another vocabulary.", None),
    ("compare", "The current concept may be compared to the related concept to clarify distinctions.", None),
    ("contrast", "The current concept is understood in contrast to the related concept.", None),
], "ISO 25964-2; SKOS; ISO 10241-1; EFS 2510:2026, 6.3")
add("associative-contiguity", "contiguity", [
    ("enhances", "The current concept is a tool; the related concept is an accessory that enhances it.", "enhanced_by"),
    ("enhanced_by", "The current concept is an accessory that enhances the related tool.", "enhances"),
    ("contains", "The current concept is a container; the related concept is its content.", "contained_by_container"),
    ("contained_by_container", "The current concept is contained in the related container.", "contains"),
    ("contained_by_contained", "The current concept shares a container with the related concept.", None),
    ("attaches", "The current concept is a tool; the related concept is a connection attached to it.", "attached_to"),
    ("attached_to", "The current concept is a connection attached to the related tool.", "attaches"),
    ("made_of", "The current concept is a concrete item; the related concept is the material it is made of.", "material_of"),
    ("material_of", "The current concept is the material of the related item.", "made_of"),
    ("has_property", "The current concept possesses the property expressed by the related concept.", "property_of"),
    ("property_of", "The current concept is a property possessed by the related concept.", "has_property"),
    ("owns", "The current concept owns the related concept.", "owned_by"),
    ("owned_by", "The current concept is owned by the related concept.", "owns"),
    ("ranks_above", "The current concept outranks the related concept in a hierarchy of rank.", "ranks_below"),
    ("ranks_below", "The current concept is outranked by the related concept.", "ranks_above"),
], "ISO 704:2022, 5.5.5, Table 1 (contiguity); EFS 2510:2026, 6.4")
add("associative-sequential", "sequential", [
    ("causes", "The current concept causes the related concept.", "caused_by"),
    ("caused_by", "The current concept is caused by the related concept.", "causes"),
    ("develops_into", "The current concept is an earlier developmental stage of the related concept.", "develops_from"),
    ("develops_from", "The current concept develops from the earlier stage expressed by the related concept.", "develops_into"),
    ("sequentially_related", "The related concept follows or precedes the current concept in an unspecified order of sequence.", None),
    ("spatially_related", "The current concept is spatially positioned relative to the related concept.", None),
    ("temporally_related", "The current concept is temporally positioned relative to the related concept.", None),
], "ISO 704:2022, 5.5.5, Table 1 (sequential); ISO 12620; EFS 2510:2026, 6.4")
add("associative-activity", "activity", [
    ("performed_by", "The current concept is an action; the related concept is its actor.", "performs_action"),
    ("performs_action", "The current concept is the actor of the related action.", "performed_by"),
    ("done_by_method", "The current concept is an action; the related concept is the method used.", "method_of"),
    ("method_of", "The current concept is the method of the related action.", "done_by_method"),
    ("done_at", "The current concept is an action; the related concept is the place where it is done.", "place_of_action"),
    ("place_of_action", "The current concept is the place of the related action.", "done_at"),
    ("done_for_purpose", "The current concept is an action; the related concept is its objective.", "purpose_of_action"),
    ("purpose_of_action", "The current concept is the objective of the related action.", "done_for_purpose"),
    ("done_for_beneficiary", "The current concept is an action; the related concept is its beneficiary.", "beneficiary_of_action"),
    ("beneficiary_of_action", "The current concept is the beneficiary of the related action.", "done_for_beneficiary"),
    ("acts_on_object", "The current concept is an action; the related concept is its object.", "object_of_action"),
    ("object_of_action", "The current concept is the object of the related action.", "acts_on_object"),
    ("done_with_tool", "The current concept is an action; the related concept is the instrument used.", "tool_of_action"),
    ("tool_of_action", "The current concept is the instrument of the related action.", "done_with_tool"),
    ("acts_on_patient", "The current concept is an action; the related concept is the patient undergoing it.", "patient_of_action"),
    ("patient_of_action", "The current concept is the patient of the related action.", "acts_on_patient"),
], "ISO 704:2022, 5.5.5, Table 1 (activity); EFS 2510:2026, 6.4")
add("associative-instrumental", "instrumental", [
    ("produces", "The current concept is the producer; the related concept is the product.", "produced_by"),
    ("produced_by", "The current concept is the product of the related producer.", "produces"),
    ("made_from_ingredient", "The current concept is the product; the related concept is the raw material.", "ingredient_of"),
    ("ingredient_of", "The current concept is the raw material of the related product.", "made_from_ingredient"),
    ("produced_by_instrument", "The current concept is the tool; the related concept is the product produced with it.", "instrument_product_of"),
    ("instrument_product_of", "The current concept is the product produced with the related tool.", "produced_by_instrument"),
    ("employed_by_professional", "The current concept is the professional; the related concept is the tool employed.", "employs_tool"),
    ("employs_tool", "The current concept is the tool employed by the related professional.", "employed_by_professional"),
    ("handled_by_tool", "The current concept is the object; the related concept is the tool used to handle it.", "tool_handles"),
    ("tool_handles", "The current concept is the tool that handles the related object.", "handled_by_tool"),
    ("applied_to_patient", "The current concept is the tool; the related concept is the patient it is applied to.", "patient_of_tool"),
    ("patient_of_tool", "The current concept is the patient to whom the related tool is applied.", "applied_to_patient"),
], "ISO 704:2022, 5.5.5, Table 1 (instrumental); EFS 2510:2026, 6.4")
add("associative-interactional-origination-transmission", "interactional", [
    ("controls", "The current concept controls the related concept.", "controlled_by"),
    ("controlled_by", "The current concept is controlled by the related concept.", "controls"),
    ("represents", "The current concept represents the related concept.", "represented_by"),
    ("represented_by", "The current concept is represented by the related concept.", "represents"),
    ("originates_from", "The current concept originates from the related concept (producer-product semantics).", "origin_of"),
    ("origin_of", "The current concept is the origin of the related concept.", "originates_from"),
    ("sends_to", "The current concept sends to the related concept.", "receives_from"),
    ("receives_from", "The current concept receives from the related concept.", "sends_to"),
    ("sends_object", "The current concept sends the related object.", "object_sent_by"),
    ("object_sent_by", "The current concept is the object sent by the related sender.", "sends_object"),
], "ISO 704:2022, 5.5.5, Table 1 (interactional, origination, transmission); EFS 2510:2026, 6.4")
add("associative-opposition", "opposition", [
    ("opposite_of", "The current concept is the opposite of the related concept.", None),
], "ISO 704:2022, 5.5.5, Table 1 (opposite); EFS 2510:2026, 6.4")
add("lexical", "lexical", [
    ("see", "The definition of the current concept is completed by referring to the related concept.", None),
    ("references", "The current concept references the related concept.", "referenced_by"),
    ("referenced_by", "The current concept is referenced by the related concept.", "references"),
    ("related_concept", "The current concept is associated with the related concept without a stated kind.", None),
    ("related_concept_broader", "The current concept is associated with the related concept in a broader sense.", "related_concept_narrower"),
    ("related_concept_narrower", "The current concept is associated with the related concept in a narrower sense.", "related_concept_broader"),
    ("homograph", "The related designation is spelled identically to the current designation but denotes a different concept.", None),
    ("false_friend", "The related designation looks or sounds similar in another language but denotes a different concept.", None),
], "ISO 12620; ISO 10241-1; EFS 2510:2026, 6.5")
add("lifecycle", "lifecycle", [
    ("deprecates", "The current concept deprecates the related concept: continued use of the related concept is discouraged.", "deprecated_by"),
    ("deprecated_by", "The current concept has been deprecated by the related concept.", "deprecates"),
    ("supersedes", "The current concept supersedes the related concept and replaces it prospectively.", "superseded_by"),
    ("superseded_by", "The current concept has been superseded by the related concept.", "supersedes"),
    ("replaces", "The current concept replaces the related concept in the register.", "replaced_by"),
    ("replaced_by", "The current concept has been replaced in the register by the related concept.", "replaces"),
    ("invalidates", "The current concept invalidates the related concept.", "invalidated_by"),
    ("invalidated_by", "The current concept has been invalidated by the related concept.", "invalidates"),
    ("retires", "The current concept retires the related concept from the register.", "retired_by"),
    ("retired_by", "The current concept has been retired from the register by the related concept.", "retires"),
], "ISO 10241-1; ISO 19135-1; EFS 2510:2026, 6.5")
add("register", "register", [
    ("has_concept", "The current register item has the related item as its concept.", "is_concept_of"),
    ("is_concept_of", "The current item is the concept of the related register item.", "has_concept"),
    ("has_definition", "The current concept has the related item as a definition.", "definition_of"),
    ("definition_of", "The current item is a definition of the related concept.", "has_definition"),
    ("inherits", "The current concept inherits characteristics from the related concept.", "inherited_by"),
    ("inherited_by", "The current concept is a source of inheritance for the related concept.", "inherits"),
], "ISO 19135-1; EFS 2510:2026, 6.5")
add("versioning", "versioning", [
    ("has_version", "The current concept has the related concept as a version.", "version_of"),
    ("version_of", "The current concept is a version of the related concept.", "has_version"),
    ("current_version", "The related concept is the current version among the versions of the current concept.", "current_version_of"),
    ("current_version_of", "The current concept is the current version of the related concept.", "current_version"),
], "ISO 19135-1; EFS 2510:2026, 6.5")

SYMMETRIC_NOTE = ("This relation type is symmetric: it carries no distinct "
                  "inverse; the assertion holds in both directions.")


def q(s):
    """Quote a string as a double-quoted YAML scalar."""
    return json.dumps(s, ensure_ascii=False)

CONCEPTS_DIR = DATASET / "concepts"
CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)

TTL_HEADER = """# ES Relation Vocabulary — SKOS projection of EFS 2510:2026, clause 6.
# Generated by scripts/generate.py — do not edit by hand.
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix eno: <urn:enosema:relation-type:> .

<urn:enosema:relation-vocabulary:2026> a skos:ConceptScheme ;
    dcterms:title "ES Relation Vocabulary"@en ;
    dcterms:creator "Enosema Foundation" ;
    dcterms:issued "%(issued)s" ;
    skos:hasTopConcept eno:broader_generic, eno:broader_partitive, eno:broader_instantial,
        eno:equivalent, eno:enhances, eno:causes, eno:performed_by, eno:produces,
        eno:controls, eno:opposite_of, eno:see, eno:deprecates, eno:has_concept, eno:has_version ;
    skos:note "Controlled vocabulary of concept relation types per EFS 2510:2026, clause 6."@en .
""" % {"issued": date.today().isoformat()}

family_collections = {}
ttl_lines = [TTL_HEADER]
for identifier, family, kind, inverse, definition, source in T:
    uri = URN.format(identifier=identifier)
    # --- managed + localized concept file (glossarist v3, two documents) ---
    related = ""
    if inverse:
        related = (
            "related:\n"
            "- type: related_concept\n"
            "  content:\n"
            "    eng: \"inverse relation type\"\n"
            "  ref:\n"
            "    source: ES\n"
            f"    id: {inverse}\n"
        )
    note = SYMMETRIC_NOTE if inverse is None else f"Inverse relation type: `{inverse}`."
    concept = f"""---
id: {identifier}
data:
  identifier: {identifier}
  uri: {uri}
status: valid
date_accepted: '{ACCEPTED}'
sources:
- type: authoritative
  origin:
    ref:
      source: EFS 2510:2026
      clause: 6
    link: https://www.enosema.org/standards/docs/efs-2510/2026/
{related}---
id: {identifier}-eng
termid: {identifier}
data:
  language_code: eng
  terms:
  - type: expression
    designation: {identifier}
    normative_status: preferred
  definition:
  - content: {q(definition)}
  notes:
  - content: {q(note + " Relation family: " + family + ". Source: " + source + ".")}
status: valid
"""
    (CONCEPTS_DIR / f"{identifier}.yaml").write_text(concept)
    # --- SKOS ---
    inv_line = (f"    owl:inverseOf eno:{inverse} ;\n" if inverse else "")
    ttl_lines.append(f"""eno:{identifier} a skos:Concept ;
    skos:prefLabel "{identifier}"@en ;
    skos:definition "{definition}"@en ;
    skos:inScheme <urn:enosema:relation-vocabulary:2026> ;
    dcterms:source "{source}" ;{inv_line}
    skos:note "Family: {family}. Symmetric."@en ;
.

""" if inverse is None else f"""eno:{identifier} a skos:Concept ;
    skos:prefLabel "{identifier}"@en ;
    skos:definition "{definition}"@en ;
    skos:inScheme <urn:enosema:relation-vocabulary:2026> ;
    dcterms:source "{source}" ;
    owl:inverseOf eno:{inverse} ;
.

""")
    family_collections.setdefault(family, []).append(identifier)

print(f"wrote {len(T)} concept files to {CONCEPTS_DIR}")

# SKOS collections per family
ttl_lines.append("# Families\n\n")
for family, idents in family_collections.items():
    members = ", ".join(f"eno:{i}" for i in idents)
    ttl_lines.append(f"""<urn:enosema:relation-family:{family}> a skos:Collection ;
    dcterms:title "{family} relation types"@en ;
    skos:member {members} ;
.

""")
(ROOT / "skos").mkdir(exist_ok=True)
(ROOT / "skos" / "relation-type.ttl").write_text("".join(ttl_lines))
print(f"wrote skos/relation-type.ttl")
