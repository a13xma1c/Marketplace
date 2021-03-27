"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import uuid


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.queue_dict = dict()
        self.cart_dict = dict()
        self.lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = uuid.uuid4()
        self.queue_dict[producer_id] = list()
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        condition = True
        if len(self.queue_dict[producer_id]) == self.queue_size_per_producer:
            condition = False
        else:
            self.queue_dict[producer_id].append(product)

        return condition

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        cart_id = uuid.uuid4()
        self.cart_dict[cart_id] = list()
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        flat_list = [item for sl in self.queue_dict.values() for item in sl]
        if product not in flat_list:
            return False
        self.lock.acquire()
        for key in self.queue_dict:
            if product in self.queue_dict[key]:
                self.queue_dict[key].remove(product)
                self.cart_dict[cart_id].append((key, product))
                break

        self.lock.release()
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.lock.acquire()
        for (key, prod) in self.cart_dict[cart_id]:
            if prod == product:
                self.cart_dict[cart_id].remove((key, product))
                self.queue_dict[key].append(product)
                break
        self.lock.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return [p for (k, p) in self.cart_dict[cart_id]]
