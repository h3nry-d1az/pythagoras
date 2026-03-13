from itertools import chain

from .pobject import POProperty

__options_dict = {"fill": ("fill", "fill"), "color": ("color", "stroke")}


def tikz_command(name: str, body: str, *args: str, **kwargs: POProperty) -> str:
    if args or kwargs:
        kwargs_ = (f"{p[0]}={p[1]}" for p in sorted(kwargs.items(), key=lambda p: p[0]))
        params = f"[{', '.join(chain(args, kwargs_))}]"
    else:
        params = ""
    return rf"\{name}{params} {body};"


def svg_command(name: str, *args: str, **kwargs: POProperty) -> str:
    if args or kwargs:
        kwargs_ = (f'{p[0]}="{p[1]}"' for p in kwargs.items())
        params = " ".join(chain(args, kwargs_))
    else:
        params = ""
    return rf"<{name} {params} />"


def compile_options_tikz(config: dict[str, POProperty]) -> None:
    for k, (v, _) in __options_dict.items():
        if k in config and k != v:
            config[v] = config[k]
            del config[k]


def compile_options_svg(config: dict[str, POProperty]) -> None:
    for k, (_, v) in __options_dict.items():
        if k in config and k != v:
            config[v] = config[k]
            del config[k]
