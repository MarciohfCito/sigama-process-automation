from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QThread
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QScreen

from automation.core.controller import RunController
from automation.core.worker import PipelineWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = Path(__file__).parent / "resources" / "main_window.ui"
        loader = QUiLoader()
        self.ui = loader.load(str(ui_path))
        self.setCentralWidget(self.ui)

        self.setWindowTitle("SIGAMA Automation (Dev)")

        #define tamanho da tela
        self.setFixedSize(400, 300)

        #centraliza tela
        screen = self.screen().availableGeometry()
        window = self.frameGeometry()
        window.moveCenter(screen.center())
        self.move(window.topLeft())

        self._controller = None
        self._thread = None
        self._worker = None

        self._connect_signals()
        self._set_idle_state()

    def _connect_signals(self):
        self.ui.btnStart.clicked.connect(self._on_start)
        self.ui.btnPause.clicked.connect(self._on_pause)
        self.ui.btnResume.clicked.connect(self._on_resume)
        self.ui.btnStop.clicked.connect(self._on_stop)

    def _set_idle_state(self):
        self.ui.btnStart.setEnabled(True)
        self.ui.btnPause.setEnabled(False)
        self.ui.btnResume.setEnabled(False)
        self.ui.btnStop.setEnabled(False)
        self.ui.spinNumRegistros.setEnabled(True)
        self.ui.status.setText("Status: ocioso")

    def _set_running_state(self) -> None:
        self.ui.btnStart.setEnabled(False)
        self.ui.btnPause.setEnabled(True)
        self.ui.btnResume.setEnabled(False)
        self.ui.btnStop.setEnabled(True)
        self.ui.spinNumRegistros.setEnabled(False)
        self._set_status("rodando")

    def _set_paused_state(self) -> None:
        self.ui.btnStart.setEnabled(False)
        self.ui.btnPause.setEnabled(False)
        self.ui.btnResume.setEnabled(True)
        self.ui.btnStop.setEnabled(True)
        self.ui.spinNumRegistros.setEnabled(False)
        self._set_status("pausado")

    def _set_status(self, text: str) -> None:
        self.ui.status.setText(f"Status: {text}")

    def _log(self, msg: str) -> None:
        self.ui.txtLog.appendPlainText(msg)


    def _on_start(self):
        if self._thread is not None and self._thread.isRunning():
            QMessageBox.warning(self, "Aviso", "Já existe uma execução em andamento.")
            return

        num = int(self.ui.spinNumRegistros.value())

        self._controller = RunController()
        self._thread = QThread(self)
        self._worker = PipelineWorker(self._controller, num)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._thread.quit)

        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._worker.started.connect(self._set_running_state)
        self._worker.error.connect(self._on_worker_error)
        self._worker.stopped.connect(self._on_worker_stopped)
        self._worker.finished.connect(self._on_worker_finished)

        self._thread.start()


    def _on_pause(self) -> None:
        if not self._controller:
            return
        self._controller.pause()
        self._log("Pausado pelo usuário.")
        self._set_paused_state()

    def _on_resume(self) -> None:
        if not self._controller:
            return
        self._controller.resume()
        self._log("Continuando...")
        self._set_running_state()

    def _on_stop(self) -> None:
        if not self._controller:
            return
        self._controller.stop()
        self._log("Parar solicitado. Aguardando ponto seguro (checkpoint)...")
        self._set_status("parando...")


    def _on_worker_stopped(self, reason: str) -> None:
        self._log(f"Execução encerrada pelo usuário. Motivo: {reason}")

    def _on_worker_error(self, tb: str) -> None:
        self._log("Erro inesperado no pipeline:")
        self._log(tb)
        QMessageBox.critical(self, "Erro no pipeline", "Ocorreu um erro. Veja os logs.")

    def _on_worker_finished(self) -> None:
        self._log("Worker finalizado.")
        self._cleanup_thread_objects()
        self._set_idle_state()

    def _cleanup_thread_objects(self) -> None:
        self._thread = None
        self._worker = None
        self._controller = None


    def closeEvent(self, event) -> None:
        # Se estiver rodando, tenta parar antes de fechar
        if self._controller and self._thread and self._thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Sair",
                "Há uma execução em andamento. Deseja parar e sair?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                event.ignore()
                return

            self._controller.stop()
            self._set_status("parando...")
            self._thread.quit()
            self._thread.wait(1500)

        event.accept()
