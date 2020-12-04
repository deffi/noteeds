from dataclasses import dataclass

from PySide2.QtGui import QKeySequence

from noteeds.engine.repository import Config as RepositoryConfig


@dataclass(frozen=True)
class GuiConfig:
    use_systray: bool
    use_global_hotkey: bool
    global_hotkey: QKeySequence


@dataclass(frozen=True)
class Config:
    gui: GuiConfig
    repositories: list[RepositoryConfig]
