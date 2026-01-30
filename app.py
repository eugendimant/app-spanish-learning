import difflib
import hashlib
import json
import random
import sqlite3
from csv import DictWriter
from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


DATA_DIR = Path("data")
PORTFOLIO_PATH = DATA_DIR / "portfolio.json"
DB_PATH = DATA_DIR / "vivalingo.db"


@dataclass(frozen=True)
class DiagnosticIssue:
    area: str
    pattern: str
    impact: str
    example: str
    fix: str


DIAGNOSTIC_AREAS = [
    "Collocations",
    "Prepositions",
    "Discourse markers",
    "Register & tone",
    "Nuance & pragmatics",
]

DIAGNOSTIC_ISSUES = [
    DiagnosticIssue(
        "Collocations",
        "hacer una decisión",
        "Sounds literal; native usage prefers a different verb.",
        "Tomamos una decisión informada después del informe.",
        "Swap to 'tomar una decisión'.",
    ),
    DiagnosticIssue(
        "Collocations",
        "gran cantidad de gente",
        "Natural but heavy; try more precise nouns.",
        "Había una multitud en la plaza.",
        "Use 'multitud' or 'afluencia'.",
    ),
    DiagnosticIssue(
        "Prepositions",
        "depender en",
        "Preposition mismatch; register error.",
        "Depende de la disponibilidad del equipo.",
        "Use 'depender de'.",
    ),
    DiagnosticIssue(
        "Prepositions",
        "casarse con vs casarse de",
        "Regional mismatch.",
        "Se casó con su pareja en junio.",
        "Use 'casarse con'.",
    ),
    DiagnosticIssue(
        "Discourse markers",
        "por otro lado (without contrast)",
        "Connector doesn't match logic.",
        "Por otro lado, los datos confirman la tendencia.",
        "Use 'además' if additive.",
    ),
    DiagnosticIssue(
        "Discourse markers",
        "sin embargo + clause without contrast",
        "Creates incoherence.",
        "Sin embargo, los resultados fueron positivos.",
        "Use only with contrastive content.",
    ),
    DiagnosticIssue(
        "Register & tone",
        "tú in formal email",
        "Inappropriate level of formality.",
        "Le agradecería una respuesta antes del viernes.",
        "Maintain 'usted' and honorifics.",
    ),
    DiagnosticIssue(
        "Register & tone",
        "overly direct request",
        "Politeness strategies missing.",
        "¿Sería posible ajustar la fecha?",
        "Add hedging and modal verbs.",
    ),
    DiagnosticIssue(
        "Nuance & pragmatics",
        "literal translation of idioms",
        "Feels calqued and non-native.",
        "Me dio la impresión de que no estaban listos.",
        "Replace with natural phraseology.",
    ),
    DiagnosticIssue(
        "Nuance & pragmatics",
        "missing mitigation",
        "Sounds abrupt or face-threatening.",
        "Quizá podríamos revisar otra opción.",
        "Add softeners + hedging.",
    ),
]

TRAINING_PLAN = {
    "Collocations": [
        "Daily collocation micro-drills (verb-noun & adjective-noun).",
        "Shadow 10 native corpus sentences and rewrite with variants.",
    ],
    "Prepositions": [
        "Contrastive pairs drill (a/de/en/por/para).",
        "Record yourself using 5 preposition-dependent verbs.",
    ],
    "Discourse markers": [
        "Map argument flow with connectors per paragraph.",
        "Swap connectors to test semantic alignment.",
    ],
    "Register & tone": [
        "Rewrite the same prompt in 5 registers weekly.",
        "Score politeness strategies and hedging density.",
    ],
    "Nuance & pragmatics": [
        "Collect 3 softeners per week and use them in dialogue.",
        "Track irony/contrast markers in listening samples.",
    ],
}

REGISTER_STYLES = [
    "Informal WhatsApp",
    "Workplace email",
    "Academic abstract",
    "Polite complaint",
    "Persuasive pitch",
]

RUBRIC_DIMENSIONS = [
    "Politeness strategies",
    "Hedging",
    "Directness",
    "Idiomaticity",
    "Audience fit",
]

REGISTER_MARKERS = {
    "politeness": ["por favor", "le agradecería", "quisiera", "sería posible", "disculpe"],
    "hedging": ["quizá", "tal vez", "podría", "sería", "me parece"],
    "direct": ["necesito", "exijo", "debe", "quiero"],
    "idiomatic": ["me da la impresión", "en pocas palabras", "a fin de cuentas", "de hecho"],
    "academic": ["objetivo", "metodología", "resultados", "conclusión", "se analiza"],
    "whatsapp": ["jaja", "qué tal", "oye", "vale", "👍"],
    "pitch": ["propuesta", "impacto", "beneficio", "valor", "oportunidad"],
}

PRONUNCIATION_TARGETS = [
    {
        "phrase": "Me da la impresión de que podríamos ajustar el plan.",
        "focus": ["stress placement", "linking", "intonation (contrast)"],
        "notes": "Focus on rising-falling contour across the contrastive clause.",
    },
    {
        "phrase": "¿Te parece si lo revisamos mañana por la tarde?",
        "focus": ["rhythm", "question contour", "softening"],
        "notes": "Keep the rhythm even; lift pitch on the final question.",
    },
    {
        "phrase": "No es que no quiera, es que no llego a tiempo.",
        "focus": ["stress", "contrast", "intonation (irony)"],
        "notes": "Contrast the clauses with a clear pause and pitch reset.",
    },
]

COLLOCATION_SETS = [
    {
        "pair": "tomar una decisión",
        "type": "verb-noun",
        "frame": "Después de analizar los datos, ___ una decisión.",
        "options": ["tomamos", "hacemos"],
        "native": "tomamos",
        "rewrite": "Tomamos una decisión informada tras el informe.",
    },
    {
        "pair": "alto nivel de",
        "type": "adjective-noun",
        "frame": "El proyecto exige un ___ compromiso.",
        "options": ["alto", "elevado"],
        "native": "alto",
        "rewrite": "El proyecto exige un alto nivel de compromiso.",
    },
]

PORTFOLIO_AXES = [
    "Lexical sophistication",
    "Collocation accuracy",
    "Pragmatic appropriateness",
    "Prosody",
    "Cohesion",
]

TOPIC_DIVERSITY_DOMAINS = [
    {
        "domain": "Healthcare",
        "register": ["neutral", "formal"],
        "sample": "Tuve que pedir una segunda opinión para el diagnóstico.",
        "keywords": ["salud", "diagnóstico", "síntoma", "consulta", "tratamiento"],
        "lexicon": [
            {"term": "diagnóstico", "meaning": "identificación médica", "register": "formal", "pos": "noun"},
            {"term": "síntoma", "meaning": "señal clínica", "register": "neutral", "pos": "noun"},
            {"term": "recetar", "meaning": "indicar un tratamiento", "register": "formal", "pos": "verb"},
        ],
    },
    {
        "domain": "Housing",
        "register": ["formal", "neutral"],
        "sample": "El contrato de arrendamiento incluye cláusulas de mantenimiento.",
        "keywords": ["alquiler", "contrato", "arrendamiento", "fianza", "piso"],
        "lexicon": [
            {"term": "arrendamiento", "meaning": "contrato de alquiler", "register": "formal", "pos": "noun"},
            {"term": "fianza", "meaning": "depósito de garantía", "register": "neutral", "pos": "noun"},
            {"term": "cláusula", "meaning": "condición contractual", "register": "formal", "pos": "noun"},
        ],
    },
    {
        "domain": "Relationships",
        "register": ["neutral", "casual"],
        "sample": "Necesitamos hablar con calma para aclarar lo que pasó.",
        "keywords": ["relación", "confianza", "pareja", "aclarar", "apoyo"],
        "lexicon": [
            {"term": "aclarar", "meaning": "explicar para evitar malentendidos", "register": "neutral", "pos": "verb"},
            {"term": "apoyo", "meaning": "respaldo emocional", "register": "neutral", "pos": "noun"},
            {"term": "confianza", "meaning": "seguridad en la relación", "register": "neutral", "pos": "noun"},
        ],
    },
    {
        "domain": "Travel problems",
        "register": ["neutral", "casual"],
        "sample": "El vuelo se retrasó y perdimos la conexión.",
        "keywords": ["vuelo", "retraso", "conexión", "equipaje", "reserva"],
        "lexicon": [
            {"term": "retraso", "meaning": "demora en horario", "register": "neutral", "pos": "noun"},
            {"term": "reclamar", "meaning": "pedir una compensación", "register": "formal", "pos": "verb"},
            {"term": "conexión", "meaning": "tramo de viaje enlazado", "register": "neutral", "pos": "noun"},
        ],
    },
    {
        "domain": "Workplace conflict",
        "register": ["formal", "neutral"],
        "sample": "Tuvimos que mediar para evitar que el conflicto escalara.",
        "keywords": ["conflicto", "equipo", "reunión", "responsabilidad", "plazo"],
        "lexicon": [
            {"term": "mediar", "meaning": "intervenir para resolver", "register": "formal", "pos": "verb"},
            {"term": "tensión", "meaning": "estado de fricción", "register": "neutral", "pos": "noun"},
            {"term": "responsabilidad", "meaning": "obligación asignada", "register": "formal", "pos": "noun"},
        ],
    },
    {
        "domain": "Finance",
        "register": ["formal", "neutral"],
        "sample": "Necesito ajustar el presupuesto para cerrar el trimestre.",
        "keywords": ["presupuesto", "factura", "ingresos", "gastos", "ahorro"],
        "lexicon": [
            {"term": "presupuesto", "meaning": "plan de gastos e ingresos", "register": "formal", "pos": "noun"},
            {"term": "liquidez", "meaning": "dinero disponible", "register": "formal", "pos": "noun"},
            {"term": "facturar", "meaning": "emitir factura", "register": "formal", "pos": "verb"},
        ],
    },
    {
        "domain": "Cooking",
        "register": ["neutral", "casual"],
        "sample": "Salteé las verduras antes de añadir la salsa.",
        "keywords": ["receta", "horno", "saltear", "sabor", "ingrediente"],
        "lexicon": [
            {"term": "saltear", "meaning": "cocinar rápidamente con poco aceite", "register": "neutral", "pos": "verb"},
            {"term": "ingrediente", "meaning": "componente de una receta", "register": "neutral", "pos": "noun"},
            {"term": "sazonar", "meaning": "añadir condimentos", "register": "neutral", "pos": "verb"},
        ],
    },
    {
        "domain": "Emotions",
        "register": ["neutral", "formal"],
        "sample": "Me invadió una mezcla de alivio y cansancio.",
        "keywords": ["emociones", "alivio", "ansiedad", "frustración", "calma"],
        "lexicon": [
            {"term": "alivio", "meaning": "sensación de descanso", "register": "neutral", "pos": "noun"},
            {"term": "frustración", "meaning": "malestar por expectativas incumplidas", "register": "formal", "pos": "noun"},
            {"term": "serenar", "meaning": "calmar el ánimo", "register": "formal", "pos": "verb"},
        ],
    },
    {
        "domain": "Bureaucracy",
        "register": ["formal"],
        "sample": "Hay que tramitar el documento antes del plazo.",
        "keywords": ["trámite", "documento", "solicitud", "plazo", "oficina"],
        "lexicon": [
            {"term": "tramitar", "meaning": "gestionar un proceso", "register": "formal", "pos": "verb"},
            {"term": "solicitud", "meaning": "pedido formal", "register": "formal", "pos": "noun"},
            {"term": "plazo", "meaning": "tiempo límite", "register": "formal", "pos": "noun"},
        ],
    },
    {
        "domain": "Everyday slang-light",
        "register": ["casual"],
        "sample": "Qué bajón, se cayó el plan a última hora.",
        "keywords": ["plan", "bajón", "rollo", "vale", "guay"],
        "lexicon": [
            {"term": "bajón", "meaning": "desánimo repentino", "register": "casual", "pos": "noun"},
            {"term": "rollo", "meaning": "tema o situación", "register": "casual", "pos": "noun"},
            {"term": "guay", "meaning": "genial", "register": "casual", "pos": "adjective"},
        ],
    },
]

