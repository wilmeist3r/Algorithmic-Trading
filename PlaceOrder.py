from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *


# Class overriding EWrapper and EClient IBKR's API classes
class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Provides connection notifications
    def error(self, reqId, errorCode, errorString):
        print("Notification: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        self.start()

    # Provides order status notifications
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print("Order ID: ", orderId, " Status: ", status, " Filled: ", filled, " Remaining: ", remaining
              , " LastFillPrice: ", lastFillPrice)

    # Provides notifications on submitted orders
    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order ID: ", orderId, contract.symbol, contract.secType, " @ ", contract.exchange, ": "
              , order.action, order.orderType, order.totalQuantity, orderState.status)

    # Provides notifications on executed (filled) orders
    def execDetails(self, reqId, contract, execution):
        print("Exec Details: ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId
              , execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        # Assigns information on a specific symbol to be bought or sold
        contract = Contract()
        contract.symbol = input("Enter a symbol: ")
        contract.secType = input("Enter a security type: ")
        contract.exchange = input("Enter an exchange: ")
        contract.currency = input("Enter a currency: ")
        contract.primaryExchange = input("Enter a primary exchange: ")

        # Assigns information on the order to be executed
        order = Order()
        order.action = input("Enter the action to be performed (BUY or SELL): ")
        order.totalQuantity = input("Enter the amount of shares to buy or sell: ")
        order.orderType = input("Enter an order type: ")
        order.lmtPrice = input("Enter a limit price: ")

        # Places the order given previously described contract and order objects
        self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    app = TestApp()
    # Connects to TWS given an IP (localhost or other) and a port (standard paper account port is used below)
    app.connect("127.0.0.1", 7497, 1)

    app.run()


if __name__ == '__main__':
    main()
