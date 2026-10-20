"""Every educational resource that was examined, with its licence and what this project took from it."""
from .model import Source

ADEM_SN_6E = Source(
    id="adem-sn-6e",
    title="Fascicule Mathématiques 6ème (v10.17)",
    publisher="Projet ADEM-Dakar, Ministère de l'Éducation nationale du Sénégal, financé par l'AFD",
    url="https://apprendre.auf.org/wp-content/uploads/2021/08/fascicule_adem_math_6e.pdf",
    licence="Free booklet marked 'interdit à la vente'. No open licence was found, so no text, exercise or figure is copied.",
    use="Which topics belong in a first chapter on decimal numbers (decimal numbers, ordering, addition, subtraction) and the kinds of exercises it asks for. "
        "The booklet contains exercises only, so every explanation, example and exercise here was written independently, with our own numbers and our own order of sections.",
    attribution="Topics inspired by the ADEM-Dakar Sixième booklet.",
)

CI_PROGRAMME_6E = Source(
    id="ci-programme-6e",
    title="Programme éducatif Mathématiques 6ème",
    publisher="Ministère de l'Éducation Nationale et de l'Enseignement Technique, Côte d'Ivoire",
    url="https://apprendre.auf.org/wp-content/uploads/2021/08/5-Programme_Educatif_Maths_6ieme.pdf",
    licence="Official programme, no licence statement found. Used only to read objectives, nothing is copied.",
    use="Read to cross-check the Sixième number work. Its number lessons are natural numbers, relative decimal numbers and fractions "
        "(the fractions lesson includes decimal fractions), so it does not list this chapter as a separate lesson and no alignment with it is claimed.",
)

REB = Source(
    id="reb-rw",
    title="Rwanda Basic Education Board mathematics books",
    publisher="Rwanda Basic Education Board",
    url="https://elearning.reb.rw/",
    licence="Marked 'All rights reserved' with credit to REB required when quoting. No open licence found.",
    use="Not used yet.",
)

SIYAVULA = Source(
    id="siyavula",
    title="Siyavula Everything Maths",
    publisher="Siyavula Education",
    url="https://www.siyavula.com/read",
    licence="Branded editions are CC BY-ND (no adaptation). Unbranded editions are CC BY and may be adapted with credit to Siyavula.",
    use="Not used yet. Only the unbranded CC BY editions may be adapted.",
)

SOURCES = {s.id: s for s in (ADEM_SN_6E, CI_PROGRAMME_6E, REB, SIYAVULA)}
