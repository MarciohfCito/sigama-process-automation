from dataclasses import dataclass, field
from threading import Event, Lock


class StopRequested(Exception):
    """Sinaliza encerramento solicitado pelo usuário."""
    pass


@dataclass
class RunController:
    """
    Controller cooperativo para controlar o pipeline:
    - pause/resume: pausa bloqueante até retomar
    - stop: encerra o pipeline com segurança (via StopRequested)
    """
    _pause_event: Event = field(default_factory=Event, init=False)
    _stop_event: Event = field(default_factory=Event, init=False)
    _lock: Lock = field(default_factory=Lock, init=False)

    def __post_init__(self) -> None:
        self._pause_event.set()


    def pause(self) -> None:
        with self._lock:
            if not self._stop_event.is_set():
                self._pause_event.clear()

    def resume(self) -> None:
        with self._lock:
            self._pause_event.set()

    def stop(self) -> None:
        with self._lock:
            self._stop_event.set()
            self._pause_event.set()


    def is_paused(self) -> bool:
        return not self._pause_event.is_set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()


    def checkpoint(self, label: str | None = None, timeout: float | None = None) -> None:
        """
        Chame frequentemente no pipeline, especialmente antes de ações com efeito colateral:
        - cliques
        - downloads
        - salvar Excel
        - mover/copiar arquivos

        Se pausado: bloqueia até retomar.
        Se stop: levanta StopRequested.
        """
        if self._stop_event.is_set():
            raise StopRequested(label or "stop")

        ok = self._pause_event.wait(timeout=timeout)
        if not ok:
            return

        if self._stop_event.is_set():
            raise StopRequested(label or "stop")
