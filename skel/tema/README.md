# Marketplace
### Alexandru Cristian Maican 335CB

The purpose of this application is the implementation of the multi producer multi consumer (**MPMC**) problem in *Python 3.9*.
The **Marketplace** class, implemented in the *marketplace.py* file, is used as a shared reference between threads, providing
the functionality of a queue.

The **Marketplace** restricts the size of the queue of produced items and contains two dictionaries with list values that
handle the distribution of products between producer queues (```queue_dict```) and consumer queues (```cart_dict```). All add and remove
operation are guarded by locks (```add_lock```, ```remove_lock```) in order to protect the shared variables mentioned above. An ```add_to_cart```
operation removes a product from a producer queue and adds the item to a consumer queue. The consumer queue (```cart_dict[cart_id]```)
is a list that contains tuple values, composed of the ```producer_id``` and the ```product``` reference. This model facilitates
the implementation of the ```remove_from_cart``` operation. A certain product is removed from a specified consumer queue and added back
to the original producer queue (based on the ```producer_id``` associated with the ```product``` reference from the tuple). The
```publish``` method is used by producer threads to add products to their respective producer queues, if the queues aren't full. 
The ```register_producer``` method returns an *uuid* (```producer_id```) and adds an entry for it in the ```queue_dict```, initializing
the value with an empty list. The ```new_cart``` method returns an *uuid* (```cart_id```) and adds an entry for it in the ```cart_dict```,
initializing the value with an empty list. Finally, the ```place_order``` method returns the list of products associated with a ```cart_id```.

The **Consumer** and **Producer** classes are implemented in the *consumer.py* and *producer.py* files, respectively. A consumer
performs the specified add or remove operations, based on the information passed through the ```carts``` argument of the class constructor.
The producer handles product creation based on the ```products``` argument of the class constructor.