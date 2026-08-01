import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_SALIDA = BASE_DIR / "noticias.json"

MAX_NOTICIAS = 30
NOTICIAS_POR_FUENTE = 10
TIMEOUT = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


# ==========================================================
# FUENTES OFICIALES VERIFICADAS
# ==========================================================

FUENTES = [
    {
        "nombre": "OECE",
        "url": "https://www.gob.pe/institucion/oece/noticias",
    },
    {
        "nombre": "Contraloría General de la República",
        "url": "https://www.gob.pe/institucion/contraloria/noticias",
    },
    {
        "nombre": "Ministerio de Economía y Finanzas",
        "url": "https://www.gob.pe/institucion/mef/noticias",
    },
    {
        "nombre": (
            "Ministerio de Vivienda, "
            "Construcción y Saneamiento"
        ),
        "url": (
            "https://www.gob.pe/institucion/"
            "vivienda/noticias"
        ),
    },
    {
        "nombre": "SENCICO",
        "url": (
            "https://www.gob.pe/institucion/"
            "sencico/noticias"
        ),
    },
]


# ==========================================================
# PALABRAS CLAVE
# ==========================================================

PALABRAS_CLAVE = [
    "obra",
    "obras",
    "obra pública",
    "obras públicas",
    "construcción",
    "edificación",
    "infraestructura",
    "contratación pública",
    "contrataciones públicas",
    "contrato de obra",
    "liquidación",
    "liquidación de obra",
    "liquidaciones",
    "expediente técnico",
    "supervisión",
    "supervisor de obra",
    "residente de obra",
    "peritaje",
    "peritajes",
    "tasación",
    "tasaciones",
    "valorización",
    "valorizaciones",
    "presupuesto",
    "inversión pública",
    "inversiones",
    "seace",
    "oece",
    "osce",
    "contraloría",
    "control concurrente",
    "arbitraje",
    "controversia",
    "adicional de obra",
    "ampliación de plazo",
    "penalidad",
    "reconocimiento de deuda",
    "saldo de obra",
    "cierre de obra",
    "recepción de obra",
    "reglamento nacional de edificaciones",
    "rne",
    "saneamiento",
]


# ==========================================================
# UTILIDADES
# ==========================================================

def limpiar_texto(texto):
    if not texto:
        return ""

    texto = BeautifulSoup(
        texto,
        "html.parser"
    ).get_text(
        " ",
        strip=True
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def normalizar(texto):
    return limpiar_texto(
        texto
    ).lower()


def es_relevante(titulo, resumen):
    texto = normalizar(
        f"{titulo} {resumen}"
    )

    coincidencias = 0

    for palabra in PALABRAS_CLAVE:

        if palabra.lower() in texto:
            coincidencias += 1

    return coincidencias >= 1


def obtener_fecha(texto):
    texto = limpiar_texto(
        texto
    )

    return texto


def obtener_html(url):

    try:

        respuesta = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        respuesta.raise_for_status()

        return respuesta.text

    except Exception as error:

        print(
            f"[ERROR] No se pudo consultar "
            f"{url}: {error}"
        )

        return None


# ==========================================================
# EXTRACCIÓN DE NOTICIAS DE GOB.PE
# ==========================================================

def extraer_noticias_gobpe(
    fuente
):

    html = obtener_html(
        fuente["url"]
    )

    if not html:
        return []

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    resultados = []

    vistos = set()

    # ------------------------------------------------------
    # Buscamos enlaces que apunten a publicaciones
    # ------------------------------------------------------

    enlaces = soup.find_all(
        "a",
        href=True
    )

    for enlace in enlaces:

        titulo = limpiar_texto(
            enlace.get_text(
                " ",
                strip=True
            )
        )

        href = enlace.get(
            "href"
        )

        if not titulo:
            continue

        if not href:
            continue

        url = urljoin(
            fuente["url"],
            href
        )

        # Evitar enlaces generales
        if "/noticias/" not in url:
            continue

        # Evitar títulos demasiado cortos
        if len(titulo) < 20:
            continue

        # Evitar duplicados
        if url in vistos:
            continue

        vistos.add(
            url
        )

        # --------------------------------------------------
        # Buscar contenedor padre para obtener contexto
        # --------------------------------------------------

        contenedor = enlace

        for _ in range(5):

            if contenedor.parent:

                contenedor = (
                    contenedor.parent
                )

        texto_contexto = limpiar_texto(
            contenedor.get_text(
                " ",
                strip=True
            )
        )

        # --------------------------------------------------
        # Filtrado por relevancia
        # --------------------------------------------------

        if not es_relevante(
            titulo,
            texto_contexto
        ):
            continue

        # --------------------------------------------------
        # Limpiar resumen
        # --------------------------------------------------

        resumen = texto_contexto

        resumen = resumen.replace(
            titulo,
            ""
        ).strip()

        if len(resumen) > 500:

            resumen = (
                resumen[:497]
                + "..."
            )

        resultados.append({

            "titulo": titulo,

            "resumen": resumen,

            "url": url,

            "fuente": fuente[
                "nombre"
            ],

            "fecha": obtener_fecha(
                texto_contexto
            ),

            "fecha_actualizacion": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            )

        })

        if len(
            resultados
        ) >= NOTICIAS_POR_FUENTE:

            break

    return resultados


