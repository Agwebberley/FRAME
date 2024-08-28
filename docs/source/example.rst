Example
=====
At https://github.com/agwebberley/Frame-Template there is an example application that contains some basic apps and models to demonstrate how to use the Frame.

As a brief overview,
- The `customers` and `inventory` apps contain a simple model and view that demonstrates how to use the Frame's `BaseModel` and `BaseView` classes.
- The `orders` app contains an internal many-to-many relationship between `order` and `order_item` models. As well as a many-to-one relationship between `order` and `customer` models.
- The `finance` app shows how to use the AWS integration to receive messages from an SNS topic and store them in a model.  It demonstrates how to ensure that cross-app models that aren't directly many-to-one related communicate with each other.

.. toctree::
    :maxdepth: 2
    
    example/customers
    example/orders
    example/finance
