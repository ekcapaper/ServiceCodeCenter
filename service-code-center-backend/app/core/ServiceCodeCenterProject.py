from dataclasses import dataclass, asdict
import pathlib

@dataclass
class ServiceCodeCenterProject:
    id_: int
    name: str
    description: str
    entrypoint: str
    working_directory: pathlib.Path
