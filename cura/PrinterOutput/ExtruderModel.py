# Copyright (c) 2017 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from PyQt5.QtCore import pyqtSignal, pyqtProperty, QObject, QVariant, pyqtSlot
from UM.Logger import Logger

from typing import Optional

MYPY = False
if MYPY:
    from cura.PrinterOutput.PrinterModel import PrinterModel
    from cura.PrinterOutput.MaterialModel import MaterialModel


class ExtruderModel(QObject):
    hotendIDChanged = pyqtSignal()
    targetHotendTemperatureChanged = pyqtSignal()
    hotendTemperatureChanged = pyqtSignal()
    activeMaterialChanged = pyqtSignal()

    def __init__(self, printer: "PrinterModel", parent=None):
        super().__init__(parent)
        self._printer = printer
        self._target_hotend_temperature = 0
        self._hotend_temperature = 0
        self._hotend_id = ""
        self._active_material = None  # type: Optional[MaterialModel]

    @pyqtProperty(QObject, notify = activeMaterialChanged)
    def activeMaterial(self) -> "MaterialModel":
        return self._active_material

    def updateActiveMaterial(self, material: Optional["MaterialModel"]):
        if self._active_material != material:
            self._active_material = material
            self.activeMaterialChanged.emit()

    ##  Update the hotend temperature. This only changes it locally.
    def updateHotendTemperature(self, temperature: int):
        if self._hotend_temperature != temperature:
            self._hotend_temperature = temperature
            self.hotendTemperatureChanged.emit()

    def updateTargetHotendTemperature(self, temperature: int):
        if self._target_hotend_temperature != temperature:
            self._target_hotend_temperature = temperature
            self.targetHotendTemperatureChanged.emit()

    ##  Set the target hotend temperature. This ensures that it's actually sent to the remote.
    @pyqtSlot(int)
    def setTargetHotendTemperature(self, temperature: int):
        self._setTargetHotendTemperature(temperature)
        self.updateTargetHotendTemperature(temperature)

    @pyqtProperty(int, notify = targetHotendTemperatureChanged)
    def targetHotendTemperature(self) -> int:
        return self._target_hotend_temperature

    @pyqtProperty(int, notify=hotendTemperatureChanged)
    def hotendTemperature(self) -> int:
        return self._hotendTemperature

    ##  Protected setter for the hotend temperature of the connected printer (if any).
    #   /parameter temperature Temperature hotend needs to go to (in deg celsius)
    #   /sa setTargetHotendTemperature
    def _setTargetHotendTemperature(self, temperature):
        Logger.log("w", "_setTargetHotendTemperature is not implemented by this model")

    @pyqtProperty(str, notify = hotendIDChanged)
    def hotendID(self) -> str:
        return self._hotend_id

    def updateHotendID(self, id: str):
        if self._hotend_id != id:
            self._hotend_id = id
            self.hotendIDChanged.emit()