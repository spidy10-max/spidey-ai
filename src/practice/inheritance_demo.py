# ============================================
# PRACTICE 3: Inheritance - Specialized AIs
# ============================================

# Parent class - basic AI (base blueprint)
class BaseAI:
    def __init__(self, name):
        self.name = name
    
    def respond(self, message):
        return f"{self.name}: Processing '{message}'..."


# Child class 1 - Voice AI (BaseAI ki saari cheezein inherit karega)
class VoiceAI(BaseAI):
    def __init__(self, name, voice_type):
        super().__init__(name)   # Parent ka __init__ call karo
        self.voice_type = voice_type
    
    def speak(self, message):
        return f"🔊 {self.name} ({self.voice_type} voice): '{message}'"


# Child class 2 - Text AI
class TextAI(BaseAI):
    def __init__(self, name):
        super().__init__(name)
        self.message_count = 0
    
    def send_text(self, message):
        self.message_count += 1
        return f"💬 {self.name} typed: '{message}' (Total: {self.message_count})"


# ============================================
# Ab use karte hain
# ============================================
print("="*50)
print("VOICE AI TEST")
print("="*50)

spidey_voice = VoiceAI("Spidey", "Male")
print(spidey_voice.respond("Hello"))              # Parent ka method
print(spidey_voice.speak("Aaj kya plan hai?"))    # Apna method

print()
print("="*50)
print("TEXT AI TEST")
print("="*50)

jarvis_text = TextAI("Jarvis")
print(jarvis_text.respond("Hi"))                  # Parent ka method
print(jarvis_text.send_text("Mission ready?"))    # Apna method
print(jarvis_text.send_text("Let's go!"))