from trackbuilder import TrackBuilder
from typing import Type


class Chainer:
    def __init__(self, name: str = "") -> None:
        self.current_module = TrackBuilder(name)

    def chain(self, module: Type[TrackBuilder] , method: str, args: dict) -> None:

        module.inherit_state(self.current_module)

        getattr(module, method)(**args)

        self.current_module = module

    def export(self, name: str = "") -> str:
        return self.current_module.export()