VOCAB_CONTEXT_UNITS = [
    {
        "term": "tomar una decisión",
        "collocations": ["tomar una decisión", "tomar una postura"],
        "contexts": [
            "—¿Ya resolviste lo del cambio de proveedor?\n—Sí, tomamos una decisión anoche.",
            "Mensaje: Tomamos una decisión: renegociar el contrato esta semana.",
            "Mini-parágrafo: Tras revisar los datos, el comité tomó una decisión estratégica para proteger el margen.",
        ],
        "question": "¿Quién tomó la decisión en los ejemplos?",
        "cloze": {
            "sentence": "Después de analizarlo, ___ una decisión rápida.",
            "options": ["tomamos", "hicimos", "dimos"],
            "answer": "tomamos",
            "explanation": "Tomar es el verbo natural para decisiones en español.",
        },
        "scenario": "Escribe una frase en la que decidas algo en un contexto laboral.",
        "swap": {
            "base": "Tomamos una decisión prudente para evitar el riesgo.",
            "choices": ["medida", "postura", "ruta"],
        },
    },
    {
        "term": "me da la sensación de que",
        "collocations": ["me da la sensación de que", "me da la impresión de que"],
        "contexts": [
            "Diálogo: Me da la sensación de que el cliente está dudando.",
            "Texto: Me da la sensación de que llegaremos tarde si no salimos ya.",
            "Mini-parágrafo: Me da la sensación de que el equipo necesita más claridad en los objetivos.",
        ],
        "question": "¿Qué indica la frase: certeza o percepción?",
        "cloze": {
            "sentence": "___ no están totalmente convencidos de la propuesta.",
            "options": ["Me da la sensación de que", "Estoy seguro de que", "Confirmo que"],
            "answer": "Me da la sensación de que",
            "explanation": "La frase indica percepción, no certeza absoluta.",
        },
        "scenario": "Escribe una frase que exprese intuición sobre un proyecto.",
        "swap": {
            "base": "Me da la sensación de que el plan es viable.",
            "choices": ["posible", "arriesgado", "inviable"],
        },
    },
]

VERB_CHOICE_STUDIO = [
    {
        "scenario": "Quieres explicar que lograste sacar un proyecto adelante pese a obstáculos.",
        "options": [
            {
                "verb": "sacar adelante",
                "register": "neutral",
                "intensity": "alta",
                "implication": "superar obstáculos y completar algo complejo",
                "objects": "proyecto, iniciativa, proceso",
            },
            {
                "verb": "terminar",
                "register": "neutral",
                "intensity": "media",
                "implication": "completar sin enfatizar esfuerzo",
                "objects": "tarea, informe",
            },
            {
                "verb": "hacer",
                "register": "casual",
                "intensity": "baja",
                "implication": "acción genérica, poco precisa",
                "objects": "cosas, trabajo",
            },
        ],
        "best": "sacar adelante",
        "also": ["terminar"],
        "contrast": [
            "Terminar suena neutro y no comunica la presión.",
            "Hacer es demasiado vago para este contexto.",
        ],
    },
    {
        "scenario": "Necesitas expresar que alcanzaste un objetivo medible.",
        "options": [
            {
                "verb": "alcanzar",
                "register": "formal",
                "intensity": "media",
                "implication": "logro cuantificable",
                "objects": "meta, objetivo, cifra",
            },
            {
                "verb": "conseguir",
                "register": "neutral",
                "intensity": "media",
                "implication": "logro general, menos técnico",
                "objects": "resultado, permiso",
            },
            {
                "verb": "lograr",
                "register": "formal",
                "intensity": "alta",
                "implication": "esfuerzo destacado",
                "objects": "acuerdo, avance",
            },
        ],
        "best": "alcanzar",
        "also": ["lograr"],
        "contrast": [
            "Lograr es más enfático; úsalo si quieres destacar esfuerzo.",
            "Conseguir es correcto pero menos preciso para metas numéricas.",
        ],
    },
]

DAILY_MISSION_GRAMMAR = [
    "subjuntivo con sugerencias (Es importante que + subjuntivo)",
    "condicional para propuestas (Podríamos...)",
    "conectores concesivos (aunque, si bien)",
    "pretérito vs imperfecto (marcar fondo y acción puntual)",
]

DAILY_MISSION_VERBS = [
    "sopesar",
    "desactivar",
    "plantear",
    "afrontar",
    "tramitar",
    "aportar",
    "exigir",
]

CONTENT_INGEST_HINTS = {
    "Healthcare": ["salud", "médico", "hospital", "síntoma", "diagnóstico"],
    "Housing": ["alquiler", "piso", "hipoteca", "contrato", "vecino"],
    "Travel problems": ["vuelo", "hotel", "reserva", "retraso", "equipaje"],
    "Finance": ["precio", "factura", "presupuesto", "inversión", "pago"],
    "Workplace conflict": ["reunión", "equipo", "conflicto", "jefe", "plazo"],
}

CONVERSATION_GOAL_SCENARIOS = [
    {
        "title": "Negociar un reembolso",
        "brief": "El servicio falló y necesitas un reembolso parcial sin romper la relación.",
        "hidden_targets": [
            "Usa 2 mitigadores (quizá, tal vez, me parece).",
            "Incluye una concesión (aunque, si bien).",
            "Evita 'aplicar para' como calco.",
        ],
    },
    {
        "title": "Resolver un conflicto en el trabajo",
        "brief": "Un colega no cumplió plazos y necesitas renegociar el cronograma.",
        "hidden_targets": [
            "Usa 1 verbo preciso (afrontar, plantear, desactivar).",
            "Incluye una petición indirecta (¿sería posible...?).",
            "Mantén registro neutral-formal.",
        ],
    },
]

ERROR_TAGS = {
    "dependen en": "preposition",
    "tomar una decisión en": "preposition",
    "la problema": "gender agreement",
    "verb precision": "verb choice",
}

VOCAB_DOMAINS = [
    {
        "domain": "Climate adaptation & resilience",
        "context": (
            "Las ciudades costeras están rediseñando su infraestructura para **mitigar** el "
            "**riesgo** de inundaciones, pero también para **blindar** servicios críticos y "
            "**reforzar** cadenas de suministro."
        ),
        "lexicon": [
            {
                "term": "mitigar",
                "meaning": "reducir el impacto de algo negativo",
                "example": "Se busca mitigar los efectos de las marejadas.",
                "register": "formal",
            },
            {
                "term": "blindar",
                "meaning": "proteger de forma sólida o estratégica",
                "example": "El plan pretende blindar la red eléctrica.",
                "register": "formal",
            },
            {
                "term": "reforzar",
                "meaning": "hacer más sólido o resistente",
                "example": "Hay que reforzar los diques.",
                "register": "neutral",
            },
            {
                "term": "umbral",
                "meaning": "límite crítico o punto de cambio",
                "example": "Superamos el umbral de tolerancia.",
                "register": "formal",
            },
        ],
    },
    {
        "domain": "Workplace dynamics & negotiation",
        "context": (
            "En negociaciones complejas conviene **sopesar** concesiones, "
            "**desactivar** tensiones y **pactar** un cronograma realista sin **ceder** "
            "más de lo necesario."
        ),
        "lexicon": [
            {
                "term": "sopesar",
                "meaning": "evaluar con calma varias opciones",
                "example": "Sopesó cada propuesta antes de responder.",
                "register": "formal",
            },
            {
                "term": "desactivar",
                "meaning": "reducir un conflicto o tensión",
                "example": "Buscamos desactivar la fricción con el cliente.",
                "register": "neutral",
            },
            {
                "term": "pactar",
                "meaning": "llegar a un acuerdo explícito",
                "example": "Pactaron nuevos plazos y prioridades.",
                "register": "neutral",
            },
            {
                "term": "ceder",
                "meaning": "entregar algo de forma parcial",
                "example": "Ceder demasiado puede debilitar la posición.",
                "register": "neutral",
            },
        ],
    },
    {
        "domain": "Health policy & public trust",
        "context": (
            "La estrategia debe **priorizar** la transparencia para **restablecer** "
            "la confianza pública, sin **subestimar** la fatiga informativa ni "
            "**desmentir** rumores con tono condescendiente."
        ),
        "lexicon": [
            {
                "term": "priorizar",
                "meaning": "dar prioridad a algo",
                "example": "El plan prioriza la atención primaria.",
                "register": "formal",
            },
            {
                "term": "restablecer",
                "meaning": "volver a instaurar",
                "example": "Restablecer la confianza requiere coherencia.",
                "register": "formal",
            },
            {
                "term": "subestimar",
                "meaning": "dar menos importancia de la real",
                "example": "No hay que subestimar el cansancio social.",
                "register": "neutral",
            },
            {
                "term": "desmentir",
                "meaning": "negar públicamente una información",
                "example": "El ministerio desmintió el rumor.",
                "register": "formal",
            },
        ],
    },
]

VERB_PRECISION_DRILLS = [
    {
        "scenario": "Necesitas decir que evaluaste opciones con calma antes de decidir.",
        "options": [
            {
                "verb": "sopesar",
                "nuance": "evaluación cuidadosa y estratégica",
                "example": "Sopesamos los riesgos antes de firmar.",
            },
            {
                "verb": "mirar",
                "nuance": "revisión general, poco profunda",
                "example": "Miramos los datos rápidamente.",
            },
            {
                "verb": "considerar",
                "nuance": "evaluación neutra, menos intensa",
                "example": "Consideramos varias alternativas.",
            },
        ],
        "best": "sopesar",
        "contrast": "Sopesar implica deliberación más intensa que considerar.",
    },
    {
        "scenario": "Quieres expresar que bajaste la tensión en una reunión.",
        "options": [
            {
                "verb": "desactivar",
                "nuance": "neutraliza tensión o conflicto",
                "example": "Desactivó la discusión con humor.",
            },
            {
                "verb": "parar",
                "nuance": "detener de forma brusca",
                "example": "Paró la conversación en seco.",
            },
            {
                "verb": "calmar",
                "nuance": "reducir intensidad emocional",
                "example": "Calmó a su equipo con claridad.",
            },
        ],
        "best": "desactivar",
        "contrast": "Desactivar es más táctico que calmar y menos brusco que parar.",
    },
    {
        "scenario": "Necesitas afirmar que insististe en cumplir una norma.",
        "options": [
            {
                "verb": "exigir",
                "nuance": "imponer con autoridad o firmeza",
                "example": "Exigió el cumplimiento del contrato.",
            },
            {
                "verb": "pedir",
                "nuance": "solicitud neutra",
                "example": "Pidió una actualización.",
            },
            {
                "verb": "sugerir",
                "nuance": "propuesta suave",
                "example": "Sugirió mejorar el proceso.",
            },
        ],
        "best": "exigir",
        "contrast": "Exigir es más fuerte y formal que pedir o sugerir.",
    },
]

GRAMMAR_MICRODRILLS = [
    {
        "focus": "Gender agreement",
        "prompt": "Selecciona la opción correcta: La reunión fue ___ y productiva.",
        "options": ["intenso", "intensa", "intensas"],
        "answer": "intensa",
        "explanation": "Reunión es femenino singular, por eso requiere intensa.",
        "examples": [
            "La discusión fue intensa.",
            "La agenda estuvo cargada.",
        ],
    },
    {
        "focus": "Verb tense",
        "prompt": "Completa: Si ___ más tiempo, habría terminado el informe.",
        "options": ["tengo", "tenía", "tuviera"],
        "answer": "tuviera",
        "explanation": "Condicional con si requiere imperfecto de subjuntivo.",
        "examples": [
            "Si tuviera apoyo, lo haría.",
            "Si fuera posible, lo ajustamos.",
        ],
    },
    {
        "focus": "Ser vs estar",
        "prompt": "El plan ___ listo, pero los recursos aún no.",
        "options": ["está", "es", "son"],
        "answer": "está",
        "explanation": "Estados temporales usan estar.",
        "examples": [
            "El equipo está listo.",
            "La sala está ocupada.",
        ],
    },
    {
        "focus": "Preposition choice",
        "prompt": "Depende ___ la aprobación del comité.",
        "options": ["de", "en", "por"],
        "answer": "de",
        "explanation": "El verbo depender se construye con de.",
        "examples": [
            "Depende de ti.",
            "Depende del presupuesto.",
        ],
    },
]

OUTPUT_PROMPTS = [
    {
        "title": "Operational update",
        "requirements": [
            "Usa 2 verbos precisos del banco.",
            "Incluye 1 conector concesivo (aunque/si bien).",
            "Usa 2 palabras del dominio elegido.",
        ],
        "prompt": "Escribe un update de 6-8 líneas para el equipo sobre un retraso en el proyecto.",
    },
    {
        "title": "Client negotiation note",
        "requirements": [
            "Usa 1 verbo de negociación.",
            "Incluye una frase de mitigación (quizá, tal vez, me parece).",
            "Evita calcos del inglés.",
        ],
        "prompt": "Redacta una respuesta breve a un cliente que pide más alcance sin ampliar plazos.",
    },
]

COMMON_MISTAKES = [
    {
        "pattern": "dependen en",
        "correction": "dependen de",
        "explanation": "El verbo depender siempre va con de.",
        "examples": ["Depende de la aprobación.", "Dependemos de su respuesta."],
    },
    {
        "pattern": "tomar una decisión en",
        "correction": "tomar una decisión sobre",
        "explanation": "En español, tomar una decisión sobre un tema es más natural.",
        "examples": [
            "Tomamos una decisión sobre el presupuesto.",
            "Tomó una decisión sobre el contrato.",
        ],
    },
    {
        "pattern": "la problema",
        "correction": "el problema",
        "explanation": "Problema es masculino pese a terminar en -a.",
        "examples": ["El problema fue resuelto.", "El problema persiste."],
    },
]

