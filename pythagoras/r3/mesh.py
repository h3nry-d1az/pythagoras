from collections.abc import Iterable
from dataclasses import dataclass
from math import atan, pi
from typing import Self, cast

from ..backend import fill_default_args, svg_path, tikz_command
from ..pobject import POProperty
from ..style.color import BLACK
from ..style.draw import Fill, LineWidth, Stroke
from ..utils import cartesian_to_canvas
from .camera import Camera3D
from .pobject import PObject3D
from .rendering import project_point
from .vector import Vector3D, dist3

__all__ = ["Face", "Mesh"]


@dataclass(init=False)
class Face(PObject3D):
    r"""
    Triangle in :math:`\mathbf R^3` which is meant to belong to a mesh.

    Attributes:
        v1: First vertex.
        v2: Second vertex.
        v3: Third vertex.
        n: Normal vector for lighting.
    """

    v1: tuple[float, float, float]
    v2: tuple[float, float, float]
    v3: tuple[float, float, float]
    n: Vector3D | None

    def __init__(
        self,
        v1: tuple[float, float, float],
        v2: tuple[float, float, float],
        v3: tuple[float, float, float],
        shaded: bool = True,
        zord: int = 0,
    ) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        if shaded:
            self.n = Vector3D.from_two_points(v1, v2) ^ Vector3D.from_two_points(v1, v3)
            self.n /= abs(self.n)
        else:
            self.n = None
        self._zord = zord

    @property
    def centroid(self) -> tuple[float, float, float]:
        return (
            (self.v1[0] + self.v2[0] + self.v3[0]) / 3,
            (self.v1[1] + self.v2[1] + self.v3[1]) / 3,
            (self.v1[2] + self.v2[2] + self.v3[2]) / 3,
        )

    def _apply_lighting(
        self,
        camera: Camera3D,
        frustum: float,
        light_sources: list[tuple[tuple[float, float, float], float]],
        args: Iterable[POProperty],
    ) -> Iterable[POProperty]:
        if not self.n:
            return args
        fargs: list[POProperty] = []
        color = None
        for arg in args:
            if isinstance(arg, Fill):
                color = arg.color
            else:
                fargs.append(arg)
        if color:
            light_factor = 0
            for p, i in light_sources:
                dist = Vector3D.from_two_points(p, self.centroid)
                light_factor = max(
                    light_factor,
                    (dist.unitary @ self.n) ** 2 * (2 * atan(i / abs(dist)) / pi),
                )
            color = color * light_factor
            fargs.append(Fill(color))
        return fargs

    def svg(
        self,
        camera: Camera3D,
        frustum: float,
        width: float,
        height: float,
        scale: float,
        lights: list[tuple[tuple[float, float, float], float]],
        *args: POProperty,
    ) -> str:
        ps = (
            project_point(camera, frustum, self.v1),
            project_point(camera, frustum, self.v2),
            project_point(camera, frustum, self.v3),
        )
        if not all(ps):
            return ""
        ps = (cartesian_to_canvas(*p, width, height, scale) for p in ps if p)
        return svg_path(
            ps,
            (0, 0),
            width,
            height,
            scale,
            *fill_default_args(
                self._apply_lighting(camera, frustum, lights, args),
                (Fill, Fill(None)),
                (Stroke, Stroke(BLACK)),
                (LineWidth, LineWidth(0.01)),
            ),
        )

    def tikz(
        self,
        camera: Camera3D,
        frustum: float,
        lights: list[tuple[tuple[float, float, float], float]],
        *args: POProperty,
    ) -> str:
        ps = (
            project_point(camera, frustum, self.v1),
            project_point(camera, frustum, self.v2),
            project_point(camera, frustum, self.v3),
        )
        if not all(ps):
            return ""
        ps = cast(
            tuple[tuple[float, float], tuple[float, float], tuple[float, float]], ps
        )
        return tikz_command(
            "draw",
            " -- ".join(f"({p[0]}, {p[1]})" for p in ps),
            *self._apply_lighting(camera, frustum, lights, args),
        )


