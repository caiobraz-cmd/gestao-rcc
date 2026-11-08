"""Limites por processo para a instalação local; não usa cabeçalhos de proxy."""
from hashlib import sha256
import hmac
from math import ceil
from threading import Lock
from time import monotonic
from flask import current_app, request


class AttemptLimiter:
    def __init__(self, window=300, capacity=4096, clock=monotonic):
        self.window, self.capacity, self.clock = window, capacity, clock
        self.entries = {}
        self.lock = Lock()

    def consume(self, limits):
        with self.lock:
            now = self.clock()
            self.entries = {k: v for k, v in self.entries.items() if v[1] > now}
            waits = [ceil(self.entries[k][1] - now) for k, maximum in limits
                     if k in self.entries and self.entries[k][0] >= maximum]
            if waits:
                return max(1, max(waits))
            missing = sum(k not in self.entries for k, _ in limits)
            if len(self.entries) + missing > self.capacity:
                return max(1, ceil(min(v[1] for v in self.entries.values()) - now))
            for k, _ in limits:
                count, until = self.entries.get(k, (0, now + self.window))
                self.entries[k] = (count + 1, until)
            return 0


def check_attempts(purpose, username):
    secret = current_app.config['SECRET_KEY'].encode()
    def key(kind, value):
        return hmac.new(secret, (purpose + ':' + kind + ':' + value).encode(), sha256).digest()
    return current_app.extensions['access_limiter'].consume([
        (key('account', username), 5),
        (key('network', request.remote_addr or 'unknown'), 30),
    ])
