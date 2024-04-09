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

"""
Send random JSON log messages of various log levels infinitely to stdout.

Uses the SHOULD_BREAK env variable.
When it is set to "true" app only logs ERROR and DEBUG messages.
Otherwise by default it is set to false, it logs INFO & WARNING messages.
"""

import os
import json
import logging
import random
import time

# Define log message dataset
LOG_MESSAGES = {
    'INFO': [
        "Data synchronization started.",
        "Data synchronization completed successfully.",
        "Database connection established.",
        "New user 'Alice' registered.",
        "User 'Bob' updated profile information.",
        "Email notification sent to all subscribers.",
        "Server started on port 8080.",
        "Incoming request: GET /api/data",
        "Data fetched from database.",
        "Data sent to client successfully."
    ],
    'WARNING': [
        "Database connection lost, retrying...",
        "Low disk space detected on server.",
        "Invalid request received, ignoring...",
        "Unauthorized access attempt detected.",
        "CPU temperature above threshold, cooling system activated.",
        "Network congestion detected.",
        "SSL certificate expires in 7 days.",
        "Unusual behavior detected, monitoring...",
        "Memory usage approaching maximum limit.",
        "Disk usage exceeding 90%."
    ],
    'DEBUG': [
        "Query: SELECT * FROM users WHERE id = 123",
        "Variable 'x' has value 10.",
        "Function 'calculate_total()' called.",
        "Incoming request data: {'user_id': 123, 'action': 'update'}",
        "Response data sent: {'status': 'success'}",
        "Executing background task: cleanup_old_logs()",
        "Initializing logging system.",
        "Preparing response: {'message': 'Hello, World!'}",
        "Connecting to external API: https://api.example.com",
        "Parsing configuration file: config.json"
    ],
    'ERROR': [
        "Failed to establish database connection.",
        "Internal server error occurred.",
        "File not found: 'config.ini'.",
        "Unhandled exception occurred.",
        "Invalid input format received from client.",
        "Server crashed, restarting...",
        "Critical error: disk failure detected.",
        "Database query failed: Table 'users' not found.",
        "Network error: Connection timed out.",
        "Permission denied to access file: 'log.txt'"
    ]
}

# Configure logging to output in JSON format
logging.basicConfig(level=logging.INFO, format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')

def generate_log(should_break):
    if should_break:
        levels = ['ERROR', 'DEBUG']
    else:
        levels = ['INFO', 'WARNING']
    level = random.choice(levels)
    message = random.choice(LOG_MESSAGES[level])
    logging.log(level=logging.getLevelName(level), msg=json.dumps(message))

def main():
    should_break = os.environ.get("SHOULD_BREAK", "false").lower() == "true"
    while True:
        generate_log(should_break)
        time.sleep(random.randint(1, 5))

if __name__ == "__main__":
    main()
