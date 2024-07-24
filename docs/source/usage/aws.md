# AWS Pub/Sub

The FRAME Django Template helper app includes built-in support for Pub/Sub mechanisms using AWS SNS and SQS. This allows for efficient and decoupled event-driven communication between different parts of your application.

## Overview

All model events (create, update, delete) are published by default using the `BaseModel`. This section will guide you through setting up listeners and handling events in a structured manner.

## Setting Up Listeners

Listeners are functions that react to specific events published on various channels. The `@listener` decorator is used to register these functions.

### Example

Here's an example of how to set up a listener and handle events:

### Listener Definition

Create a listener function in a module (e.g., `finance/listener.py`) and use the `@listener` decorator to specify the channel it should listen to.

```python
from core.aws_utils import listener

@listener("Order")
def order_listener(channel, action, data):
    from finance.subscribers.order_invoice import (
        event_handler as order_invoice_event_handler,
    )

    order_invoice_event_handler(action, data)
```

### Event Handler

Define an event handler function to process the events. Place this in a module within a `subscribers` directory (e.g., `finance/subscribers/order_invoice.py`).

```python 
from finance.models import Invoice
from orders.models import Order

def event_handler(action, data):
    if action == "created":
        create_invoice(data)
    elif action == "updated":
        create_invoice(data)
    elif action == "deleted":
        delete_invoice(data)

def create_invoice(order):
    order = Order.objects.get(id=order["id"])
    invoice, created = Invoice.objects.get_or_create(order=order)
    return invoice

def delete_invoice(order):
    order = Order.objects.get(id=order["id"])
    invoice = Invoice.objects.get(order=order)
    invoice.status = "CANCELLED"
    invoice.save()
    return invoice

```

## Conventions

To ensure consistency and maintainability, follow these conventions when setting up listeners and event handlers:

1. **File Naming**:
    - Place listener functions in a file named `listener.py` within the relevant app directory.
    - Place event handler functions in a `subscribers` directory within the relevant app directory.

2. **Function Naming**:
    - Listener functions should be named to reflect the model or channel they are listening to, e.g., `order_listener`.
    - Event handler functions should clearly indicate their purpose, e.g., `event_handler`, `create_invoice`, `delete_invoice`.

3. **Event Publishing**:
    - All model events (create, update, delete) are published by default using the `BaseModel`.
    - Ensure your models inherit from `BaseModel` to leverage this functionality.

## Summary

By following these guidelines, you can effectively utilize the Pub/Sub capabilities provided by FRAME to create a decoupled, event-driven architecture for your Django applications. This ensures that your business logic remains organized and easy to maintain, while also providing the flexibility to respond to various model events.

For more detailed information on setting up AWS SNS and SQS, refer to the AWS documentation:
- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [AWS SQS Documentation](https://docs.aws.amazon.com/sqs/latest/dg/welcome.html)
