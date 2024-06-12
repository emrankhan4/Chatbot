from ..models.userlib import *
from ..models.get_from_chromaDB import *
class ChatHistory:
    def __init__(self):
        self.history = []

    def add_message(self, role, message):
        # self.history.append({"role": role, "message": message})
        if role.lower()=='ai':
            self.history.append({f"AI: {message}"})
        else:
            
            self.history.append({f"USER: {message}"})
    def get_history(self):
        return self.history



history = ChatHistory()

ch = get_general_chat_chain(history)
print(ch.invoke({"question":"what is nikles?"}))