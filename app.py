from abc import ABC, abstractmethod


class OrderException(Exception):
    pass


class Order:
    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount
        self.status = "CREATED"


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, order: Order):
        pass


class CardPayment(PaymentStrategy):
    def __init__(self, card_no):
        self.card_no = card_no

    def pay(self, order: Order):
        if len(self.card_no) != 16:
            raise OrderException("Invalid card number")
        return True


class PaypalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email

    def pay(self, order: Order):
        if "@" not in self.email:
            raise OrderException("Invalid PayPal email")
        return True


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass

    @abstractmethod
    def get(self, order_id):
        pass


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.store = {}

    def save(self, order: Order):
        self.store[order.order_id] = order

    def get(self, order_id):
        if order_id not in self.store:
            raise OrderException("Order not found")
        return self.store[order_id]


class OrderEventListener(ABC):
    @abstractmethod
    def update(self, order: Order):
        pass


class LoggingListener(OrderEventListener):
    def update(self, order: Order):
        print(f"[LOG] Order {order.order_id} updated: {order.status}")


class NotificationListener(OrderEventListener):
    def update(self, order: Order):
        print(f"[NOTIFY] Order {order.order_id} status changed to {order.status}")


class OrderService:
    def __init__(self, repo: OrderRepository, listeners=None):
        self.repo = repo
        self.listeners = listeners or []

    def create_order(self, order_id, amount):
        order = Order(order_id, amount)
        self.repo.save(order)
        self._notify(order)
        return order

    def process_payment(self, order_id, payment: PaymentStrategy):
        order = self.repo.get(order_id)
        if payment.pay(order):
            order.status = "PAID"
            self.repo.save(order)
            self._notify(order)
        return order

    def _notify(self, order: Order):
        for listener in self.listeners:
            listener.update(order)


repo = InMemoryOrderRepository()
listeners = [LoggingListener(), NotificationListener()]
service = OrderService(repo, listeners)

service.create_order("A001", 500)
service.process_payment("A001", CardPayment("1111222233334444"))
service.process_payment("A001", PaypalPayment("user@mail.com"))
