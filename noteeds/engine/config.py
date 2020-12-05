from dataclasses import dataclass

from PySide2.QtCore import QSettings
from PySide2.QtGui import QKeySequence

from noteeds.engine.repository import Config as RepositoryConfig


@dataclass(frozen=True)
class GuiConfig:
    use_systray: bool
    use_global_hotkey: bool
    global_hotkey: QKeySequence

    def store(self, settings: QSettings):
        settings.setValue("use_systray", self.use_systray)
        settings.setValue("use_global_hotkey", self.use_global_hotkey)
        settings.setValue("global_hotkey", self.global_hotkey.toString())

    @classmethod
    def load(cls, settings: QSettings):
        return cls(
            use_systray=settings.value("use_systray", True, bool),
            use_global_hotkey=settings.value("use_global_hotkey", True, bool),
            global_hotkey=QKeySequence.fromString(settings.value("global_hotkey", "", str)),
        )


@dataclass(frozen=True)
class Config:
    gui: GuiConfig
    repositories: list[RepositoryConfig]

    def store(self, settings: QSettings):
        settings.beginGroup("gui")
        self.gui.store(settings)
        settings.endGroup()

        settings.beginWriteArray("repos")
        for i, repo in enumerate(self.repositories):
            settings.setArrayIndex(i)
            repo.store(settings)
        settings.endArray()

    @classmethod
    def load(cls, settings: QSettings):
        settings.beginGroup("gui")
        gui = GuiConfig.load(settings)
        settings.endGroup()

        repo_count = settings.beginReadArray("repos")
        repos = []
        for i in range(repo_count):
            settings.setArrayIndex(i)
            repos.append(RepositoryConfig.load(settings))
        settings.endArray()

        return cls(
            gui=gui,
            repositories=repos,
        )
