
import traceback
from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal, Slot

from automation.core.controller import RunController, StopRequested
from automation.core.pipeline import run_pipeline


class PipelineWorker(QObject):
    started = Signal()
    finished = Signal()
    stopped = Signal(str)   # motivo/label opcional
    error = Signal(str)     # mensagem + stacktrace (string)
    log = Signal(str)       # opcional: logs do pipeline

    def __init__(self, controller: RunController, num_registros: int) -> None:
        super().__init__()
        self._controller = controller
        self._num_registros = int(num_registros)

    @Slot()
    def run(self) -> None:
        self.started.emit()
        try:
            run_pipeline(self._controller, self._num_registros)

        except StopRequested as e:
            # stop solicitado (botão "Parar" na UI chama controller.stop())
            self.stopped.emit(str(e))

        except Exception:
            # erro inesperado: envie stacktrace para depuração
            tb = traceback.format_exc()
            self.error.emit(tb)

        finally:
            self.finished.emit()

    # Botões de controle da UI chamam esses slots
    @Slot()
    def pause(self) -> None:
        self._controller.pause()

    @Slot()
    def resume(self) -> None:
        self._controller.resume()

    @Slot()
    def stop(self) -> None:
        self._controller.stop()