ADAPTIVE_QUESTION_BANK = [
    {
        "pair": "me da la impresión de que",
        "type": "fixed phrase",
        "frame": "___ no estaban listos para el cambio.",
        "options": ["Me da la impresión de que", "Me hace pensar que"],
        "native": "Me da la impresión de que",
        "rewrite": "Me da la impresión de que el equipo necesita más tiempo.",
    },
]

CONVERSATION_SCENARIOS = [
    {
        "title": "Negotiating scope creep",
        "roles": "You are a product lead; the client wants more features without timeline changes.",
        "constraints": [
            "Use 3 concessive structures (aunque, si bien, a pesar de).",
            "Maintain formal usted throughout.",
            "Avoid English-like calques.",
        ],
    },
    {
        "title": "Soft disagreement in a meeting",
        "roles": "You disagree with a peer but need to keep collaboration.",
        "constraints": [
            "Include 2 softeners (quizá, me parece, tal vez).",
            "Use one redirecting phrase (en todo caso, de todos modos).",
        ],
    },
]

WRITING_GUIDE = [
    {
        "pattern": "muy importante",
        "replacement": "crucial",
        "category": "lexical choice",
        "reason": "Increase lexical sophistication.",
    },
    {
        "pattern": "pienso que",
        "replacement": "considero que",
        "category": "register",
        "reason": "More formal stance marker.",
    },
    {
        "pattern": "pero",
        "replacement": "sin embargo",
        "category": "cohesion",
        "reason": "Stronger discourse connector.",
    },
]

ARGUMENTATION_TOPICS = [
    "La inteligencia artificial en la educación superior",
    "Teletrabajo y productividad en empresas globales",
    "Políticas de movilidad urbana sostenible",
]

DIALECT_MODULES = {
    "Spain": {
        "features": ["distinción /θ/ vs /s/", "leísmo moderado", "tú predominante"],
        "lexicon": {"ordenador": "computer", "coger": "to take", "vale": "okay"},
        "sample": "Vale, luego te llamo para concretar los detalles.",
        "trap": {
            "question": "¿Qué matiz tiene 'vale' aquí?",
            "options": ["confirmación informal", "desacuerdo", "sorpresa"],
            "answer": "confirmación informal",
        },
    },
    "Mexico": {
        "features": ["seseo", "ustedes generalizado", "diminutivos frecuentes"],
        "lexicon": {"computadora": "computer", "platicar": "to chat", "ahorita": "soon-ish"},
        "sample": "Ahorita lo revisamos y te aviso.",
        "trap": {
            "question": "¿Qué implica 'ahorita' en este contexto?",
            "options": ["inmediatamente", "pronto, pero flexible", "mañana"],
            "answer": "pronto, pero flexible",
        },
    },
    "River Plate": {
        "features": ["voseo", "entonación rioplatense", "yeísmo rehilado"],
        "lexicon": {"vos": "you", "laburo": "work", "che": "hey"},
        "sample": "Che, ¿vos venís a la reunión o laburás desde casa?",
        "trap": {
            "question": "¿Qué marca el uso de 'vos'?",
            "options": ["voseo", "formalidad", "plural"],
            "answer": "voseo",
        },
    },
    "Caribbean": {
        "features": ["aspiration of /s/", "fast rhythm", "tuteo predominante"],
        "lexicon": {"guagua": "bus", "china": "orange", "chévere": "cool"},
        "sample": "La guagua viene llena, pero está chévere el plan.",
        "trap": {
            "question": "¿Qué significa 'chévere' aquí?",
            "options": ["molesto", "agradable", "lento"],
            "answer": "agradable",
        },
    },
    "Andes": {
        "features": ["intonation rise", "use of 'pues'", "leísmo parcial"],
        "lexicon": {"chompa": "sweater", "anticucho": "street food", "pues": "emphasis"},
        "sample": "Sí, pues, mañana nos vemos temprano.",
        "trap": {
            "question": "¿Qué función cumple 'pues'?",
            "options": ["énfasis", "negación", "finalizar"],
            "answer": "énfasis",
        },
    },
}

LISTENING_SCENARIOS = [
    {
        "title": "Fast overlap meeting",
        "audio": "Bueno, sí, pero—no, espera, lo que digo es que el cliente quiere otra cosa.",
        "tasks": [
            {
                "question": "¿Qué cambió de postura la persona?",
                "options": [
                    "Se contradijo y reformuló.",
                    "Aceptó la propuesta sin reservas.",
                    "Se negó a hablar.",
                ],
                "answer": "Se contradijo y reformuló.",
            },
            {
                "question": "Identifica un suavizador.",
                "options": ["bueno", "espera", "cliente"],
                "answer": "bueno",
            },
        ],
    },
    {
        "title": "Street interview",
        "audio": "Pues, la verdad, no sé, como que al final me convencieron.",
        "tasks": [
            {
                "question": "¿Qué implica 'como que'?",
                "options": ["hedging", "certeza", "ironía"],
                "answer": "hedging",
            }
        ],
    },
]

WEEKLY_MISSIONS = [
    {
        "week": "Week 1",
        "title": "Secure a rental apartment",
        "brief": "Convince a landlord you are reliable, negotiate utilities, and clarify lease clauses.",
        "stakes": "Landlord skeptical due to high demand.",
        "skills": ["politeness", "hedging", "formal register", "negotiation"],
        "constraints": [
            "Use usted + formal greetings.",
            "Include 2 hedging phrases.",
            "Ask for clarification on a clause.",
        ],
    },
    {
        "week": "Week 2",
        "title": "Negotiate a contract clause",
        "brief": "You must push back on liability while preserving the partnership.",
        "stakes": "Legal counsel is firm on indemnity language.",
        "skills": ["diplomacy", "persuasion", "connector control", "tone"],
        "constraints": [
            "Offer a compromise with conditional language.",
            "Use 2 contrastive connectors.",
            "Avoid direct blame.",
        ],
    },
    {
        "week": "Week 3",
        "title": "Defend a thesis point",
        "brief": "Respond to committee doubts with evidence and respectful firmness.",
        "stakes": "Defense panel challenges your methodology.",
        "skills": ["academic register", "certainty control", "stance"],
        "constraints": [
            "Use 2 evidential markers.",
            "Use one concession + rebuttal.",
            "Stay in academic register.",
        ],
    },
    {
        "week": "Week 4",
        "title": "Handle a customer escalation",
        "brief": "De-escalate a frustrated client and negotiate a timeline reset.",
        "stakes": "Client threatens to cancel.",
        "skills": ["empathy", "de-escalation", "clarity", "solution framing"],
        "constraints": [
            "Acknowledge emotion explicitly.",
            "Offer 2 concrete next steps.",
            "Use softeners to reduce friction.",
        ],
    },
]

INPUT_LIBRARY = [
    {
        "title": "Investigative podcast: housing market crisis",
        "type": "Podcast",
        "level": "C1",
        "tags": ["persuasion", "interruptions", "technical vocabulary", "economics"],
    },
    {
        "title": "Debate: AI policy in higher education",
        "type": "Debate",
        "level": "C2",
        "tags": ["stance", "irony", "connectors", "academic register"],
    },
    {
        "title": "Court snippet: contract liability dispute",
        "type": "Court audio",
        "level": "C2",
        "tags": ["formal register", "precision", "hedging", "legal vocabulary"],
    },
    {
        "title": "Street interview: rent negotiations",
        "type": "Interview",
        "level": "C1",
        "tags": ["slang", "politeness", "interruptions", "negotiation"],
    },
    {
        "title": "Op-ed: customer service under pressure",
        "type": "Op-ed",
        "level": "C1",
        "tags": ["tone", "politeness", "blame control", "connectors"],
    },
    {
        "title": "Stand-up set: workplace miscommunication",
        "type": "Stand-up",
        "level": "C1",
        "tags": ["irony", "stance", "slang", "timing"],
    },
]

RELATIONSHIP_PERSONAS = [
    {
        "name": "María (Landlord)",
        "role": "Landlord",
        "relationship": "Cautiously open, wants reassurance about stability.",
        "tendencies": ["formal register", "expects concise answers", "likes polite hedging"],
    },
    {
        "name": "Sergio (Boss)",
        "role": "Boss",
        "relationship": "Direct, time-constrained, expects solutions.",
        "tendencies": ["prefers decisive tone", "low tolerance for vagueness"],
    },
    {
        "name": "Lucía (Colleague)",
        "role": "Colleague",
        "relationship": "Collaborative, values soft disagreement.",
        "tendencies": ["prefers inclusive language", "sensitive to bluntness"],
    },
]

LIVE_MODE_SCENARIOS = [
    {
        "title": "Overlapping stand-up update",
        "prompt": "Your teammate interrupts twice while you defend a timeline.",
        "focus": ["turn-taking", "speed", "assertiveness"],
    },
    {
        "title": "Angry customer call",
        "prompt": "Customer complains loudly while you propose a fix.",
        "focus": ["de-escalation", "empathy", "clarity"],
    },
    {
        "title": "Academic Q&A",
        "prompt": "Panel interrupts with rapid-fire follow-up questions.",
        "focus": ["certainty control", "evidence", "register"],
    },
]


def set_theme() -> None:
    st.set_page_config(page_title="VivaLingo Pro", page_icon="🗣️", layout="wide")
    st.markdown(
        """
        <style>
        :root {
            --primary: #1f3a8a;
            --secondary: #38bdf8;
            --accent: #f97316;
            --surface: #ffffff;
            --surface-muted: #f8fafc;
            --ink: #0f172a;
            --muted: #64748b;
            --border: rgba(148, 163, 184, 0.3);
        }
        .stApp {
            background: radial-gradient(circle at top left, #e0f2fe 0%, #f8fafc 45%, #ecfeff 100%);
            color: var(--ink);
            font-family: "Inter", "SF Pro Text", "Segoe UI", system-ui, -apple-system, sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: var(--ink);
        }
        .hero {
            padding: 2.2rem;
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(31, 58, 138, 0.92), rgba(56, 189, 248, 0.9));
            color: #fff;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.16);
        }
        .hero p {
            color: rgba(255, 255, 255, 0.85);
            font-size: 1.05rem;
        }
        .pill {
            display: inline-block;
            padding: 0.2rem 0.75rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            font-weight: 600;
            margin-right: 0.4rem;
        }
        .card {
            padding: 1.4rem;
            border-radius: 20px;
            border: 1px solid var(--border);
            background: var(--surface);
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
        }
        .card-muted {
            padding: 1.2rem;
            border-radius: 18px;
            border: 1px dashed rgba(148, 163, 184, 0.6);
            background: var(--surface-muted);
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }
        .wave-box {
            border-radius: 18px;
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 1rem;
        }
        .shadow-pill {
            display: inline-flex;
            align-items: center;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.2);
            color: #0c4a6e;
            font-weight: 600;
            margin-right: 0.4rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-weight: 600;
            margin-right: 0.4rem;
        }
        section[data-testid="stSidebar"] .stButton button:hover {
            border-color: rgba(56, 189, 248, 0.6);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    if "profile" not in st.session_state:
        st.session_state.profile = {
            "name": "",
            "level": "C1",
            "weekly_goal": 6,
            "last_gap_week": None,
        }
    if "assessment" not in st.session_state:
        st.session_state.assessment = {
            "active": False,
            "last_completed": None,
        }
    if "gap_results" not in st.session_state:
        st.session_state.gap_results = []
    if "adaptive_focus" not in st.session_state:
        st.session_state.adaptive_focus = []
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = load_portfolio()
    if "writing_analysis" not in st.session_state:
        st.session_state.writing_analysis = {"draft": "", "edits": []}
    if "relationship_memory" not in st.session_state:
        st.session_state.relationship_memory = {
            persona["name"]: {"notes": [], "tendencies": persona["tendencies"]}
            for persona in RELATIONSHIP_PERSONAS
        }
    if "live_mode" not in st.session_state:
        st.session_state.live_mode = {"last_speed": 1.0, "last_complexity": 1.0}
    if "review_queue" not in st.session_state:
        st.session_state.review_queue = {}
    if "review_step" not in st.session_state:
        st.session_state.review_step = 0
    if "mistake_log" not in st.session_state:
        st.session_state.mistake_log = {}
    if "domain_exposure" not in st.session_state:
        st.session_state.domain_exposure = {d["domain"]: 0 for d in TOPIC_DIVERSITY_DOMAINS}
    if "grammar_review_queue" not in st.session_state:
        st.session_state.grammar_review_queue = {}
    if "grammar_review_step" not in st.session_state:
        st.session_state.grammar_review_step = 0
    if "mistake_notebook" not in st.session_state:
        st.session_state.mistake_notebook = []
    if "daily_mission_history" not in st.session_state:
        st.session_state.daily_mission_history = []
    if "speaking_minutes" not in st.session_state:
        st.session_state.speaking_minutes = 0
    if "active_vocab" not in st.session_state:
        st.session_state.active_vocab = set()
    if "active_verbs" not in st.session_state:
        st.session_state.active_verbs = set()
    if "error_review_queue" not in st.session_state:
        st.session_state.error_review_queue = {}
    if "error_review_step" not in st.session_state:
        st.session_state.error_review_step = 0


def load_portfolio() -> dict:
    if not PORTFOLIO_PATH.exists():
        return {
            "writing_samples": [],
            "recordings": [],
            "transcripts": [],
            "benchmarks": [],
        }
    return json.loads(PORTFOLIO_PATH.read_text(encoding="utf-8"))


def save_portfolio() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_PATH.write_text(json.dumps(st.session_state.portfolio, indent=2), encoding="utf-8")


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vocab_items (
                term TEXT PRIMARY KEY,
                meaning TEXT,
                example TEXT,
                domain TEXT,
                register TEXT,
                part_of_speech TEXT,
                created_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT,
                correction TEXT,
                tag TEXT,
                user_text TEXT,
                corrected_text TEXT,
                confidence REAL,
                created_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transcript TEXT,
                created_at TEXT
            )
            """
        )


