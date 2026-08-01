import json
import re
from datetime import datetime, timezone

import feedparser


# =====================================================
# CONFIGURACIÓN
# =====================================================

FUENTES = [

    {
        "nombre": "OECE",
        "url": "https://www.gob.pe/institucion/oece/noticias"
    },

    {
        "nombre": "MEF",
        "url": "https://www.gob.pe/institucion/mef/noticias"
    }

]


# =====================================================
# PALABRAS CLAVE
# =====================================================

PALABRAS_CLAVE = [

    "obra",
    "obras",
    "liquidación",
    "liquidaciones",
    "contratación pública",
    "contrataciones públicas",
    "contrato",
    "contratos",
    "infraestructura",
    "inversión pública",
    "inversiones",
    "expediente técnico",
    "valorización",
    "valorizaciones",
    "reajuste",
    "reajustes",
    "peritaje",
    "peritajes",
    "arbitraje",
    "arbitrajes",
    "tasación",
    "tasaciones",
    "controversia",
    "controversias",
    "Ley 32069",
    "Ley N.° 32069",
    "Ley 30225"

]


# =====================================================
# CATEGORIZAR NOTICIA
# =====================================================

def categorizar(titulo, resumen):

    texto = (
        titulo + " " + resumen
    ).lower()


    if any(
        palabra in texto
        for palabra in [
            "liquidación",
            "liquidaciones",
            "valorización",
            "reajuste",
            "reajustes"
        ]
    ):

        return "Liquidación de Obras"


    if any(
        palabra in texto
        for palabra in [
            "peritaje",
            "peritajes",
            "arbitraje",
            "arbitrajes",
            "controversia",
            "controversias"
        ]
    ):

        return "Peritajes y Controversias"


    if any(
        palabra in texto
        for palabra in [
            "tasación",
            "tasaciones"
        ]
    ):

        return "Tasaciones"


    if any(
        palabra in texto
        for palabra in [
            "contratación",
            "contrataciones",
            "contrato",
            "contratos",
            "ley 32069",
            "ley n.° 32069",
            "ley 30225"
        ]
    ):

        return "Contratación Pública"


    return "Obras Públicas"


# =====================================================
# LIMPIAR TEXTO
# =====================================================

def limpiar(texto):

    texto = re.sub(
        r"<[^>]+>",
        "",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


# =====================================================
# OBTENER RSS
# =====================================================

def obtener_noticias():

    noticias = []


    # -------------------------------------------------
    # NOTA
    # -------------------------------------------------
    # Las fuentes oficiales pueden cambiar sus URLs RSS.
    # Se dejan configuradas para ampliar posteriormente.
    # -------------------------------------------------

    feeds = [

        {
            "fuente": "OECE",
            "url": "https://www.gob.pe/institucion/oece/noticias.rss"
        },

        {
            "fuente": "MEF",
            "url": "https://www.gob.pe/institucion/mef/noticias.rss"
        }

    ]


    for feed_info in feeds:

        try:

            feed = feedparser.parse(
                feed_info["url"]
            )


            for item in feed.entries[:20]:

                titulo = limpiar(
                    item.get(
                        "title",
                        ""
                    )
                )


                resumen = limpiar(
                    item.get(
                        "summary",
                        ""
                    )
                )


                enlace = item.get(
                    "link",
                    ""
                )


                texto_busqueda = (
                    titulo + " " + resumen
                ).lower()


                relevante = any(

                    palabra.lower()
                    in texto_busqueda

                    for palabra
                    in PALABRAS_CLAVE

                )


                if not relevante:

                    continue


                noticias.append({

                    "titulo":
                        titulo,

                    "categoria":
                        categorizar(
                            titulo,
                            resumen
                        ),

                    "resumen":
                        resumen[:350],

                    "fecha":
                        datetime.now(
                            timezone.utc
                        ).strftime(
                            "%Y-%m-%d"
                        ),

                    "fuente":
                        feed_info["fuente"],

                    "url":
                        enlace

                })


        except Exception as error:

            print(
                "Error consultando",
                feed_info["fuente"],
                error
            )


    return noticias


# =====================================================
# GUARDAR NOTICIAS
# =====================================================

def guardar_noticias(noticias):

    archivo = {

        "actualizado":
            datetime.now(
                timezone.utc
            ).strftime(
                "%Y-%m-%d %H:%M UTC"
            ),

        "noticias":
            noticias[:12]

    }


    with open(
        "noticias.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(

            archivo,

            f,

            ensure_ascii=False,

            indent=2

        )


# =====================================================
# EJECUCIÓN
# =====================================================

if __name__ == "__main__":

    print(
        "Buscando noticias..."
    )


    noticias = obtener_noticias()


    print(
        "Noticias encontradas:",
        len(noticias)
    )


    guardar_noticias(
        noticias
    )


    print(
        "noticias.json actualizado."
    )
