class Card:
    def __init__(self, name):
        self.name = name


class Joker(Card):
    def __init__(self):
        super().__init__("Joker")
        self.value = None

    def set_value(self, value):
        self.value = value


class PassTurn(Card):
    def __init__(self):
        super().__init__("PassTurn")


class Reverse(Card):
    def __init__(self):
        super().__init__("Reverse")


class NumberCard(Card):
    def __init__(self, value):
        super().__init__(str(value))
        self.value = value
