class GoTo:
    def __init__(self, bot):
        self.bot = bot
        self.go_to = {
            'greetings': self.greetings,
        }

    def greetings(self):
        return [
            "Olá, tudo bem? Espero que sim! aaaaaaaaaaaaaaaaaaaaaaaaaa",
            "Sou o Codinho, assistente virtual da Dress Code. Aqui posso te ajudar mostrando nossos produtos, tirando dúvidas e até mesmo finalizar um pedido.",
            'Então, como posso te ajudar? 😊',
        ]