# ==========================================================
# CARGAR NOTICIAS EXISTENTES
# ==========================================================

def cargar_noticias_existentes():

    if not ARCHIVO_SALIDA.exists():

        return []

    try:

        with open(
            ARCHIVO_SALIDA,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(
                archivo
            )

        if isinstance(
            datos,
            dict
        ):

            return datos.get(
                "noticias",
                []
            )

        if isinstance(
            datos,
            list
        ):

            return datos

    except Exception as error:

        print(
            f"[ADVERTENCIA] "
            f"No se pudo leer "
            f"noticias.json: "
            f"{error}"
        )

    return []


# ==========================================================
# ELIMINAR DUPLICADOS
# ==========================================================

def eliminar_duplicados(
    noticias
):

    unicas = {}

    for noticia in noticias:

        url = noticia.get(
            "url"
        )

        titulo = normalizar(
            noticia.get(
                "titulo",
                ""
            )
        )

        clave = (
            url
            or titulo
        )

        if clave:

            unicas[
                clave
            ] = noticia

    return list(
        unicas.values()
    )


# ==========================================================
# GUARDAR JSON
# ==========================================================

def guardar_noticias(
    noticias
):

    noticias = eliminar_duplicados(
        noticias
    )

    # Ordenar por fecha de actualización
    noticias.sort(
        key=lambda x:
            x.get(
                "fecha_actualizacion",
                ""
            ),
        reverse=True
    )

    noticias = noticias[
        :MAX_NOTICIAS
    ]

    datos = {

        "actualizado": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),

        "total": len(
            noticias
        ),

        "fuentes": [
            fuente[
                "nombre"
            ]
            for fuente in FUENTES
        ],

        "noticias": noticias

    }

    with open(
        ARCHIVO_SALIDA,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=2
        )


# ==========================================================
# PROCESO PRINCIPAL
# ==========================================================

def main():

    print(
        "======================================"
    )

    print(
        "ACTUALIZACIÓN AUTOMÁTICA DE NOTICIAS"
    )

    print(
        "======================================"
    )

    noticias_nuevas = []

    for fuente in FUENTES:

        print(
            f"\nConsultando: "
            f"{fuente['nombre']}"
        )

        noticias = (
            extraer_noticias_gobpe(
                fuente
            )
        )

        print(
            f"Noticias encontradas: "
            f"{len(noticias)}"
        )

        noticias_nuevas.extend(
            noticias
        )

    noticias_anteriores = (
        cargar_noticias_existentes()
    )

    # Mantener noticias anteriores
    # como respaldo si una fuente falla
    todas = (
        noticias_nuevas
        + noticias_anteriores
    )

    todas = eliminar_duplicados(
        todas
    )

    guardar_noticias(
        todas
    )

    print(
        "\n======================================"
    )

    print(
        f"TOTAL DE NOTICIAS: "
        f"{len(todas)}"
    )

    print(
        "Archivo actualizado: "
        "noticias.json"
    )

    print(
        "======================================"
    )


if __name__ == "__main__":

    main()
