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
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,"
        "application/rss+xml;q=0.9,"
        "application/atom+xml;q=0.9,"
        "*/*;q=0.8"
    ),
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
}


# ==========================================================
# FUENTES OFICIALES
# ==========================================================

FUENTES = [
    {
        "nombre": "OECE",
        "url": "https://www.gob.pe/institucion/oece/noticias",
        "rss": None,
        "categoria": "Contratación pública",
    },
    {
        "nombre": "Contraloría General de la República",
        "url": "https://www.gob.pe/institucion/contraloria/noticias",
        "rss": None,
        "categoria": "Control y fiscalización",
    },
    {
        "nombre": "Ministerio de Economía y Finanzas",
        "url": "https://www.gob.pe/institucion/mef/noticias",
        "rss": None,
        "categoria": "Economía e inversión pública",
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
        "rss": None,
        "categoria": "Construcción e infraestructura",
    },
    {
        "nombre": "SENCICO",
        "url": (
            "https://www.gob.pe/institucion/"
            "sencico/noticias"
        ),
        "rss": None,
        "categoria": "Construcción y capacitación",
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
    """
    Limpia HTML y espacios innecesarios.
    """
    if not texto:
        return ""

    texto = BeautifulSoup(
        str(texto),
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
    """
    Normaliza texto para búsquedas y comparación.
    """
    return limpiar_texto(
        texto
    ).lower()


def es_relevante(titulo, resumen):
    """
    Determina si una noticia está relacionada
    con el ámbito de obras, construcción,
    contratación pública o liquidaciones.

    Se acepta una coincidencia de al menos
    una palabra clave.
    """
    texto = normalizar(
        f"{titulo} {resumen}"
    )

    for palabra in PALABRAS_CLAVE:

        if normalizar(
            palabra
        ) in texto:

            return True

    return False


def obtener_html(url):
    """
    Descarga una URL y devuelve el contenido.
    """
    try:

        print(
            f"  Consultando URL: {url}"
        )

        respuesta = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        respuesta.raise_for_status()

        print(
            f"  HTTP {respuesta.status_code}"
        )

        return respuesta.text

    except requests.RequestException as error:

        print(
            f"  [ERROR HTTP] {error}"
        )

    except Exception as error:

        print(
            f"  [ERROR] {error}"
        )

    return None


def limpiar_url(url):
    """
    Limpia una URL y elimina fragmentos.
    """
    if not url:
        return ""

    return url.split(
        "#",
        1
    )[0].strip()


def es_url_valida(url):
    """
    Comprueba que la URL sea HTTP/HTTPS.
    """
    if not url:
        return False

    return url.startswith(
        "http://"
    ) or url.startswith(
        "https://"
    )


def extraer_fecha(texto):
    """
    Busca fechas habituales en textos
    publicados en español.
    """
    texto = limpiar_texto(
        texto
    )

    patrones = [

        r"\b\d{1,2}/\d{1,2}/\d{4}\b",

        r"\b\d{1,2}-\d{1,2}-\d{4}\b",

        r"\b\d{4}-\d{1,2}-\d{1,2}\b",

        r"\b\d{1,2}\s+de\s+"
        r"(enero|febrero|marzo|abril|mayo|junio|"
        r"julio|agosto|septiembre|octubre|"
        r"noviembre|diciembre)"
        r"\s+de\s+\d{4}\b",

        r"\b\d{1,2}\s+"
        r"(enero|febrero|marzo|abril|mayo|junio|"
        r"julio|agosto|septiembre|octubre|"
        r"noviembre|diciembre)"
        r"\s+\d{4}\b",
    ]

    for patron in patrones:

        coincidencia = re.search(
            patron,
            texto,
            flags=re.IGNORECASE
        )

        if coincidencia:

            return coincidencia.group(
                0
            )

    return ""


def crear_resumen(texto, titulo):
    """
    Genera un resumen limpio y limitado.
    """
    texto = limpiar_texto(
        texto
    )

    titulo = limpiar_texto(
        titulo
    )

    if titulo and titulo in texto:

        texto = texto.replace(
            titulo,
            "",
            1
        ).strip()

    if len(texto) > 500:

        texto = (
            texto[:497]
            + "..."
        )

    return texto


def crear_noticia(
    titulo,
    resumen,
    url,
    fuente,
    categoria,
    fecha=""
):
    """
    Construye un registro uniforme para noticias.json.
    """
    titulo = limpiar_texto(
        titulo
    )

    resumen = crear_resumen(
        resumen,
        titulo
    )

    url = limpiar_url(
        url
    )

    if not titulo:
        return None

    if not es_url_valida(
        url
    ):
        return None

    return {

        "titulo": titulo,

        "resumen": resumen,

        "url": url,

        "fuente": fuente,

        "categoria": categoria,

        "fecha": (
            limpiar_texto(
                fecha
            )
            if fecha
            else ""
        ),

        "fecha_actualizacion": (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

    }


# ==========================================================
# EXTRACCIÓN RSS / ATOM
# ==========================================================

def extraer_noticias_rss(
    fuente
):
    """
    Intenta obtener noticias desde un RSS o Atom.
    """
    rss_url = fuente.get(
        "rss"
    )

    if not rss_url:

        return []

    print(
        f"  Intentando RSS/Atom: "
        f"{rss_url}"
    )

    xml = obtener_html(
        rss_url
    )

    if not xml:

        return []

    soup = BeautifulSoup(
        xml,
        "xml"
    )

    resultados = []

    elementos = soup.find_all(
        [
            "item",
            "entry"
        ]
    )

    for elemento in elementos:

        titulo_tag = elemento.find(
            "title"
        )

        titulo = (
            titulo_tag.get_text(
                " ",
                strip=True
            )
            if titulo_tag
            else ""
        )

        enlace = ""

        link_tag = elemento.find(
            "link"
        )

        if link_tag:

            if link_tag.get(
                "href"
            ):

                enlace = link_tag.get(
                    "href"
                )

            else:

                enlace = link_tag.get_text(
                    " ",
                    strip=True
                )

        descripcion_tag = (
            elemento.find(
                "description"
            )
            or elemento.find(
                "summary"
            )
            or elemento.find(
                "content"
            )
        )

        resumen = (
            descripcion_tag.get_text(
                " ",
                strip=True
            )
            if descripcion_tag
            else ""
        )

        fecha_tag = (
            elemento.find(
                "pubDate"
            )
            or elemento.find(
                "published"
            )
            or elemento.find(
                "updated"
            )
        )

        fecha = (
            fecha_tag.get_text(
                " ",
                strip=True
            )
            if fecha_tag
            else ""
        )

        if not es_relevante(
            titulo,
            resumen
        ):
            continue

        noticia = crear_noticia(
            titulo=titulo,
            resumen=resumen,
            url=enlace,
            fuente=fuente[
                "nombre"
            ],
            categoria=fuente.get(
                "categoria",
                "General"
            ),
            fecha=fecha
        )

        if noticia:

            resultados.append(
                noticia
            )

        if len(
            resultados
        ) >= NOTICIAS_POR_FUENTE:

            break

    return resultados


# ==========================================================
# EXTRACCIÓN HTML DE GOB.PE
# ==========================================================

def es_enlace_de_publicacion(
    url
):
    """
    Comprueba si una URL parece corresponder
    a una publicación individual.

    Se evita depender exclusivamente de
    '/noticias/'.
    """
    if not url:
        return False

    url = url.lower()

    patrones = [

        "/noticias/",

        "/noticia/",

        "/comunicado/",

        "/campana/",

        "/informe/",

        "/publicacion/",

        "/post/",

    ]

    return any(
        patron in url
        for patron in patrones
    )


def obtener_contenedor_contexto(
    enlace
):
    """
    Sube varios niveles del HTML para obtener
    título, fecha y resumen.
    """
    contenedor = enlace

    for _ in range(6):

        if not contenedor.parent:

            break

        contenedor = (
            contenedor.parent
        )

    return contenedor


def extraer_noticias_gobpe(
    fuente
):
    """
    Extrae publicaciones de una página institucional
    de Gob.pe utilizando múltiples estrategias.
    """

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

    enlaces = soup.find_all(
        "a",
        href=True
    )

    print(
        f"  Enlaces encontrados en HTML: "
        f"{len(enlaces)}"
    )

    for enlace in enlaces:

        href = enlace.get(
            "href",
            ""
        )

        href = limpiar_url(
            href
        )

        if not href:

            continue

        url = urljoin(
            fuente["url"],
            href
        )

        url = limpiar_url(
            url
        )

        if not es_url_valida(
            url
        ):

            continue

        if not es_enlace_de_publicacion(
            url
        ):

            continue

        if url in vistos:

            continue

        vistos.add(
            url
        )

        titulo = limpiar_texto(
            enlace.get_text(
                " ",
                strip=True
            )
        )

        if len(
            titulo
        ) < 15:

            continue

        contenedor = (
            obtener_contenedor_contexto(
                enlace
            )
        )

        texto_contexto = limpiar_texto(
            contenedor.get_text(
                " ",
                strip=True
            )
        )

        # ----------------------------------------------
        # Buscar título alternativo
        # ----------------------------------------------

        if not titulo:

            encabezado = (
                contenedor.find(
                    [
                        "h1",
                        "h2",
                        "h3",
                        "h4"
                    ]
                )
            )

            if encabezado:

                titulo = limpiar_texto(
                    encabezado.get_text(
                        " ",
                        strip=True
                    )
                )

        if not titulo:

            continue

        # ----------------------------------------------
        # Filtrado de relevancia
        # ----------------------------------------------

        if not es_relevante(
            titulo,
            texto_contexto
        ):

            continue

        # ----------------------------------------------
        # Extraer fecha
        # ----------------------------------------------

        fecha = extraer_fecha(
            texto_contexto
        )

        # ----------------------------------------------
        # Crear noticia
        # ----------------------------------------------

        noticia = crear_noticia(
            titulo=titulo,
            resumen=texto_contexto,
            url=url,
            fuente=fuente[
                "nombre"
            ],
            categoria=fuente.get(
                "categoria",
                "General"
            ),
            fecha=fecha
        )

        if not noticia:

            continue

        resultados.append(
            noticia
        )

        print(
            f"  [+] {titulo[:100]}"
        )

        if len(
            resultados
        ) >= NOTICIAS_POR_FUENTE:

            break

    return resultados


# ==========================================================
# MÉTODO ALTERNATIVO: TARJETAS / ARTÍCULOS
# ==========================================================

def extraer_noticias_por_bloques(
    fuente
):
    """
    Método alternativo para páginas donde los enlaces
    no tienen una estructura convencional.
    """
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

    bloques = soup.find_all(
        [
            "article",
            "li"
        ]
    )

    for bloque in bloques:

        enlace = bloque.find(
            "a",
            href=True
        )

        if not enlace:

            continue

        titulo_tag = bloque.find(
            [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5"
            ]
        )

        titulo = ""

        if titulo_tag:

            titulo = limpiar_texto(
                titulo_tag.get_text(
                    " ",
                    strip=True
                )
            )

        if not titulo:

            titulo = limpiar_texto(
                enlace.get_text(
                    " ",
                    strip=True
                )
            )

        if len(
            titulo
        ) < 15:

            continue

        url = urljoin(
            fuente["url"],
            enlace.get(
                "href"
            )
        )

        texto = limpiar_texto(
            bloque.get_text(
                " ",
                strip=True
            )
        )

        if not es_relevante(
            titulo,
            texto
        ):

            continue

        noticia = crear_noticia(
            titulo=titulo,
            resumen=texto,
            url=url,
            fuente=fuente[
                "nombre"
            ],
            categoria=fuente.get(
                "categoria",
                "General"
            ),
            fecha=extraer_fecha(
                texto
            )
        )

        if noticia:

            resultados.append(
                noticia
            )

        if len(
            resultados
        ) >= NOTICIAS_POR_FUENTE:

            break

    return resultados


# ==========================================================
# EXTRACCIÓN COMPLETA DE UNA FUENTE
# ==========================================================

def extraer_noticias_fuente(
    fuente
):
    """
    Ejecuta las estrategias disponibles
    hasta encontrar noticias.
    """

    print(
        "\n--------------------------------------"
    )

    print(
        f"FUENTE: {fuente['nombre']}"
    )

    print(
        "--------------------------------------"
    )

    resultados = []

    # ------------------------------------------------------
    # 1. RSS / Atom
    # ------------------------------------------------------

    if fuente.get(
        "rss"
    ):

        resultados = (
            extraer_noticias_rss(
                fuente
            )
        )

        if resultados:

            print(
                f"  RSS/Atom: "
                f"{len(resultados)} noticias"
            )

            return resultados

    # ------------------------------------------------------
    # 2. HTML por enlaces
    # ------------------------------------------------------

    resultados = (
        extraer_noticias_gobpe(
            fuente
        )
    )

    if resultados:

        print(
            f"  HTML: "
            f"{len(resultados)} noticias"
        )

        return resultados

    # ------------------------------------------------------
    # 3. HTML por bloques
    # ------------------------------------------------------

    print(
        "  No se encontraron noticias "
        "con el método principal."
    )

    print(
        "  Intentando método alternativo..."
    )

    resultados = (
        extraer_noticias_por_bloques(
            fuente
        )
    )

    print(
        f"  Método alternativo: "
        f"{len(resultados)} noticias"
    )

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

            noticias = datos.get(
                "noticias",
                []
            )

            if isinstance(
                noticias,
                list
            ):

                return noticias

        if isinstance(
            datos,
            list
        ):

            return datos

    except Exception as error:

        print(
            "[ADVERTENCIA] "
            "No se pudo leer noticias.json:"
        )

        print(
            error
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

        if not isinstance(
            noticia,
            dict
        ):

            continue

        url = limpiar_url(
            noticia.get(
                "url",
                ""
            )
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

        if not clave:

            continue

        if clave not in unicas:

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

    # ------------------------------------------------------
    # Ordenar por fecha de actualización del registro.
    # Las noticias nuevas quedan primero.
    # ------------------------------------------------------

    noticias.sort(
        key=lambda noticia:
            noticia.get(
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

    print(
        f"\nJSON guardado correctamente: "
        f"{ARCHIVO_SALIDA}"
    )

    print(
        f"Noticias guardadas: "
        f"{len(noticias)}"
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

    print(
        f"Fecha UTC: "
        f"{datetime.now(timezone.utc).isoformat()}"
    )

    print(
        f"Fuentes configuradas: "
        f"{len(FUENTES)}"
    )

    noticias_nuevas = []

    # ------------------------------------------------------
    # CONSULTAR TODAS LAS FUENTES
    # ------------------------------------------------------

    for fuente in FUENTES:

        try:

            noticias = (
                extraer_noticias_fuente(
                    fuente
                )
            )

            print(
                f"Resultado final de "
                f"{fuente['nombre']}: "
                f"{len(noticias)}"
            )

            noticias_nuevas.extend(
                noticias
            )

        except Exception as error:

            print(
                f"[ERROR] Falló la fuente "
                f"{fuente['nombre']}: "
                f"{error}"
            )

    # ------------------------------------------------------
    # CARGAR NOTICIAS ANTERIORES
    # ------------------------------------------------------

    noticias_anteriores = (
        cargar_noticias_existentes()
    )

    print(
        "\nNoticias nuevas: "
        f"{len(noticias_nuevas)}"
    )

    print(
        "Noticias anteriores: "
        f"{len(noticias_anteriores)}"
    )

    # ------------------------------------------------------
    # COMBINAR
    # ------------------------------------------------------

    todas = (
        noticias_nuevas
        + noticias_anteriores
    )

    todas = eliminar_duplicados(
        todas
    )

    # ------------------------------------------------------
    # PROTECCIÓN CONTRA JSON VACÍO
    # ------------------------------------------------------
    #
    # Si todas las fuentes fallan y ya existen noticias,
    # conservamos las noticias anteriores.
    #
    # Si nunca hubo noticias, se genera el JSON vacío
    # correctamente, pero el log deja constancia.
    # ------------------------------------------------------

    if (
        not noticias_nuevas
        and noticias_anteriores
    ):

        print(
            "\n[ADVERTENCIA]"
        )

        print(
            "No se obtuvieron noticias nuevas."
        )

        print(
            "Se conservarán las noticias anteriores."
        )

    # ------------------------------------------------------
    # GUARDAR
    # ------------------------------------------------------

    guardar_noticias(
        todas
    )

    print(
        "\n======================================"
    )

    print(
        "PROCESO FINALIZADO"
    )

    print(
        f"TOTAL DE NOTICIAS DISPONIBLES: "
        f"{len(todas)}"
    )

    print(
        "Archivo actualizado: noticias.json"
    )

    print(
        "======================================"
    )


# ==========================================================
# EJECUCIÓN
# ==========================================================

if __name__ == "__main__":

    main()
