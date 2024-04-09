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
Send random log messages in JSON format to mimic logs of a shopping app
"""



import logging
import random
import time

# Configure logging to output in JSON format
logging.basicConfig(level=logging.INFO, format='{"timestamp": "%(asctime)s", "message": %(message)s}')

# Define business activities and corresponding log messages
BUSINESS_ACTIVITIES = {
    'User Interaction': [
        "User 'Alice' viewed product 'iPhone 12'.",
        "User 'Bob' searched for 'laptop'.",
        "User 'Charlie' clicked on a banner ad.",
        "User 'David' visited the homepage.",
        "User 'Eve' logged in to the account.",
        "User 'Frank' added item 'Samsung Galaxy Watch' to the wishlist.",
        "User 'Grace' subscribed to the newsletter.",
        "User 'Hannah' updated profile information.",
        "User 'Isaac' posted a review for product 'AirPods Pro'.",
        "User 'Jack' shared a product link on social media."
    ],
    'Checkout': [
        "User 'Alice' completed checkout for product 'iPhone 12'.",
        "User 'Bob' added 'laptop' to the cart and proceeded to checkout.",
        "User 'Charlie' purchased product 'Smart TV' with express shipping.",
        "User 'David' finalized the order for 'Bluetooth headphones'.",
        "User 'Eve' paid for 'Wireless mouse' using credit card.",
        "User 'Frank' placed an order for 'Portable charger' as a gift.",
        "User 'Grace' confirmed the payment for product 'Fitness tracker'.",
        "User 'Hannah' bought 'Gaming keyboard' and 'Gaming mouse'.",
        "User 'Isaac' completed checkout for 'Smartphone case'.",
        "User 'Jack' purchased 'External hard drive' with discount code."
    ],
    'Abandoned Cart': [
        "User 'Alice' abandoned the cart with 'iPhone 12' in it.",
        "User 'Bob' left the website with 'laptop' in the cart.",
        "User 'Charlie' closed the browser tab with 'Smart TV' in the cart.",
        "User 'David' got distracted after adding 'Bluetooth headphones' to the cart.",
        "User 'Eve' decided not to proceed with 'Wireless mouse' purchase.",
        "User 'Frank' left 'Portable charger' in the cart and exited the site.",
        "User 'Grace' changed her mind about 'Fitness tracker' and emptied the cart.",
        "User 'Hannah' removed 'Gaming keyboard' and 'Gaming mouse' from the cart.",
        "User 'Isaac' abandoned the cart with 'Smartphone case' in it.",
        "User 'Jack' decided not to buy 'External hard drive' after all."
    ],
    'Other': [
        "Admin updated product inventory.",
        "System maintenance scheduled for tomorrow.",
        "New product 'Smartwatch' added to the catalog.",
        "Website traffic increased by 20% compared to last week.",
        "Server upgraded to improve performance.",
        "Payment gateway integration completed successfully.",
        "Product review moderation queue cleared.",
        "New blog post published: 'Top 10 Tech Gadgets of the Year'.",
        "Customer support team achieved 95% satisfaction rate.",
        "Holiday promotion campaign launched."
    ]
}

def generate_log():
    activity_type = random.choice(list(BUSINESS_ACTIVITIES.keys()))
    log_message = random.choice(BUSINESS_ACTIVITIES[activity_type])
    logging.info(f"{{\"activity_type\": \"{activity_type}\", \"message\": \"{log_message}\"}}")

def main():
    while True:
        generate_log()
        time.sleep(random.randint(1, 5))

if __name__ == "__main__":
    main()
