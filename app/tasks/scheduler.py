from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from datetime import timedelta

logger = logging.getLogger(__name__)


class ScheduledTask:
    def __init__(self, name: str, interval: timedelta, func: Callable[[], None]):
        self.name = name
        self.interval = interval
        self.func = func
        self._timer: threading.Timer | None = None

    def start(self) -> None:
        logger.debug("Iniciando tarea programada %s", self.name)
        self._schedule_next()

    def _schedule_next(self) -> None:
        self._timer = threading.Timer(self.interval.total_seconds(), self._run)
        self._timer.daemon = True
        self._timer.start()

    def _run(self) -> None:
        try:
            logger.info("Ejecutando tarea programada %s", self.name)
            self.func()
        finally:
            self._schedule_next()

    def cancel(self) -> None:
        if self._timer:
            logger.debug("Cancelando tarea %s", self.name)
            self._timer.cancel()
            self._timer = None


class Scheduler:
    """Orquestador muy simple basado en `threading.Timer`."""

    def __init__(self) -> None:
        self._tasks: list[ScheduledTask] = []

    def add_task(self, name: str, interval: timedelta, func: Callable[[], None]) -> None:
        task = ScheduledTask(name, interval, func)
        self._tasks.append(task)
        task.start()

    def stop_all(self) -> None:
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()


scheduler = Scheduler()