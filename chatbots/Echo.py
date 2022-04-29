from chatbots.Chatbot import Chatbot
# https://www.w3schools.com/python/python_inheritance.asp#:~:text=1%20Python%20Inheritance.%20Inheritance%20allows%20us%20to%20define,inheritance%20of%20the%20parent%20method%20will%20be%20

class Echo(Chatbot):
    response = None
    def send_message(self):
        return self.response
    def recv_message(self, message):
        self.response = message
        return super().recv_message(message)