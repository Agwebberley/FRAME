# Style

This project is built around the principles of fat models and thin views. The key idea is to keep views simple and free of business logic, which should instead reside in the models or be handled via a Pub/Sub mechanism. This approach ensures better separation of concerns, maintainability, and testability of your code.

## Principles

1. **Fat Models, Thin Views**: 
    - **Views**: Should handle request processing, data validation, and rendering templates. They should not contain any business logic.
    - **Models**: Should encapsulate all business logic and rules related to the data they manage. This makes models rich in functionality and ensures that the business logic is reusable across different views.

2. **Single Responsibility**:
    - **Model Responsibility**: If the logic pertains only to a single model, it should be encapsulated within the model. This includes validation, calculations, and any behavior related to the model’s data.
    - **Cross-Model Communication**: If the logic involves interactions between multiple models, it should be managed via a Pub/Sub mechanism to ensure decoupling and scalability.

## Implementation Guidelines

### Fat Models

Encapsulate all business logic within the models. This includes:

- **Validation**: Implement custom validation methods within the models.
- **Calculations and Aggregations**: Perform any necessary calculations or aggregations in model methods.
- **Complex Queries**: Encapsulate complex queries in model managers or model methods.

**Example**:

```python
class Order(BaseModel):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def apply_discount(self, discount_amount):
        self.discount = discount_amount
        self.total_price -= discount_amount
        self.save()
```
### Thin Views

Views should be limited to handling HTTP requests and responses. They should:

- **Process Requests**: Handle incoming requests and prepare responses.
- **Data Validation**: Perform basic validation of request data.
- **Rendering Templates**: Pass data to templates for rendering.
Example:

```python
class OrderCreateView(BaseCreateView):
    model = Order
```
### Pub/Sub for Cross-Model Communication

Use Pub/Sub mechanisms to handle interactions between different models. This ensures that models remain decoupled and communication between them is flexible and scalable.

- **Publishing Events**: Models can publish events when certain actions occur.
- **Subscribing to Events**: Other models or services can subscribe to these events and perform the necessary actions.

## Best Practices

1. **Encapsulation**: Keep business logic encapsulated within models. Avoid placing business logic in views or forms.
2. **Reusability**: Write model methods and managers to be reusable across different views and contexts.
3. **Decoupling**: Use Pub/Sub mechanisms to decouple different parts of the application, ensuring they can evolve independently.
4. **Consistency**: Follow consistent naming conventions and design patterns throughout the codebase.
5. **Documentation**: Document the purpose and usage of complex methods and business logic to aid in maintainability.

By adhering to these principles and guidelines, you can maintain a clean, maintainable, and scalable codebase.
