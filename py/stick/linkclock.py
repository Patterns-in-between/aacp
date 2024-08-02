# (c) Damian Silvani, Alex Mclean and contributors
# Distributed under the terms of the GNU Public License version 3

import logging
import math
import threading
import time
#import importlib
#import contextlib

import link

import link

_logger = logging.getLogger(__name__)


class LinkClock:
    """
    This class handles synchronization between different devices using the Link
    protocol.

    You can subscribe other objects (i.e. Streams), which will be notified on
    each clock tick. It expects that subscribers define a `notify_tick` method.

    Parameters
    ----------
    bpm: float
        beats per minute (default: 120)

    """

    def __init__(self, bpm=120, bpc=4, latency=0):
        self.bpm = bpm
        self.bpc = bpc
        self.latency_micros = math.floor(latency * 1000000.0)

        self._subscribers = []
        self._link = link.Link(bpm)
        self._is_running = False
        self._mutex = threading.Lock()

    def subscribe(self, subscriber):
        """Subscribe an object to tick notifications"""
        with self._mutex:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        """Unsubscribe from tick notifications"""
        with self._mutex:
            self._subscribers.remove(subscriber)

    def start(self):
        """Start the clock"""
        with self._mutex:
            if self._is_running:
                return
            self._is_running = True
        self._start = self._link.clock().micros()
        self._create_notify_thread()

    def cyclePos(self):
        s = self._link.captureSessionState()
        now = self._link.clock().micros()
        t = s.beatAtTime(now, self.bpc) / self.bpc
        #print(t)
        #print(s.tempo())
        return t

    def beat(self):
        s = self._link.captureSessionState()
        now = self._link.clock().micros()
        return math.floor(s.beatAtTime(now, self.bpc))

    def stop(self):
        """Stop the clock"""
        with self._mutex:
            self._is_running = False
        # Wait until thread has stopped
        # Will block until (at least) the next start of frame
        self._notify_thread.join()

    @property
    def is_playing(self):
        """Returns whether clock is currently running"""
        return self._is_running

    def _create_notify_thread(self):
        self._notify_thread = threading.Thread(target=self._notify_thread_target)
        self._notify_thread.start()

    def _notify_thread_target(self):
        _logger.info("Link enabled")
        self._link.enabled = True
        self._link.startStopSyncEnabled = True

        start = self._link.clock().micros()
        mill = 1000000
        start_beat = self._link.captureSessionState().beatAtTime(start, 4)
        _logger.info("Start beat: %f", start_beat)

        ticks = 0

        # FIXME rate and latency should be constructor parameters
        rate = 1 / 20
        frame = rate * mill

        while self._is_running:
            ticks = ticks + 1

            logical_now = math.floor(start + (ticks * frame))
            logical_next = math.floor(start + ((ticks + 1) * frame))

            now = self._link.clock().micros()

            # wait until start of next frame
            wait = (logical_now - now) / mill
            if wait > 0:
                time.sleep(wait)

            if not self._is_running:
                break

            s = self._link.captureSessionState()
            cps = (s.tempo() / self.bpc) / 60
            cycle_from = s.beatAtTime(logical_now, 0) / self.bpc
            cycle_to = s.beatAtTime(logical_next, 0) / self.bpc

            for sub in self._subscribers:
                sub.notify_tick((cycle_from, cycle_to), s, cps, self.bpc, mill, now)

            # sys.stdout.write(
            #     "cps %.2f | playing %s | cycle %.2f\r"
            #     % (cps, s.isPlaying(), cycle_from)
            # )

            # sys.stdout.flush()

        self._link.enabled = False
        _logger.info("Link disabled")
        return