def save_vocab_item(item: dict) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO vocab_items
            (term, meaning, example, domain, register, part_of_speech, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["term"],
                item.get("meaning"),
                item.get("example"),
                item.get("domain"),
                item.get("register"),
                item.get("pos"),
                date.today().isoformat(),
            ),
        )


def save_mistake_entry(entry: dict) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO mistakes
            (pattern, correction, tag, user_text, corrected_text, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry["pattern"],
                entry["correction"],
                entry["tag"],
                entry.get("user_text"),
                entry.get("corrected_text"),
                entry["confidence"],
                entry["date"],
            ),
        )


def save_transcript(text: str) -> None:
    if not text.strip():
        return
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO transcripts (transcript, created_at) VALUES (?, ?)",
            (text, date.today().isoformat()),
        )


def seed_for_week(week: date, name: str) -> int:
    base = f"{week.isoformat()}:{name}"
    return int(hashlib.sha256(base.encode("utf-8")).hexdigest()[:8], 16)


def generate_gap_results(scores: dict[str, int]) -> list[DiagnosticIssue]:
    weights = {
        issue: (6 - scores.get(issue.area, 3)) * random.uniform(0.8, 1.2)
        for issue in DIAGNOSTIC_ISSUES
    }
    ranked = sorted(DIAGNOSTIC_ISSUES, key=lambda issue: weights[issue], reverse=True)
    return ranked[:20]


def derive_adaptive_focus(scores: dict[str, int]) -> list[str]:
    focus = [area for area, score in scores.items() if score <= 3]
    return focus or ["Nuance & pragmatics", "Register & tone"]


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div>
                <span class="pill">C1–C2 Diagnostics</span>
                <span class="pill">Prosody Coach</span>
                <span class="pill">Native Corpus</span>
            </div>
            <h1>VivaLingo Pro: Spanish Mastery Lab</h1>
            <p>Train nuance, register, collocation accuracy, and real-world fluency with adaptive diagnostics and
            portfolio-ready evidence.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_profile_sidebar() -> None:
    st.sidebar.header("Learner Profile")
    profile = st.session_state.profile
    assessment = st.session_state.assessment
    profile["name"] = st.sidebar.text_input("Name", value=profile["name"], placeholder="Your name")
    profile["level"] = st.sidebar.selectbox("Target level", ["C1", "C2"], index=0)
    profile["weekly_goal"] = st.sidebar.slider("Weekly sessions", 2, 10, profile["weekly_goal"])
    assessment["active"] = st.sidebar.toggle("Activate adaptive mode", value=assessment["active"])
    if assessment["active"]:
        st.sidebar.success("Adaptive mode is on.")
    else:
        st.sidebar.info("Turn on adaptive mode to unlock weekly missions.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")

    if not assessment["active"]:
        st.sidebar.caption("Complete the activation to enable personalized missions.")

def render_gap_finder() -> None:
    st.header("Real-time gap-finder diagnostics")
    st.write("Weekly adaptive tests targeting collocations, prepositions, discourse markers, register, and nuance.")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        week = st.date_input("Week of", value=date.today())
        st.caption("Diagnostics adapt weekly to C1–C2 micro-skills.")
        scores = {}
        for area in DIAGNOSTIC_AREAS:
            scores[area] = st.slider(f"Self-assess {area}", 1, 5, 3)
    with col2:
        st.markdown("#### Diagnostic Focus")
        st.markdown("- Collocation strength\n- Preposition precision\n- Discourse cohesion\n- Register control\n- Pragmatic nuance")
        run = st.button("Run adaptive diagnostics")

    if run:
        random.seed(seed_for_week(week, st.session_state.profile["name"]))
        st.session_state.gap_results = generate_gap_results(scores)
        st.session_state.profile["last_gap_week"] = week.isoformat()
        st.session_state.adaptive_focus = derive_adaptive_focus(scores)

    if st.session_state.gap_results:
        st.subheader("Error Top 20")
        table = [
            {
                "Rank": idx + 1,
                "Area": issue.area,
                "Pattern": issue.pattern,
                "Impact": issue.impact,
                "Native corpus example": issue.example,
                "Fix": issue.fix,
            }
            for idx, issue in enumerate(st.session_state.gap_results)
        ]
        st.dataframe(table, use_container_width=True)

        st.subheader("Personalized training plan")
        for area in DIAGNOSTIC_AREAS:
            st.markdown(f"**{area}**")
            for item in TRAINING_PLAN[area]:
                st.markdown(f"- {item}")


def score_register_response(text: str, style: str) -> dict[str, int]:
    lowered = text.lower()
    scores = {dim: 2 for dim in RUBRIC_DIMENSIONS}
    if any(marker in lowered for marker in REGISTER_MARKERS["politeness"]):
        scores["Politeness strategies"] += 2
    if any(marker in lowered for marker in REGISTER_MARKERS["hedging"]):
        scores["Hedging"] += 2
    if any(marker in lowered for marker in REGISTER_MARKERS["direct"]):
        scores["Directness"] += 1
    if any(marker in lowered for marker in REGISTER_MARKERS["idiomatic"]):
        scores["Idiomaticity"] += 2
    if style == "Academic abstract" and any(marker in lowered for marker in REGISTER_MARKERS["academic"]):
        scores["Audience fit"] += 3
    if style == "Informal WhatsApp" and any(marker in lowered for marker in REGISTER_MARKERS["whatsapp"]):
        scores["Audience fit"] += 3
    if style == "Persuasive pitch" and any(marker in lowered for marker in REGISTER_MARKERS["pitch"]):
        scores["Audience fit"] += 3
    if len(text.split()) > 55:
        scores["Directness"] += 1
    return {k: min(v, 5) for k, v in scores.items()}


def render_register_simulator() -> None:
    st.header("Register & tone mastery simulator")
    prompt = st.text_area(
        "Scenario prompt",
        value="You need to convince a skeptical team to adopt a new workflow.",
        height=90,
    )

    responses = {}
    for style in REGISTER_STYLES:
        responses[style] = st.text_area(f"{style} response", key=f"register-{style}")

    if st.button("Score responses"):
        rows = []
        for style, text in responses.items():
            scores = score_register_response(text, style)
            rows.append({"Register": style, **scores})
        st.dataframe(rows, use_container_width=True)
        st.markdown("**Rubric guidance**")
        st.markdown(
            "- *Politeness strategies*: modals, gratitude, deference.\n"
            "- *Hedging*: quizá, tal vez, me parece.\n"
            "- *Directness*: strong imperatives lower score in formal contexts.\n"
            "- *Idiomaticity*: natural phraseology and discourse frames.\n"
            "- *Audience fit*: match lexical density and formality to register."
        )

def render_pronunciation_coach() -> None:
    st.header("High-precision pronunciation & prosody coach")
    target = st.selectbox("Shadowing prompt", [item["phrase"] for item in PRONUNCIATION_TARGETS])
    details = next(item for item in PRONUNCIATION_TARGETS if item["phrase"] == target)
    st.markdown("**Focus areas:** " + ", ".join(details["focus"]))
    st.info(details["notes"])

    phrase_chunks = [chunk.strip() for chunk in target.split(",") if chunk.strip()]
    st.markdown("#### Shadowing mode")
    loop_count = st.slider("Replay loops", 1, 5, 2)

    components.html(
        f"""
        <div class="wave-box">
            <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:10px;">
                {''.join([f'<span class="shadow-pill">{chunk}</span>' for chunk in phrase_chunks])}
            </div>
            <svg width="100%" height="120" viewBox="0 0 600 120" preserveAspectRatio="none">
                <polyline fill="none" stroke="#38bdf8" stroke-width="3"
                    points="0,60 40,55 80,70 120,40 160,60 200,30 240,65 280,50 320,80 360,55 400,65 440,35 480,60 520,45 560,70 600,50" />
                <polyline fill="none" stroke="#f97316" stroke-width="2" stroke-dasharray="6 4"
                    points="0,90 40,85 80,95 120,70 160,85 200,65 240,92 280,75 320,100 360,80 400,88 440,70 480,85 520,78 560,92 600,80" />
            </svg>
            <div style="font-size:12px; color:#64748b;">Waveform (blue) & pitch track (orange)</div>
            <button id="shadow-play" style="margin-top:8px; padding:8px 12px; border-radius:8px; border:1px solid #cbd5f5;">▶️ Play & loop</button>
            <div id="shadow-status" style="margin-top:6px; font-size:13px; color:#0f172a;"></div>
        </div>
        <script>
            const button = document.getElementById('shadow-play');
            const status = document.getElementById('shadow-status');
            const utteranceText = {json.dumps(target)};
            const loops = {loop_count};
            button.onclick = () => {{
                let count = 0;
                status.textContent = `Loop 1 / ${loops}`;
                const speakOnce = () => {{
                    const utterance = new SpeechSynthesisUtterance(utteranceText);
                    utterance.lang = 'es-ES';
                    utterance.onend = () => {{
                        count += 1;
                        if (count < loops) {{
                            status.textContent = `Loop ${count + 1} / ${loops}`;
                            speakOnce();
                        }} else {{
                            status.textContent = 'Done. Replay to continue shadowing.';
                        }}
                    }};
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(utterance);
                }};
                speakOnce();
            }};
        </script>
        """,
        height=280,
    )


def render_collocation_engine() -> None:
    st.header("Native-corpus collocation engine")
    tabs = st.tabs(["Choose-the-more-native", "Rewrite to sound native", "Collocation completion"])

    with tabs[0]:
        item = random.choice(COLLOCATION_SETS)
        st.markdown(f"**{item['pair']}** ({item['type']})")
        choice = st.radio("Which is more native?", item["options"], key="collocation-choice")
        if st.button("Check", key="collocation-check"):
            st.success("Correct!" if choice == item["native"] else "Not quite.")
            st.caption(f"Native choice: {item['native']} • Example: {item['rewrite']}")

    with tabs[1]:
        item = random.choice(COLLOCATION_SETS)
        st.markdown(f"Rewrite using: **{item['pair']}**")
        rewrite = st.text_area("Your rewrite", value="", key="rewrite-native")
        if st.button("Show model", key="rewrite-show"):
            st.info(item["rewrite"])
            st.caption("Compare rhythm, verb choice, and fixed frames.")

    with tabs[2]:
        item = random.choice(COLLOCATION_SETS)
        st.markdown(item["frame"])
        completion = st.text_input("Fill in the blank", key="collocation-fill")
        if st.button("Reveal", key="collocation-reveal"):
            st.success(f"Suggested: {item['native']}")
            st.caption(f"Full example: {item['rewrite']}")


def render_mission_control() -> None:
    st.header("Weekly mission control")
    st.write("Every week you enter a real-world mission that adapts to your slips.")

    if not st.session_state.assessment["active"]:
        st.info("Activate adaptive mode in the sidebar to unlock mission constraints.")
        return

    mission = st.selectbox("Choose your weekly mission", WEEKLY_MISSIONS, format_func=lambda m: f"{m['week']}: {m['title']}")
    st.markdown(f"**Brief:** {mission['brief']}")
    st.markdown(f"**Stakes:** {mission['stakes']}")
    st.markdown("**Core skills:** " + ", ".join(mission["skills"]))

    adaptive_constraints = {
        "Collocations": "Use 2 precise collocations from your gap list.",
        "Prepositions": "Avoid preposition mismatches (de/en/por/para).",
        "Discourse markers": "Use at least 3 discourse connectors.",
        "Register & tone": "Maintain consistent register for the whole response.",
        "Nuance & pragmatics": "Include softeners and avoid unintended blame.",
    }
    focus = st.session_state.adaptive_focus or ["Nuance & pragmatics"]
    st.markdown("**Adaptive constraints (tighten where you slipped)**")
    for area in focus:
        st.markdown(f"- {adaptive_constraints.get(area, 'Maintain clarity and precision.')}")

    st.markdown("**Mission constraints**")
    for constraint in mission["constraints"]:
        st.markdown(f"- {constraint}")

    st.text_area("Draft your mission response", height=180, key="mission-response")
    st.caption("Your mission response will be evaluated for register, hedging, and connector control.")


