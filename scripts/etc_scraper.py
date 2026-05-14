import re
from argparse import ArgumentParser
from functools import reduce
from sys import exit

import requests
from bs4 import BeautifulSoup


def replace_dict(text: str, keys: dict[str, str]) -> str:
    return reduce(lambda acc, kp: acc.replace(kp[0], kp[1]), keys.items(), initial=text)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def compile(text: str) -> str:
    return ", ".join(
        c
        if (
            c := replace_dict(
                coord,
                {
                    "a": "t.a",
                    "b": "t.b",
                    "c": "t.c",
                    "A": "t.alpha",
                    "B": "t.beta",
                    "C": "t.gamma",
                    "sec": "__sec",
                    "csc": "__csc",
                    "cot": "__cot",
                    "^": "**",
                },
            ).strip()
        )
        else "0"
        for coord in text.split(":")
    )


def scrape(url: str, logging: bool = False) -> str:
    centers = """from collections.abc import Callable
from math import acos, asin, atan, cos, pi, sin, tan

from ..triangle import GenericBarycentric

__sec: Callable[[float], float] = lambda t: 1 / cos(t)  # noqa: E731
__csc: Callable[[float], float] = lambda t: 1 / sin(t)  # noqa: E731
__cot: Callable[[float], float] = lambda t: 1 / tan(t)  # noqa: E731
"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        if logging:
            print(f"Successfully fetched file `{url}'")

        text = clean(
            BeautifulSoup(response.content, "html.parser").get_text(separator=" ")
        )
        blocks = re.split(r"(?=\bX\(\d+\)\s*=)", text)
        seen: set[str] = set()

        for block in blocks:
            name_match = re.match(
                r"X\((\d+)\)\s*=\s*(.*?)(?=\s*(?:Barycentrics|Trilinears|Tripolars|As a center|\bX\(\d+\)|$))",
                block,
                re.IGNORECASE,
            )

            if not name_match:
                continue

            n = name_match.group(1)
            if n in seen:
                continue
            seen.add(n)

            name = name_match.group(2).strip().replace('"', '\\"')
            bary_match = re.search(
                r"\bBarycentrics\s*(?:are|=)?\s*(.*?)(?=\.\s+[a-z]{2,}|\b(?:Trilinears|Tripolars)\b|\bX\(\d+\)|$)",
                block,
                re.IGNORECASE,
            )
            barycentrics = bary_match.group(1).strip() if bary_match else "None"
            if barycentrics.endswith("."):
                barycentrics = barycentrics[:-1].strip()

            centers += f"X{n}: GenericBarycentric = lambda t: ({compile(barycentrics)})  # noqa: E731\n"
            centers += f'X{n}.__doc__ = "{name}"\n'

            if logging:
                print(f"Compiled center X{n}")

    except Exception as e:
        print(f"Error while fetching `{url}':", e, sep="\n")
        exit(1)

    centers += f"""\n__all__ = [{", ".join(f'"X{n}"' for n in seen)}]"""
    return centers


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="etc_scraper",
        description="Script to scrape Clark Kimberling's Encyclopedia of Triangle Centers",
        epilog="Made to populate the module `triangle.etc` in the Pythagoras package",
    )
    parser.add_argument(
        "volume", type=int, nargs=1, metavar="volume", help="volume to be scraped"
    )
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    args = parser.parse_args()
    vol, log = args.volume[0], args.verbose
    with open(f"volume{vol}.py", "w", encoding="utf-8") as f:
        f.write(
            scrape(
                "https://faculty.evansville.edu/ck6/encyclopedia/ETC.html"
                if vol == 1
                else f"https://faculty.evansville.edu/ck6/encyclopedia/ETCPart{vol}.html",
                log,
            )
        )
