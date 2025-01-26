class Prompt:
    def __init__(self):
        self.messages = []

    def add_system_message(self, content: str):
        self.messages.append({"role": "system", "content": content})

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def get_messages(self):
        return self.messages 