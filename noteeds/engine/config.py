from dataclasses import dataclass

from noteeds.engine.repository import Config as RepositoryConfig


@dataclass(frozen=True)
class GuiConfig:
    use_systray: bool
    use_global_hotkey: bool
    global_hotkey: tuple[str, ...]


@dataclass(frozen=True)
class Config:
    gui: GuiConfig
    repositories: list[RepositoryConfig]
