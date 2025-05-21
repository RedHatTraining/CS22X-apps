# Copyright (C) 2024 Red Hat, Inc.
#
# This file is part of the CS221 Red Hat course.
#
# This is a free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# The software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Simulate generating metrics for an online store."""

import threading
import random
import time

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge, Counter


application = Flask(__name__)

# Add prometheus WSGI middleware to route /metrics requests
application.wsgi_app = DispatcherMiddleware(
    application.wsgi_app, {"/metrics": make_wsgi_app()}
)


def purchase_cart(c):
    c["items"].inc(random.randint(1, 10))
    c["total_revenue"].inc(random.randint(10, 200))
    c["cart_purchase"].inc()


def abandon_cart(c):
    c["cart_abandonment"].inc()


def refund_items(c):
    c["refund"].inc()


def generate_cart_metrics():
    """Generate random data for shopping cart metrics."""
    counters = {
        "cart_purchase": Counter("cart_purchase", "Number of purchased shopping carts"),
        "cart_abandonment": Counter(
            "cart_abandonment", "Number of abandoned shopping carts"
        ),
        "total_revenue": Counter("revenue", "Total revenue"),
        "items": Counter("items", "Number of items purchased"),
        "refund": Counter("refund", "Number of items customers returned"),
    }

    functions = [purchase_cart, abandon_cart, refund_items]

    while True:
        f = random.choice(functions)
        f(counters)
        time.sleep(0.5)


def generate_concurrent_user_metrics():
    """Generate random data for the concurrent user metric."""
    g = Gauge("concurrent_users", "Number of connected users")
    n = 0
    while True:
        r = random.randint(100, 400)
        while r > 0:
            n += random.randint(1, 5)
            g.set(n)
            r -= 1
            time.sleep(0.1)

        r = random.randint(100, 400)
        while r > 0:
            n -= random.randint(1, 5)
            if n <= 0:
                n = 0
                break
            g.set(n)
            r -= 1
            time.sleep(0.1)


@application.route("/")
def hello_world():
    """Fake home page"""
    return "<p>Hello, World!</p>"


@application.route("/health")
def health():
    """Application health check"""
    return {"status": 200, "title": "OK"}, 200


# Start generating random metrics in the background
t1 = threading.Thread(target=generate_cart_metrics)
t1.start()
t2 = threading.Thread(target=generate_concurrent_user_metrics)
t2.start()


if __name__ == "__main__":
    application.run()
