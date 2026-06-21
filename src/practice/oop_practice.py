# ============================================
# PRACTICE 1: Simple AI Assistant Class
# ============================================

class AIAssistant:
    def __init__(self, name, language="English"):
        self.name = name
        self.language = language
        self.conversation_count = 0
    
    def greet(self):
        self.conversation_count += 1
        return f"Hello! I'm {self.name}, speaking {self.language}"
    
    def chat(self, message):
        self.conversation_count += 1
        return f"{self.name} received: '{message}'"
    
    def stats(self):
        return f"{self.name} has had {self.conversation_count} conversations"


# Objects banao
spidey = AIAssistant("Spidey", "Urdu")
print(spidey.greet())
print(spidey.chat("Aaj weather kaisa hai?"))
print(spidey.chat("Mujhe news suna do"))
print(spidey.stats())

print("\n" + "="*50 + "\n")

# Doosra object
jarvis = AIAssistant("Jarvis")
print(jarvis.greet())
print(jarvis.stats())