def render_adaptive_input_selection() -> None:
    st.header("Adaptive input selection")
    st.write("Authentic inputs are chosen based on your errors, not generic lessons.")

    tag_pool = sorted({tag for item in INPUT_LIBRARY for tag in item["tags"]})
    default_tags = []
    if st.session_state.adaptive_focus:
        focus_to_tags = {
            "Register & tone": ["formal register", "tone"],
            "Nuance & pragmatics": ["stance", "politeness", "blame control"],
            "Discourse markers": ["connectors"],
            "Collocations": ["technical vocabulary"],
            "Prepositions": ["precision"],
        }
        for focus in st.session_state.adaptive_focus:
            default_tags += focus_to_tags.get(focus, [])
    selected_tags = st.multiselect("Skills to target", tag_pool, default=list(dict.fromkeys(default_tags)))
    target_level = st.selectbox("Target input level", ["C1", "C2"])

    filtered = []
    for item in INPUT_LIBRARY:
        if item["level"] != target_level:
            continue
        overlap = len(set(item["tags"]) & set(selected_tags))
        filtered.append((overlap, item))
    filtered.sort(key=lambda x: x[0], reverse=True)

    st.markdown("**Recommended inputs at your edge**")
    for overlap, item in filtered:
        st.markdown(
            f"""
            <div class="card" style="margin-bottom:12px;">
                <h4>{item['title']}</h4>
                <p><strong>Type:</strong> {item['type']} • <strong>Level:</strong> {item['level']}</p>
                <p><strong>Skills:</strong> {", ".join(item["tags"])}</p>
                <p><strong>Match score:</strong> {overlap} skill tags</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_nuance_feedback() -> None:
    st.header("Nuance-first feedback lab")
    st.write("Compare what you intended to imply vs what you actually implied.")

    intent = st.text_area("Intended meaning", height=90, key="nuance-intent")
    message = st.text_area("Your message", height=120, key="nuance-message")
    stance = st.selectbox(
        "Target stance",
        ["Diplomatic", "Firm", "Skeptical", "Enthusiastic", "Neutral"],
    )

    if st.button("Analyze nuance"):
        lowered = message.lower()
        polite_markers = sum(marker in lowered for marker in REGISTER_MARKERS["politeness"])
        hedging_markers = sum(marker in lowered for marker in REGISTER_MARKERS["hedging"])
        blame_markers = sum(word in lowered for word in ["culpa", "fallo", "responsable"])
        certainty = "high" if "sin duda" in lowered or "claramente" in lowered else "medium"
        tone = "soft" if hedging_markers else "direct"

        st.subheader("Implication profile")
        st.write(
            [
                {"Signal": "Politeness", "Level": "high" if polite_markers else "low"},
                {"Signal": "Hedging", "Level": "present" if hedging_markers else "absent"},
                {"Signal": "Certainty", "Level": certainty},
                {"Signal": "Blame risk", "Level": "elevated" if blame_markers else "low"},
                {"Signal": "Emotional tone", "Level": tone},
            ]
        )

        st.markdown("**Mismatch check**")
        if intent and message and intent.lower() not in message.lower():
            st.warning("Your message may not reflect the intended meaning. Add explicit stance markers.")
        else:
            st.success("Message aligns with your intended meaning.")

    st.markdown("**Rephrase drill**")
    drill = st.selectbox(
        "Rephrase the same message as:",
        ["Softer", "Firmer", "More diplomatic", "More skeptical", "More enthusiastic", "More neutral"],
    )
    st.text_area("Rewrite here", height=120, key=f"nuance-drill-{drill}")
    st.caption(f"Target stance: {stance} • Drill mode: {drill}")


def render_relationship_memory() -> None:
    st.header("Relationship & persona memory")
    st.write("Stay consistent with personas across weeks and adapt to your tendencies.")

    persona_name = st.selectbox("Choose a partner", [p["name"] for p in RELATIONSHIP_PERSONAS])
    persona = next(p for p in RELATIONSHIP_PERSONAS if p["name"] == persona_name)
    memory = st.session_state.relationship_memory[persona_name]

    st.markdown(f"**Role:** {persona['role']}")
    st.markdown(f"**Relationship status:** {persona['relationship']}")
    st.markdown("**Known tendencies**")
    st.write(memory["tendencies"])

    note = st.text_area("Log a new interaction note", height=100)
    tendency_flags = st.multiselect(
        "Observed tendencies in your speech",
        ["too direct", "too formal", "over-hedging", "weak turn-taking", "awkward closings"],
    )
    if st.button("Save interaction"):
        if note.strip():
            memory["notes"].append(
                {"date": date.today().isoformat(), "note": note, "flags": tendency_flags}
            )
            st.success("Saved. Your future missions will reflect this relationship history.")
        else:
            st.info("Add a note to save the interaction.")

    if memory["notes"]:
        st.subheader("Relationship history")
        st.dataframe(memory["notes"], use_container_width=True)


def render_live_mode() -> None:
    st.header("Live mode: speed + messiness mastery")
    st.write("Real-time pace with overlaps, fillers, and timed responses.")

    scenario = st.selectbox("Scenario", [s["title"] for s in LIVE_MODE_SCENARIOS])
    selected = next(s for s in LIVE_MODE_SCENARIOS if s["title"] == scenario)
    st.markdown(f"**Prompt:** {selected['prompt']}")
    st.markdown("**Focus:** " + ", ".join(selected["focus"]))

    speed = st.slider("Audio speed multiplier", 0.8, 1.6, 1.0, 0.1)
    complexity = st.slider("Content complexity", 1, 5, 3)
    response_time = st.slider("Response time (seconds)", 10, 60, 25)

    if st.button("Start live drill"):
        st.session_state.live_mode["last_speed"] = speed
        st.session_state.live_mode["last_complexity"] = complexity
        st.info(
            f"Play the audio at {speed}× speed. Respond within {response_time}s. "
            f"Keep {complexity}/5 complexity."
        )
        st.progress(0.0, text="Timer ready — respond aloud, then debrief.")
    st.caption("Adaptive pacing: raise speed before complexity if time pressure is the issue.")


def analyze_constraints(response: str, constraints: list[str]) -> dict[str, bool]:
    lowered = response.lower()
    results = {}
    concessives = ["aunque", "si bien", "a pesar de", "no obstante"]
    softeners = ["quizá", "tal vez", "me parece", "podría"]
    redirect = ["en todo caso", "de todos modos", "en cualquier caso"]

    for constraint in constraints:
        if "concessive" in constraint.lower():
            results[constraint] = sum(phrase in lowered for phrase in concessives) >= 3
        elif "softeners" in constraint.lower():
            results[constraint] = sum(phrase in lowered for phrase in softeners) >= 2
        elif "redirecting" in constraint.lower():
            results[constraint] = any(phrase in lowered for phrase in redirect)
        elif "formal usted" in constraint.lower():
            results[constraint] = "usted" in lowered or "su " in lowered
        elif "Avoid English-like calques" in constraint:
            results[constraint] = "aplicar para" not in lowered
        else:
            results[constraint] = False
    return results


def render_conversation_lab() -> None:
    st.header("Advanced conversation lab with constraints")
    scenario = st.selectbox("Choose a roleplay", [s["title"] for s in CONVERSATION_SCENARIOS])
    selected = next(s for s in CONVERSATION_SCENARIOS if s["title"] == scenario)

    st.markdown("**Roleplay brief**")
    st.write(selected["roles"])
    st.markdown("**Constraints**")
    for constraint in selected["constraints"]:
        st.markdown(f"- {constraint}")

    response = st.text_area("Your response", height=160, key="conversation-response")
    if st.button("Evaluate constraints"):
        checks = analyze_constraints(response, selected["constraints"])
        for constraint, passed in checks.items():
            st.write(f"{'✅' if passed else '❌'} {constraint}")
        score = sum(checks.values()) / max(len(checks), 1)
        st.metric("Constraint completion", f"{score:.0%}")
        st.caption("Improve by weaving softeners, concessions, and register markers.")


def generate_edit_trail(text: str) -> list[dict]:
    edits = []
    for guide in WRITING_GUIDE:
        if guide["pattern"] in text:
            edited = text.replace(guide["pattern"], guide["replacement"])
            edits.append(
                {
                    "before": guide["pattern"],
                    "after": guide["replacement"],
                    "category": guide["category"],
                    "reason": guide["reason"],
                    "preview": edited,
                }
            )
    if not edits and text:
        edits.append(
            {
                "before": "(sentence cohesion)",
                "after": "Add connector: sin embargo",
                "category": "cohesion",
                "reason": "Improve logical flow between sentences.",
                "preview": text,
            }
        )
    return edits


def render_writing_studio() -> None:
    st.header("Error-aware writing studio with edit trails")
    st.write("Write 300–1000 words and receive line edits with reasoning categories.")
    draft = st.text_area("Your draft", height=220, key="writing-draft")

    if st.button("Analyze writing"):
        st.session_state.writing_analysis = {
            "draft": draft,
            "edits": generate_edit_trail(draft),
        }

    if st.session_state.writing_analysis["draft"]:
        edits = st.session_state.writing_analysis["edits"]
        st.subheader("Line edits")
        st.dataframe(
            [
                {
                    "Before": edit["before"],
                    "After": edit["after"],
                    "Category": edit["category"],
                    "Reason": edit["reason"],
                }
                for edit in edits
            ],
            use_container_width=True,
        )
        if edits:
            diff = "\n".join(
                difflib.unified_diff(
                    st.session_state.writing_analysis["draft"].splitlines(),
                    edits[0]["preview"].splitlines(),
                    fromfile="before",
                    tofile="after",
                    lineterm="",
                )
            )
            st.subheader("Before/after diff")
            st.code(diff or "(No diff produced)")

        deck = {}
        for edit in edits:
            deck[edit["category"]] = deck.get(edit["category"], 0) + 1
        st.subheader("Spaced repetition deck")
        st.write(
            [
                {"Category": category, "Cards": count}
                for category, count in deck.items()
            ]
        )

        if st.session_state.writing_analysis["draft"].strip():
            if st.button("Save to portfolio"):
                st.session_state.portfolio["writing_samples"].append(
                    {
                        "date": date.today().isoformat(),
                        "text": st.session_state.writing_analysis["draft"],
                    }
                )
                save_portfolio()
                st.success("Saved to portfolio.")


def render_argumentation_drills() -> None:
    st.header("Argumentation & rhetoric drills")
    topic = st.selectbox("Choose a topic", ARGUMENTATION_TOPICS)
    st.write("Build a thesis, counterargument, concession, and conclusion using discourse connectors.")

    thesis = st.text_input("Thesis")
    counter = st.text_input("Counterargument")
    concession = st.text_input("Concession")
    conclusion = st.text_input("Conclusion")

    if st.button("Evaluate structure"):
        connector_count = sum(
            phrase in " ".join([thesis, counter, concession, conclusion]).lower()
            for phrase in ["por lo tanto", "sin embargo", "no obstante", "además", "en conclusión"]
        )
        length_score = sum(len(part.split()) > 6 for part in [thesis, counter, concession, conclusion])
        score = (connector_count + length_score) / 10
        st.metric("Argumentation score", f"{score:.0%}")
        st.caption("Improve cohesion by adding explicit stance markers and connectors.")


def render_dialect_tuning() -> None:
    st.header("Dialect & regional Spanish tuning")
    dialect = st.selectbox("Select region", list(DIALECT_MODULES.keys()))
    data = DIALECT_MODULES[dialect]

    st.markdown("**Core features**")
    st.write(", ".join(data["features"]))
    st.markdown("**Key lexicon**")
    st.table([{"Term": k, "Meaning": v} for k, v in data["lexicon"].items()])

    st.markdown("**Listening: same content across dialects**")
    for name, variant in DIALECT_MODULES.items():
        with st.expander(f"{name} variant"):
            st.write(variant["sample"])
            components.html(
                f"""
                <button id="dialect-{name}" style="padding:6px 10px; border-radius:8px; border:1px solid #cbd5f5;">🔊 Play</button>
                <script>
                    const btn = document.getElementById('dialect-{name}');
                    btn.onclick = () => {{
                        const utterance = new SpeechSynthesisUtterance({json.dumps(variant['sample'])});
                        utterance.lang = 'es-ES';
                        window.speechSynthesis.cancel();
                        window.speechSynthesis.speak(utterance);
                    }};
                </script>
                """,
                height=60,
            )

    st.markdown("**Comprehension trap**")
    trap = data["trap"]
    answer = st.radio(trap["question"], trap["options"], key="dialect-trap")
    if st.button("Check trap"):
        st.success("Correct!" if answer == trap["answer"] else "Try again.")


def render_listening_nuance() -> None:
    st.header("Listening for nuance: fast, messy, real")
    scenario_title = st.selectbox("Choose a scenario", [s["title"] for s in LISTENING_SCENARIOS])
    scenario = next(s for s in LISTENING_SCENARIOS if s["title"] == scenario_title)
    st.write(scenario["audio"])

    components.html(
        f"""
        <button id="nuance-audio" style="padding:6px 10px; border-radius:8px; border:1px solid #cbd5f5;">🔊 Play sample</button>
        <script>
            const btn = document.getElementById('nuance-audio');
            btn.onclick = () => {{
                const utterance = new SpeechSynthesisUtterance({json.dumps(scenario['audio'])});
                utterance.lang = 'es-ES';
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
            }};
        </script>
        """,
        height=60,
    )

    for idx, task in enumerate(scenario["tasks"]):
        choice = st.radio(task["question"], task["options"], key=f"nuance-{idx}")
        if st.button("Reveal", key=f"nuance-reveal-{idx}"):
            st.info(f"Answer: {task['answer']}")


def render_portfolio() -> None:
    st.header("Native-likeness benchmark & portfolio")
    st.write("Track progress across measurable axes and export your evidence.")

    axis_scores = {}
    for axis in PORTFOLIO_AXES:
        axis_scores[axis] = st.slider(axis, 1, 10, 6)

    if st.button("Save benchmark"):
        st.session_state.portfolio["benchmarks"].append(
            {"date": date.today().isoformat(), "scores": axis_scores}
        )
        save_portfolio()
        st.success("Benchmark saved.")

    if st.session_state.portfolio["benchmarks"]:
        st.subheader("Benchmark history")
        st.dataframe(st.session_state.portfolio["benchmarks"], use_container_width=True)

    st.subheader("Portfolio artifacts")
    st.write(f"Writing samples: {len(st.session_state.portfolio['writing_samples'])}")
    st.write(f"Recordings: {len(st.session_state.portfolio['recordings'])}")
    st.write(f"Conversation transcripts: {len(st.session_state.portfolio['transcripts'])}")

    if st.session_state.portfolio["writing_samples"]:
        st.markdown("**Latest writing sample**")
        st.text_area(
            "",
            value=st.session_state.portfolio["writing_samples"][-1]["text"],
            height=160,
            disabled=True,
        )

    export = json.dumps(st.session_state.portfolio, indent=2)
    st.download_button("Download portfolio JSON", data=export, file_name="vivalingo_portfolio.json")


def render_overview() -> None:
    st.header("Program Overview")
    st.write(
        "This lab integrates diagnostics, register calibration, prosody coaching, collocation accuracy,"
        " and portfolio-grade evidence for advanced Spanish learners."
    )

    shares = domain_coverage_share()
    domain_percent = {domain: f"{share:.0%}" for domain, share in shares.items()}
    active_vocab_count = len(st.session_state.active_vocab)
    active_verb_count = len(st.session_state.active_verbs)
    error_total = sum(item["count"] for item in st.session_state.mistake_log.values()) if st.session_state.mistake_log else 0

    st.markdown("### Progress that matters")
    st.markdown(
        """
        <div class="metric-grid">
            <div class="card">
                <h3>Domain coverage</h3>
                <p>Tracks how balanced your exposure is across themes.</p>
            </div>
            <div class="card">
                <h3>Verb range</h3>
                <p>Counts distinct precision verbs used in practice.</p>
            </div>
            <div class="card">
                <h3>Error trend</h3>
                <p>Shows top recurring errors and reduction over time.</p>
            </div>
            <div class="card">
                <h3>Speaking minutes</h3>
                <p>Manual tracking from daily missions.</p>
            </div>
            <div class="card">
                <h3>Active vocabulary</h3>
                <p>Items produced, not just recognized.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("**Domain coverage snapshot**")
    st.write(domain_percent)
    st.write(
        [
            {"Metric": "Verb range", "Value": len(DAILY_MISSION_VERBS)},
            {"Metric": "Active verbs used", "Value": active_verb_count},
            {"Metric": "Top errors logged", "Value": error_total},
            {"Metric": "Speaking minutes", "Value": st.session_state.speaking_minutes},
            {"Metric": "Active vocabulary", "Value": active_vocab_count},
        ]
    )

    st.markdown("### Fast navigation")
    if st.button("Do a 5-minute session"):
        st.session_state.quick_session = True
        st.success("Quick session ready. Jump to Growth Studio or Daily Missions.")

    st.markdown(
        """
        <div class="metric-grid">
            <div class="card">
                <h3>Weekly Mission Control</h3>
                <p>Real-life missions that tighten constraints where you slip and expand only after consistency.</p>
            </div>
            <div class="card">
                <h3>Adaptive Input Selection</h3>
                <p>Authentic content tagged by skills, auto-picked from your error patterns.</p>
            </div>
            <div class="card">
                <h3>Weekly Gap Finder</h3>
                <p>Adaptive C1–C2 diagnostics with ranked Error Top 20 and targeted training plan.</p>
            </div>
            <div class="card">
                <h3>Nuance Feedback Lab</h3>
                <p>Meaning vs implication feedback with rephrase drills for tone control.</p>
            </div>
            <div class="card">
                <h3>Prosody Coach</h3>
                <p>Shadowing with waveform + pitch tracks and looped playback.</p>
            </div>
            <div class="card">
                <h3>Growth Studio</h3>
                <p>Vocabulary expansion, verb precision, grammar drills, and output-first challenges.</p>
            </div>
            <div class="card">
                <h3>Relationship Memory</h3>
                <p>Track persona history, adjust to tendencies, stay consistent across weeks.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Placement & calibration")
    st.write("Short adaptive test to seed your first week.")
    calibration = st.radio(
        "Choose the most natural option",
        ["Tomamos una decisión.", "Hicimos una decisión.", "Dimos una decisión."],
    )
    if st.button("Save calibration"):
        st.session_state.profile["level"] = "C1" if calibration == "Tomamos una decisión." else "C1"
        st.success("Calibration saved. Adaptive missions will now reflect this baseline.")


def add_review_items(items: list[dict]) -> None:
    for item in items:
        item_id = item["term"]
        if item_id not in st.session_state.review_queue:
            st.session_state.review_queue[item_id] = {
                "term": item["term"],
                "meaning": item["meaning"],
                "example": item["example"],
                "domain": item.get("domain"),
                "register": item.get("register"),
                "pos": item.get("pos"),
                "streak": 0,
                "next_due": 0,
            }
            if item.get("domain"):
                record_domain_exposure(item["domain"])
            save_vocab_item(item)


def add_error_review_item(tag: str, entry: dict) -> None:
    queue = st.session_state.error_review_queue.setdefault(tag, [])
    entry_with_schedule = {
        **entry,
        "streak": 0,
        "next_due": st.session_state.error_review_step,
    }
    queue.append(entry_with_schedule)


def update_error_review_item(tag: str, index: int, success: bool) -> None:
    item = st.session_state.error_review_queue[tag][index]
    if success:
        item["streak"] += 1
    else:
        item["streak"] = 0
    item["next_due"] = st.session_state.error_review_step + (2 ** item["streak"])


def log_mistake(pattern: str, correction: str, user_text: str | None = None, corrected_text: str | None = None) -> None:
    log = st.session_state.mistake_log
    if pattern not in log:
        log[pattern] = {"correction": correction, "count": 0}
    log[pattern]["count"] += 1
    entry = {
        "date": date.today().isoformat(),
        "pattern": pattern,
        "correction": correction,
        "tag": ERROR_TAGS.get(pattern, "general"),
        "confidence": round(random.uniform(0.6, 0.95), 2),
        "user_text": user_text,
        "corrected_text": corrected_text,
    }
    st.session_state.mistake_notebook.append(entry)
    add_error_review_item(entry["tag"], entry)
    save_mistake_entry(entry)


def record_domain_exposure(domain: str) -> None:
    st.session_state.domain_exposure[domain] = st.session_state.domain_exposure.get(domain, 0) + 1


def domain_coverage_share() -> dict[str, float]:
    total = sum(st.session_state.domain_exposure.values()) or 1
    return {domain: count / total for domain, count in st.session_state.domain_exposure.items()}


def pick_domain_pair() -> tuple[str, str]:
    shares = domain_coverage_share()
    stretch = min(shares, key=shares.get)
    familiar = max(shares, key=shares.get)
    return familiar, stretch


def add_grammar_review_item(item_id: str, focus: str, explanation: str, example: str) -> None:
    if item_id not in st.session_state.grammar_review_queue:
        st.session_state.grammar_review_queue[item_id] = {
            "focus": focus,
            "explanation": explanation,
            "example": example,
            "streak": 0,
            "next_due": 0,
        }


def update_grammar_review_item(item_id: str, success: bool) -> None:
    item = st.session_state.grammar_review_queue[item_id]
    if success:
        item["streak"] += 1
    else:
        item["streak"] = 0
    item["next_due"] = st.session_state.grammar_review_step + (2 ** item["streak"])


def highlight_diff(original: str, corrected: str) -> str:
    diff = []
    for token in difflib.ndiff(original.split(), corrected.split()):
        if token.startswith("- "):
            diff.append(f"<span style='background-color:#fee2e2;'>{token[2:]}</span>")
        elif token.startswith("+ "):
            diff.append(f"<span style='background-color:#dcfce7;'>{token[2:]}</span>")
        elif token.startswith("  "):
            diff.append(token[2:])
    return " ".join(diff)


def sentence_split(text: str) -> list[str]:
    parts = []
    buffer = ""
    for char in text:
        buffer += char
        if char in ".!?":
            parts.append(buffer.strip())
            buffer = ""
    if buffer.strip():
        parts.append(buffer.strip())
    return parts


def extract_candidate_phrases(text: str) -> list[dict]:
    tokens = [token.strip(".,;:!?¡¿()").lower() for token in text.split()]
    tokens = [token for token in tokens if token]
    stopwords = {"de", "la", "el", "y", "en", "a", "que", "por", "para"}
    counts: dict[str, int] = {}
    for idx in range(len(tokens) - 1):
        phrase = f"{tokens[idx]} {tokens[idx + 1]}"
        if set(phrase.split()) & stopwords:
            continue
        counts[phrase] = counts.get(phrase, 0) + 1
    for idx in range(len(tokens) - 2):
        phrase = f"{tokens[idx]} {tokens[idx + 1]} {tokens[idx + 2]}"
        if set(phrase.split()) & stopwords:
            continue
        counts[phrase] = counts.get(phrase, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [{"phrase": phrase, "count": count} for phrase, count in ranked]


def detect_domains(text: str) -> list[str]:
    lowered = text.lower()
    hits = []
    for domain, keywords in CONTENT_INGEST_HINTS.items():
        if any(keyword in lowered for keyword in keywords):
            hits.append(domain)
    return hits or ["General"]


def update_review_item(item_id: str, success: bool) -> None:
    item = st.session_state.review_queue[item_id]
    if success:
        item["streak"] += 1
    else:
        item["streak"] = 0
    item["next_due"] = st.session_state.review_step + (2 ** item["streak"])


def render_growth_studio() -> None:
    st.header("Growth studio: vocabulary, verbs, grammar, output")
    st.write(
        "Push beyond repeated input with domain-specific vocabulary, precise verb choices, "
        "micro-grammar drills, and output-first practice with review."
    )

    st.subheader("1) Vocabulary expansion in context")
    domain = st.selectbox("Choose a new domain", [d["domain"] for d in VOCAB_DOMAINS])
    selected_domain = next(d for d in VOCAB_DOMAINS if d["domain"] == domain)
    st.markdown(selected_domain["context"])
    st.table(
        [
            {
                "Term": item["term"],
                "Meaning": item["meaning"],
                "Example": item["example"],
                "Register": item["register"],
            }
            for item in selected_domain["lexicon"]
        ]
    )
    chosen_terms = st.multiselect(
        "Add words to your review queue",
        [item["term"] for item in selected_domain["lexicon"]],
    )
    if st.button("Save vocab to review"):
        add_review_items(
            [
                {
                    **item,
                    "domain": selected_domain["domain"],
                    "pos": "verb" if item["term"].endswith("ar") else "noun",
                }
                for item in selected_domain["lexicon"]
                if item["term"] in chosen_terms
            ]
        )
        st.success("Added to review queue.")

    st.markdown("**Active production check**")
    vocab_response = st.text_area(
        "Write 2-3 sentences using at least 3 words from the table.",
        height=120,
        key="vocab-output",
    )
    if st.button("Check vocabulary usage"):
        used_terms = [item["term"] for item in selected_domain["lexicon"] if item["term"] in vocab_response]
        if len(used_terms) >= 3:
            st.success(f"Great—used: {', '.join(used_terms)}.")
            st.session_state.active_vocab.update(used_terms)
        else:
            st.warning(
                "Try to include at least 3 target words. Detected: "
                f"{', '.join(used_terms) or 'none'}."
            )

    st.subheader("2) Verb precision lab")
    verb_drill = st.selectbox(
        "Select a scenario", [item["scenario"] for item in VERB_PRECISION_DRILLS]
    )
    drill = next(item for item in VERB_PRECISION_DRILLS if item["scenario"] == verb_drill)
    verb_choice = st.radio(
        "Choose the best verb",
        [option["verb"] for option in drill["options"]],
        key="verb-choice",
    )
    if st.button("Check verb choice"):
        if verb_choice == drill["best"]:
            st.success("Correct choice for tone and precision.")
        else:
            st.error("Close, but there is a more precise option.")
            log_mistake("verb precision", drill["best"])
        st.caption(drill["contrast"])
        st.markdown("**Quick contrasts**")
        st.write(
            [
                {
                    "Verb": option["verb"],
                    "Nuance": option["nuance"],
                    "Example": option["example"],
                }
                for option in drill["options"]
            ]
        )

    st.subheader("3) Grammar reinforcement (micro-drills)")
    drill_results = []
    for idx, drill in enumerate(GRAMMAR_MICRODRILLS):
        st.markdown(f"**{drill['focus']}**")
        choice = st.radio(drill["prompt"], drill["options"], key=f"grammar-{idx}")
        drill_results.append((drill, choice))
    if st.button("Check grammar drills"):
        for drill, choice in drill_results:
            if choice == drill["answer"]:
                st.success(f"{drill['focus']}: Correct.")
            else:
                st.error(f"{drill['focus']}: Correct answer is {drill['answer']}.")
                log_mistake(drill["prompt"], drill["answer"], user_text=choice, corrected_text=drill["answer"])
                add_grammar_review_item(
                    drill["prompt"],
                    drill["focus"],
                    drill["explanation"],
                    drill["examples"][0],
                )
            st.caption(drill["explanation"])
            st.write("Examples: " + " • ".join(drill["examples"]))

    st.subheader("4) Output-first challenge")
    output_prompt = st.selectbox("Choose a prompt", [p["title"] for p in OUTPUT_PROMPTS])
    selected_prompt = next(p for p in OUTPUT_PROMPTS if p["title"] == output_prompt)
    st.markdown("**Prompt**: " + selected_prompt["prompt"])
    st.markdown("**Requirements**")
    for req in selected_prompt["requirements"]:
        st.markdown(f"- {req}")
    output_text = st.text_area("Your response", height=180, key="output-challenge")
    if st.button("Evaluate output"):
        feedback = []
        for mistake in COMMON_MISTAKES:
            if mistake["pattern"] in output_text.lower():
                feedback.append(mistake)
                log_mistake(mistake["pattern"], mistake["correction"])
        if feedback:
            st.error("Corrections needed")
            for item in feedback:
                st.markdown(f"- **Correction**: {item['correction']}")
                st.caption(item["explanation"])
                st.write("Examples: " + " • ".join(item["examples"]))
        else:
            st.success("Nice work! Your output avoids common errors.")

    st.subheader("5) Personalized review queue")
    st.session_state.review_step += 1
    due_items = [
        item for item in st.session_state.review_queue.values()
        if item["next_due"] <= st.session_state.review_step
    ]
    if not due_items:
        st.info("No items due. Add vocab above to start reviewing.")
    for item in due_items:
        st.markdown(f"**{item['term']}** — {item['meaning']}")
        st.caption(item["example"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Got it", key=f"review-pass-{item['term']}"):
                update_review_item(item["term"], True)
                st.success("Scheduled further out.")
        with col2:
            if st.button("Missed", key=f"review-fail-{item['term']}"):
                update_review_item(item["term"], False)
                st.warning("We'll recycle it sooner.")

    if st.session_state.mistake_log:
        st.markdown("**Mistake focus tracker**")
        sorted_mistakes = sorted(
            st.session_state.mistake_log.items(),
            key=lambda item: item[1]["count"],
            reverse=True,
        )
        st.table(
            [
                {
                    "Pattern": pattern,
                    "Correction": data["correction"],
                    "Count": data["count"],
                }
                for pattern, data in sorted_mistakes
            ]
        )


def render_topic_diversity_engine() -> None:
    st.header("Topic-Diversity Vocabulary Engine")
    st.write("Rotate across underexposed domains to escape the same-news-same-words loop.")

    familiar, stretch = pick_domain_pair()
    st.caption(f"Suggested mix: 70% familiar ({familiar}) • 30% stretch ({stretch})")

    domains = [d["domain"] for d in TOPIC_DIVERSITY_DOMAINS]
    if "topic_domain" not in st.session_state:
        st.session_state.topic_domain = stretch
    selected_domain = st.selectbox("Choose a domain", domains, key="topic_domain")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Surprise me"):
            st.session_state.topic_domain = stretch
            selected_domain = stretch
            st.success(f"Stretch domain selected: {stretch}")
    with col2:
        st.markdown("**Register options**")
        selected = next(d for d in TOPIC_DIVERSITY_DOMAINS if d["domain"] == selected_domain)
        st.write(", ".join(selected["register"]))

    st.markdown("**Domain prompt**")
    st.info(selected["sample"])
    st.markdown("**Session mix**")
    st.write(
        [
            {"Type": "Familiar (70%)", "Domain": familiar},
            {"Type": "Stretch (30%)", "Domain": stretch},
        ]
    )
    if st.button("Log exposure"):
        record_domain_exposure(selected_domain)
        st.success("Exposure logged.")

    st.markdown("**Save domain vocabulary**")
    domain_terms = {item["term"]: item for item in selected["lexicon"]}
    st.table(selected["lexicon"])
    selected_terms = st.multiselect("Select terms to learn", list(domain_terms.keys()))
    if st.button("Save selected terms"):
        add_review_items(
            [
                {
                    **domain_terms[term],
                    "domain": selected_domain,
                }
                for term in selected_terms
            ]
        )
        st.success("Saved with domain + register + part of speech tags.")

    st.markdown("**Domain coverage**")
    shares = domain_coverage_share()
    for domain, share in shares.items():
        st.progress(min(share, 1.0), text=f"{domain}: {share:.0%}")


def render_context_first_units() -> None:
    st.header("Context-First Vocabulary Units")
    st.write("Learn phrases through dialogue, messages, and mini-paragraphs.")

    unit_term = st.selectbox("Choose a unit", [unit["term"] for unit in VOCAB_CONTEXT_UNITS])
    unit = next(item for item in VOCAB_CONTEXT_UNITS if item["term"] == unit_term)
    tabs = st.tabs(["Context", "Practice", "Your sentence", "Review"])

    with tabs[0]:
        st.markdown("**Collocations**: " + ", ".join(unit["collocations"]))
        for context in unit["contexts"]:
            st.info(context)
        st.markdown(f"**Check:** {unit['question']}")

    with tabs[1]:
        st.markdown("**Step A: Comprehension check**")
        st.text_input(unit["question"], placeholder="Answer in one line")
        st.markdown("**Step B: Cloze with a twist**")
        choice = st.radio(unit["cloze"]["sentence"], unit["cloze"]["options"])
        if st.button("Check cloze"):
            if choice == unit["cloze"]["answer"]:
                st.success("Correct!")
            else:
                st.error("Try again.")
                st.caption(unit["cloze"]["explanation"])
        st.markdown("**Step D: Swap one word**")
        swap_choice = st.selectbox(
            unit["swap"]["base"], unit["swap"]["choices"], key=f"swap-{unit_term}"
        )
        st.caption(f"Rewrite by swapping one word: {swap_choice}")

    with tabs[2]:
        st.markdown("**Step C: Forced output**")
        response = st.text_area(unit["scenario"], height=120)
        if st.button("Log sentence"):
            if response.strip():
                st.session_state.active_vocab.update(unit["collocations"])
                st.success("Saved to active vocabulary.")
            else:
                st.info("Write a response to log it.")

    with tabs[3]:
        st.markdown("**Review prompts**")
        st.write(
            [
                "¿Qué contexto fue más natural para esta frase?",
                "¿Qué sinónimo usarías para variar el registro?",
                "¿Puedes reescribir la frase con un conector concesivo?",
            ]
        )


def render_verb_choice_studio() -> None:
    st.header("Verb Choice Studio")
    st.write("Pick the verb that best matches tone, intensity, and implication.")

    scenario = st.selectbox("Scenario", [item["scenario"] for item in VERB_CHOICE_STUDIO])
    drill = next(item for item in VERB_CHOICE_STUDIO if item["scenario"] == scenario)
    option_map = {option["verb"]: option for option in drill["options"]}
    choice = st.radio("Choose the best verb", list(option_map.keys()))
    explanation = st.text_input("Explain your choice in one line")

    if st.button("Reveal guidance"):
        if choice == drill["best"]:
            st.success("Best fit.")
        elif choice in drill["also"]:
            st.info("Also possible, but not the best fit.")
        else:
            st.error("Sounds odd in this context.")
        st.session_state.active_verbs.add(choice)
        if explanation.strip():
            st.caption(f"Your rationale: {explanation}")
        st.markdown("**Why**")
        for line in drill["contrast"]:
            st.write(f"- {line}")
        st.markdown("**Micro-notes**")
        st.write(
            [
                {
                    "Verb": option["verb"],
                    "Register": option["register"],
                    "Intensity": option["intensity"],
                    "Implication": option["implication"],
                    "Typical objects": option["objects"],
                }
                for option in drill["options"]
            ]
        )


def render_tiny_mistake_catcher() -> None:
    st.header("Real-time Tiny Mistake Catcher")
    st.write("Catch agreement, tense, and clitic slips with short, focused feedback.")
    draft = st.text_area("Type a sentence", height=120)
    st.toggle("Optional LLM second pass (not configured)", value=False, disabled=True)

    if st.button("Check sentence"):
        corrections = []
        for mistake in COMMON_MISTAKES:
            if mistake["pattern"] in draft.lower():
                corrections.append(mistake)
        if "ser" in draft.lower() and "listo" in draft.lower() and "está" not in draft.lower():
            corrections.append(
                {
                    "pattern": "ser listo",
                    "correction": "estar listo",
                    "explanation": "Estados temporales requieren estar.",
                    "examples": ["El plan está listo.", "La sala está lista."],
                }
            )
        if not corrections:
            st.success("No common issues detected.")
        else:
            for correction in corrections:
                fixed = draft.replace(correction["pattern"], correction["correction"])
                log_mistake(
                    correction["pattern"],
                    correction["correction"],
                    user_text=draft,
                    corrected_text=fixed,
                )
                st.markdown("**Diff**")
                st.markdown(highlight_diff(draft, fixed), unsafe_allow_html=True)
                st.markdown(f"**Correction:** {fixed}")
                st.caption(correction["explanation"])
                st.write("Examples: " + " • ".join(correction["examples"]))


def render_daily_missions() -> None:
    st.header("Output-First Daily Missions")
    st.write("Short daily tasks with constraints for speaking and writing.")

    today_seed = seed_for_week(date.today(), st.session_state.profile["name"])
    random.seed(today_seed)
    mission_vocab = random.sample(DAILY_MISSION_VERBS, k=2)
    grammar_target = random.choice(DAILY_MISSION_GRAMMAR)
    verb_target = random.choice(DAILY_MISSION_VERBS)

    st.markdown("**Today's constraints**")
    st.markdown(f"- Use 2 of these verbs/phrases: {', '.join(mission_vocab)}")
    st.markdown(f"- Include one grammar target: {grammar_target}")
    st.markdown(f"- Highlight verb nuance: {verb_target}")

    st.subheader("Speaking (60–90 seconds)")
    audio = st.file_uploader("Upload a recording", type=["wav", "mp3", "m4a"])
    if audio:
        st.session_state.speaking_minutes += 1
        st.success("Recording received. Add a short transcript below.")
    transcript = st.text_area("Transcript (optional)", height=100)

    st.subheader("Writing (2–4 sentences)")
    response = st.text_area("Write your response", height=140, key="daily-writing")
    if st.button("Submit mission"):
        if response.strip():
            feedback = []
            for mistake in COMMON_MISTAKES:
                if mistake["pattern"] in response.lower():
                    feedback.append(mistake)
                    log_mistake(mistake["pattern"], mistake["correction"], user_text=response)
            st.session_state.daily_mission_history.append(
                {
                    "date": date.today().isoformat(),
                    "response": response,
                    "constraints": [mission_vocab, grammar_target, verb_target],
                    "transcript": transcript,
                }
            )
            st.session_state.active_vocab.update(mission_vocab)
            st.session_state.active_verbs.add(verb_target)
            save_transcript(transcript)
            if feedback:
                st.warning("Corrections needed before retry.")
                for item in feedback:
                    st.markdown(f"- **Correction**: {item['correction']}")
                    st.caption(item["explanation"])
                st.info("Retry prompt: rewrite your response using the corrections.")
            else:
                st.success("Mission saved. Retry with corrections to reinforce.")
        else:
            st.info("Write a response before submitting.")


def render_error_notebook() -> None:
    st.header("Personalized Error Notebook")
    st.write("Track recurring errors and review by error type.")

    if not st.session_state.mistake_notebook:
        st.info("No errors logged yet. Practice to populate the notebook.")
        return

    st.markdown("**Your top errors**")
    st.dataframe(st.session_state.mistake_notebook, use_container_width=True)

    tag_counts = {}
    for entry in st.session_state.mistake_notebook:
        tag_counts[entry["tag"]] = tag_counts.get(entry["tag"], 0) + 1
    st.markdown("**Trend by error type**")
    trend_rows = [{"Tag": tag, "Count": count} for tag, count in tag_counts.items()]
    st.write(trend_rows)
    st.bar_chart({row["Tag"]: row["Count"] for row in trend_rows})

    tag = st.selectbox("Practice this error", sorted(tag_counts.keys()))
    st.session_state.error_review_step += 1
    queue = st.session_state.error_review_queue.get(tag, [])
    due_items = [
        (idx, item) for idx, item in enumerate(queue)
        if item["next_due"] <= st.session_state.error_review_step
    ]
    if due_items:
        idx, item = due_items[0]
        st.markdown(f"**Pattern:** {item['pattern']}")
        st.caption(f"Correction: {item['correction']}")
        if item.get("corrected_text"):
            st.info(f"Original → Corrected: {item['corrected_text']}")
            st.markdown("**Micro-drill**")
            st.write(
                "Reescribe la frase cambiando un solo detalle (tiempo verbal o sujeto) y mantén la corrección."
            )
        st.text_area("Rewrite a correct version", height=100, key=f"error-rewrite-{tag}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Got it", key=f"error-pass-{tag}-{idx}"):
                update_error_review_item(tag, idx, True)
                st.success("Scheduled further out.")
        with col2:
            if st.button("Missed", key=f"error-fail-{tag}-{idx}"):
                update_error_review_item(tag, idx, False)
                st.warning("Scheduled sooner.")
    else:
        st.info("No items due for this error tag yet.")


def render_review_hub() -> None:
    st.header("Two-Layer Spaced Review")
    st.write("Separate streams for vocabulary and grammar patterns.")

    st.subheader("Vocabulary review")
    st.session_state.review_step += 1
    due_vocab = [
        item for item in st.session_state.review_queue.values()
        if item["next_due"] <= st.session_state.review_step
    ]
    if not due_vocab:
        st.info("No vocab items due.")
    for item in due_vocab:
        stage = "meaning" if item["streak"] == 0 else "usage" if item["streak"] == 1 else "production"
        st.markdown(f"**{item['term']}** — {item['meaning']}")
        st.caption(f"{item['example']} • Stage: {stage}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Got it", key=f"hub-vocab-pass-{item['term']}"):
                update_review_item(item["term"], True)
                st.success("Scheduled later.")
        with col2:
            if st.button("Missed", key=f"hub-vocab-fail-{item['term']}"):
                update_review_item(item["term"], False)
                st.warning("Scheduled sooner.")

    st.subheader("Grammar review")
    st.session_state.grammar_review_step += 1
    due_grammar = [
        item for item in st.session_state.grammar_review_queue.values()
        if item["next_due"] <= st.session_state.grammar_review_step
    ]
    if not due_grammar:
        st.info("No grammar items due.")
    for item_id, item in st.session_state.grammar_review_queue.items():
        if item["next_due"] > st.session_state.grammar_review_step:
            continue
        stage = "recognition" if item["streak"] == 0 else "constrained" if item["streak"] == 1 else "free"
        st.markdown(f"**{item['focus']}**")
        st.caption(f"{item['explanation']} • Stage: {stage}")
        st.write(f"Example: {item['example']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Got it", key=f"hub-grammar-pass-{item_id}"):
                update_grammar_review_item(item_id, True)
                st.success("Scheduled later.")
        with col2:
            if st.button("Missed", key=f"hub-grammar-fail-{item_id}"):
                update_grammar_review_item(item_id, False)
                st.warning("Scheduled sooner.")

    st.subheader("Interleaving mix")
    if due_vocab and due_grammar:
        mixed_prompt = random.choice(
            [
                f"Vocab: define '{due_vocab[0]['term']}' and use it in a sentence.",
                f"Grammar: apply '{due_grammar[0]['focus']}' in a new sentence.",
            ]
        )
        st.info(mixed_prompt)
        st.text_area("Mixed response", height=120, key="interleaving-response")
    else:
        st.caption("Interleaving unlocks once both queues have due items.")

def render_content_ingest() -> None:
    st.header("Bring Your Own Content")
    st.write("Paste content to extract phrases and build practice.")

    raw = st.text_area("Paste article or transcript", height=180)
    if st.button("Extract"):
        sentences = sentence_split(raw)
        candidates = extract_candidate_phrases(raw)
        known = {item["term"] for item in st.session_state.review_queue.values()}
        filtered = [item for item in candidates if item["phrase"] not in known and item["count"] >= 1][:20]
        domains = detect_domains(raw)
        st.markdown(f"**Detected domains:** {', '.join(domains)}")
        st.markdown("**Candidates**")
        selections = []
        for item in filtered:
            phrase = item["phrase"]
            status = st.selectbox(
                f"{phrase} (freq {item['count']})",
                ["Learn", "Skip", "Already know"],
                key=f"phrase-status-{phrase}",
            )
            if status == "Learn":
                selections.append(phrase)
        if selections:
            for phrase in selections:
                add_review_items(
                    [
                        {
                            "term": phrase,
                            "meaning": "to define",
                            "example": f"Contexto: {phrase} ...",
                            "domain": domains[0] if domains else "General",
                            "register": "neutral",
                            "pos": "phrase",
                        }
                    ]
                )
            st.success("Added selected phrases to review queue.")
        st.markdown("**Auto-contexts**")
        for sentence in sentences[:3]:
            st.info(sentence)


def render_conversation_goals() -> None:
    st.header("Conversation Mode with Goals")
    st.write("Goal-driven roleplays with hidden targets and corrective replay.")

    scenario = st.selectbox("Choose a mission", [s["title"] for s in CONVERSATION_GOAL_SCENARIOS])
    selected = next(s for s in CONVERSATION_GOAL_SCENARIOS if s["title"] == scenario)
    st.markdown(f"**Brief:** {selected['brief']}")
    response = st.text_area("Your response", height=180, key="goal-convo")

    if st.button("Finish conversation"):
        lowered = response.lower()
        st.markdown("**Inline corrections**")
        for mistake in COMMON_MISTAKES:
            if mistake["pattern"] in lowered:
                st.warning(f"Correction: {mistake['correction']} — {mistake['explanation']}")
                log_mistake(mistake["pattern"], mistake["correction"], user_text=response)
        st.markdown("**Hidden targets**")
        results = []
        for target in selected["hidden_targets"]:
            if "mitigadores" in target:
                passed = any(token in lowered for token in ["quizá", "tal vez", "me parece"])
            elif "concesión" in target:
                passed = any(token in lowered for token in ["aunque", "si bien", "a pesar de"])
            elif "verbo preciso" in target:
                passed = any(token in lowered for token in ["afrontar", "plantear", "desactivar"])
            elif "petición indirecta" in target:
                passed = "sería posible" in lowered or "podría" in lowered
            elif "calco" in target:
                passed = "aplicar para" not in lowered
            else:
                passed = False
            results.append((target, passed))
        for target, passed in results:
            st.write(f"{'✅' if passed else '❌'} {target}")
        st.info("Replay task: rewrite your response applying the missed targets.")
        st.markdown("**What you did well**")
        st.write(
            "- Maintained focus on the task goal.\n"
            "- Included at least one register marker."
        )
        st.markdown("**One thing to repeat tomorrow**")
        st.write("Reuse the missed targets in a new, shorter response.")


def render_settings() -> None:
    st.header("Settings & data portability")
    st.write("Export vocab, mistakes, and transcripts for portability.")

    vocab_export = json.dumps(list(st.session_state.review_queue.values()), indent=2)
    mistakes_export = json.dumps(st.session_state.mistake_notebook, indent=2)
    transcripts_export = json.dumps(
        [entry.get("transcript", "") for entry in st.session_state.daily_mission_history],
        indent=2,
    )

    st.download_button("Download vocab JSON", data=vocab_export, file_name="vocab.json")
    st.download_button("Download mistakes JSON", data=mistakes_export, file_name="mistakes.json")
    st.download_button("Download transcripts JSON", data=transcripts_export, file_name="transcripts.json")

    vocab_csv = StringIO()
    vocab_writer = DictWriter(
        vocab_csv, fieldnames=["term", "meaning", "example", "domain", "register", "pos"]
    )
    vocab_writer.writeheader()
    for item in st.session_state.review_queue.values():
        vocab_writer.writerow(item)

    mistakes_csv = StringIO()
    mistake_writer = DictWriter(
        mistakes_csv,
        fieldnames=[
            "date",
            "pattern",
            "correction",
            "tag",
            "confidence",
            "user_text",
            "corrected_text",
        ],
    )
    mistake_writer.writeheader()
    for item in st.session_state.mistake_notebook:
        mistake_writer.writerow(item)

    transcripts_csv = StringIO()
    transcript_writer = DictWriter(transcripts_csv, fieldnames=["date", "transcript"])
    transcript_writer.writeheader()
    for entry in st.session_state.daily_mission_history:
        transcript_writer.writerow(
            {"date": entry["date"], "transcript": entry.get("transcript", "")}
        )

    st.download_button("Download vocab CSV", data=vocab_csv.getvalue(), file_name="vocab.csv")
    st.download_button(
        "Download mistakes CSV", data=mistakes_csv.getvalue(), file_name="mistakes.csv"
    )
    st.download_button(
        "Download transcripts CSV",
        data=transcripts_csv.getvalue(),
        file_name="transcripts.csv",
    )


def main() -> None:
    set_theme()
    init_db()
    init_state()
    render_profile_sidebar()

    render_hero()
    st.write("")

    nav = st.sidebar.radio(
        "Go to",
        [
            "Overview",
            "Topic Diversity",
            "Context Units",
            "Growth Studio",
            "Verb Choice Studio",
            "Tiny Mistake Catcher",
            "Daily Missions",
            "Review Hub",
            "Error Notebook",
            "Weekly Mission",
            "Adaptive Inputs",
            "Content Ingest",
            "Nuance Feedback",
            "Relationship Memory",
            "Live Mode",
            "Gap Finder",
            "Register Simulator",
            "Prosody Coach",
            "Collocation Engine",
            "Conversation Goals",
            "Conversation Lab",
            "Writing Studio",
            "Argumentation",
            "Dialect Tuning",
            "Listening for Nuance",
            "Portfolio",
            "Settings",
        ],
    )

    if nav == "Overview":
        render_overview()
    elif nav == "Topic Diversity":
        render_topic_diversity_engine()
    elif nav == "Context Units":
        render_context_first_units()
    elif nav == "Growth Studio":
        render_growth_studio()
    elif nav == "Verb Choice Studio":
        render_verb_choice_studio()
    elif nav == "Tiny Mistake Catcher":
        render_tiny_mistake_catcher()
    elif nav == "Daily Missions":
        render_daily_missions()
    elif nav == "Review Hub":
        render_review_hub()
    elif nav == "Error Notebook":
        render_error_notebook()
    elif nav == "Weekly Mission":
        render_mission_control()
    elif nav == "Adaptive Inputs":
        render_adaptive_input_selection()
    elif nav == "Content Ingest":
        render_content_ingest()
    elif nav == "Nuance Feedback":
        render_nuance_feedback()
    elif nav == "Relationship Memory":
        render_relationship_memory()
    elif nav == "Live Mode":
        render_live_mode()
    elif nav == "Gap Finder":
        render_gap_finder()
    elif nav == "Register Simulator":
        render_register_simulator()
    elif nav == "Prosody Coach":
        render_pronunciation_coach()
    elif nav == "Collocation Engine":
        render_collocation_engine()
    elif nav == "Conversation Goals":
        render_conversation_goals()
    elif nav == "Conversation Lab":
        render_conversation_lab()
    elif nav == "Writing Studio":
        render_writing_studio()
    elif nav == "Argumentation":
        render_argumentation_drills()
    elif nav == "Dialect Tuning":
        render_dialect_tuning()
    elif nav == "Listening for Nuance":
        render_listening_nuance()
    elif nav == "Portfolio":
        render_portfolio()
    elif nav == "Settings":
        render_settings()


if __name__ == "__main__":
    main()
