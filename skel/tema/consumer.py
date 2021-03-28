"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from functools import reduce
import operator
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        # initialize the consumer with the given name and set it as a daemon thread
        super().__init__(name=kwargs.get("name"), daemon=kwargs.get("daemon"))

    def run(self):
        # register a single cart for the consumer
        cart_id = self.marketplace.new_cart()
        # coalesce carts to a single cart entity
        all_ops = reduce(operator.add, self.carts)
        # iterate over operations
        for single_op in all_ops:
            # produce as many items as specified
            quantity = single_op.get("quantity")
            while quantity > 0:
                if single_op.get("type") == "add":
                    # check if a product can be added to the cart. if not, wait and retry
                    status = False
                    while not status:
                        status = self.marketplace.add_to_cart(cart_id, single_op.get("product"))
                        if status:
                            break
                        time.sleep(self.retry_wait_time)
                elif single_op.get("type") == "remove":
                    # remove a product from the cart
                    self.marketplace.remove_from_cart(cart_id, single_op.get("product"))
                quantity -= 1

        # print the final contents of the cart
        for prod in self.marketplace.place_order(cart_id):
            print(self.name + " bought " + prod.__repr__())
