"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        # initialize the producer with the given name and set it as a daemon thread
        super().__init__(name=kwargs.get("name"), daemon=kwargs.get("daemon"))

    def run(self):
        # register producer
        producer_id = self.marketplace.register_producer()
        # continuously add products to the marketplace
        while True:
            # iterate over the list of available products
            for product in self.products:
                # add as many products as specified by the quantity element of the product tuple
                quantity = product[1]
                while quantity > 0:
                    # check if the producer queue is full. if it is, wait and retry
                    status = False
                    while not status:
                        status = self.marketplace.publish(producer_id, product[0])
                        if status:
                            time.sleep(product[2])
                            break
                        time.sleep(self.republish_wait_time)
                    quantity -= 1