class Mesh(PObject3D):
    """
    Three-dimensional mesh, represented as a collection of triangles. Vertices are also
    stored for efficient retrieval.

    Attributes:
        triangles: Triangles that make up the mesh, together with their properties.
        vertices: Vertices of the mesh.
    """

    triangles: tuple[tuple[Face, tuple[POProperty, ...]], ...]
    vertices: set[tuple[float, float, float]]

    def __init__(
        self,
        triangles: Iterable[tuple[Face, tuple[POProperty, ...]]],
        vertices: Iterable[tuple[float, float, float]] | None = None,
        zord: int = 0,
    ) -> None:
        self.triangles = tuple(triangles)
        self._zord = zord
        if vertices:
            self.vertices = set(vertices)
            return
        self.vertices = set()
        for pair in self.triangles:
            self.vertices.add(pair[0].v1)
            self.vertices.add(pair[0].v2)
            self.vertices.add(pair[0].v3)

    @classmethod
    def from_obj(
        cls, obj: str, shaded: bool = True, zord: int = 0, *args: POProperty
    ) -> Self:
        """
        Constructs a mesh from Wavefront OBJ-formatted string.
        It only supports the `v` and `f` commands, the remaining ones are ignored when encountered.

        Parameters:
            obj: 3D OBJ model.
            shaded: Whether to calculate face normals for shading.
            zord: Rendering priority within a :class:`Canvas3D <pythagoras.r3.canvas.Canvas3D>` context.
            args: Properties to apply globally to the mesh.

        Returns:
            A :class:`Mesh` instance.
        """
        vs: list[tuple[float, float, float]] = []
        fs: list[Face] = []
        for line in obj.splitlines():
            line = line.strip()
            if len(line) == 0:
                continue
            cmd = [w.lower() for w in line.split()]
            match cmd[0]:
                case "v":
                    params = [float(t.split("/")[0]) for t in cmd[1:]]
                    vs.append((params[0], params[1], params[2]))
                case "f":
                    params = [int(t.split("/")[0]) for t in cmd[1:]]
                    v1 = vs[i1 - 1 if (i1 := params[0]) > 0 else i1]
                    for i in range(1, len(params) - 1):
                        fs.append(
                            Face(
                                v1,
                                vs[i1 - 1 if (i1 := params[i]) > 0 else i1],
                                vs[i2 - 1 if (i2 := params[i + 1]) > 0 else i2],
                                shaded,
                            )
                        )
                case _:
                    continue
        return cls(((fi, args) for fi in fs), vs, zord)

    def translate(self, translation: tuple[float, float, float]) -> None:
        """
        Translates the mesh in some direction in space.

        Parameters:
            translation: Coordinates of the translation vector.
        """
        self.vertices = {
            (v[0] + translation[0], v[1] + translation[1], v[2] + translation[2])
            for v in self.vertices
        }
        for i in range(len(self.triangles)):
            v1, v2, v3 = (
                self.triangles[i][0].v1,
                self.triangles[i][0].v2,
                self.triangles[i][0].v3,
            )
            self.triangles[i][0].v1 = (
                v1[0] + translation[0],
                v1[1] + translation[1],
                v1[2] + translation[2],
            )
            self.triangles[i][0].v2 = (
                v2[0] + translation[0],
                v2[1] + translation[1],
                v2[2] + translation[2],
            )
            self.triangles[i][0].v3 = (
                v3[0] + translation[0],
                v3[1] + translation[1],
                v3[2] + translation[2],
            )

    def svg(
        self,
        camera: Camera3D,
        frustum: float,
        width: float,
        height: float,
        scale: float,
        lights: list[tuple[tuple[float, float, float], float]],
        *args: POProperty,
    ) -> str:
        return (
            "<g>"
            + "\n".join(
                p[0].svg(camera, frustum, width, height, scale, lights, *p[1], *args)
                for p in sorted(
                    self.triangles,
                    key=lambda p: dist3(p[0].centroid, camera.position),
                    reverse=True,
                )
            )
            + "\n</g>"
        )

    def tikz(
        self,
        camera: Camera3D,
        frustum: float,
        lights: list[tuple[tuple[float, float, float], float]],
        *args: POProperty,
    ) -> str:
        return "\n".join(
            p[0].tikz(camera, frustum, lights, *p[1], *args)
            for p in sorted(
                self.triangles,
                key=lambda p: dist3(p[0].centroid, camera.position),
                reverse=True,
            )
        )
