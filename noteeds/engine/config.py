from dataclasses import dataclass

from PySide6.QtCore import QSettings
from PySide6.QtGui import QKeySequence

from noteeds.engine.repository import Config as RepositoryConfig


@dataclass(frozen=True)
class GuiConfig:
    close_to_systray: bool
    use_global_hotkey: bool
    global_hotkey: QKeySequence
    external_editor: str

    def store(self, settings: QSettings):
        settings.setValue("close_to_systray", self.close_to_systray)
        settings.setValue("use_global_hotkey", self.use_global_hotkey)
        settings.setValue("global_hotkey", self.global_hotkey.toString())
        settings.setValue("external_editor", self.external_editor)

    @classmethod
    def load(cls, settings: QSettings):
        return cls(
            close_to_systray=settings.value("close_to_systray", True, bool),
            use_global_hotkey=settings.value("use_global_hotkey", False, bool),
            global_hotkey=QKeySequence.fromString(settings.value("global_hotkey", "", str)),
            external_editor=settings.value("external_editor", "")
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
