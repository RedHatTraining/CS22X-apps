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

"""Send test messages in an infinite loop to an Amazon SQS queue.

For authenticating with the AWS API, the program expects the following
environment variables:

.. envvar:: AWS_DEFAULT_REGION
   The AWS Region.
.. envvar:: AWS_ROLE_ARN
   The Amazon Resource Name (ARN) of the IAM role that has permissions to send
   messages to the Amazon SQS queue.
.. envvar:: AWS_WEB_IDENTITY_TOKEN_FILE
   The path to a file that contains the JSON Web Token (JWT) token that the
   OIDC identity provider supplies.

These environment variables are used by the :py:mod:`boto3` module.
The :envvar:`AWS_ROLE_ARN` and :envvar:`AWS_WEB_IDENTITY_TOKEN_FILE` environment
variables, as well as the JWT file, are automatically set by the Kubernetes API
server when the pod starts.

The following environment variables are optional:

.. envvar:: AWS_SQS_QUEUE_NAME
   Name of the Amazon SQS queue. The program does not create that queue.
   Therefore, the queue must exist before the program starts.
   Defaults to `CS221-queue`
.. envvar:: MESSAGE_STRING
   String that contains the message to send to the queue. In the string, the
   `{num}` pattern is replaced by the message sequence number.
   Defaults to `Message #{num}`
"""


import os
import sys
import logging
import random
import time
import boto3
import botocore


def send_message(sqs, queue_url, msg):
    """Send an Amazon SQS message.

    :param sqs: A handle to the Amazon SQS service client.
    :type sqs: :py:class:`botocore.client.BaseClient`
    :param queue_url: The name of the Amazon SQS queue.
    :type queue_url: str
    :param msg: Message to send to the queue.
    :type msg: str
    """
    try:
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=msg)
    except (
        botocore.exceptions.BotoCoreError,
        botocore.exceptions.ClientError,
    ) as error:
        logging.critical(error)
        sys.exit(1)
    msg_id = response["MessageId"]
    logging.info(f"Message sent: {msg_id}: {msg}")


def main():
    """Main function."""
    SQS_QUEUE_URL = os.environ.get("AWS_SQS_QUEUE_NAME", "CS221-queue")
    MESSAGE_STRING = os.environ.get("MESSAGE_STRING", "Message #{num}")

    logging.basicConfig(level=logging.INFO)

    # Create the Amazon SQS service client.
    try:
        sqs = boto3.client("sqs")
    except botocore.exceptions.BotoCoreError as error:
        logging.critical(error)
        sys.exit(1)

    # Send a few messages as soon as the pod starts so that students see some
    # messages when they access the SQS queue from the AWS Management Console.
    num = 1
    while num <= 4:
        send_message(sqs, SQS_QUEUE_URL, MESSAGE_STRING.format(num=num))
        time.sleep(random.randint(1, 5))
        num += 1

    # After the few initial messages, send messages at a slower pace.
    while True:
        send_message(sqs, SQS_QUEUE_URL, MESSAGE_STRING.format(num=num))
        time.sleep(random.randint(15, 60))
        num += 1


if __name__ == "__main__":
    main()
