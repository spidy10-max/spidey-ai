"""
Spidey AI — Chat Brain (With Agent!)
"""
from spidey.brain.providers import ProviderManager
from spidey.memory.memory import SpideyMemory
from spidey.memory.search_engine import SearchEngine
from spidey.memory.auto_memory import AutoMemory
from spidey.tools.tool_connector import ToolConnector
from spidey.agent.agent import SpideyAgent
from spidey.config import settings, SYSTEM_PROMPT
from spidey.logger import brain_logger, log_chat, log_event, log_error


class SpideyBrain:

    def __init__(self):
        provider = settings.get("provider", "groq")
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)
        self.auto_context = settings.get("auto_context", True)
        self.auto_memory_enabled = settings.get("auto_memory", True)

        self.provider_manager = ProviderManager(default_provider=provider)
        self.system_prompt = {"role": "system", "content": settings.get("system_prompt", SYSTEM_PROMPT)}
        self.memory = SpideyMemory()
        self.search_engine = SearchEngine(db=self.memory.db, vectors=self.memory.vectors)
        self.auto_memory = AutoMemory(self.memory)
        self.tools = ToolConnector()
        self.agent = SpideyAgent(self)
        self.messages = [self.system_prompt]
        brain_logger.info("SpideyBrain initialized with agent")

    def start_new_conversation(self):
        provider_info = self.provider_manager.get_current_info()
        conv_id = self.memory.start_conversation(
            provider=self.provider_manager.get_current_name(),
            model=provider_info.get("model", "unknown")
        )
        self.messages = [self.system_prompt]
        memory_context = self.memory.get_memory_context()
        if memory_context:
            self.messages.append({"role": "system", "content": memory_context})
        return conv_id

    def chat(self, user_message):
        if not self.memory.current_conv_id:
            self.start_new_conversation()

        # Step 1: Check tools
        tool_result = self.tools.process_command(user_message)
        if tool_result:
            log_chat("user", user_message)
            log_chat("assistant", tool_result, provider="tool")
            self.memory.save_message("user", user_message)
            self.memory.save_message("assistant", tool_result)
            return tool_result

        # Step 2: Auto memory
        if self.auto_memory_enabled:
            try:
                detected = self.auto_memory.detect_and_save(user_message)
                if detected:
                    for fact in detected:
                        print(f"\n   🧠 Auto-remembered: {fact['key']} = {fact['value']}")
            except Exception as e:
                log_error(str(e), "chat - auto memory")

        # Step 3: Auto context
        if self.auto_context:
            try:
                context = self.search_engine.get_context_for_query(user_message)
                if context:
                    self.messages.append({"role": "system", "content": f"[Context]\n{context}"})
            except Exception as e:
                log_error(str(e), "chat - context")

        # Step 4: AI
        self.messages.append({"role": "user", "content": user_message})
        log_chat("user", user_message)

        try:
            result = self.provider_manager.chat(
                messages=self.messages, temperature=self.temperature, max_tokens=self.max_tokens
            )
            ai_reply = result["content"]
            provider_name = result.get("provider", "unknown")

            self.messages.append({"role": "assistant", "content": ai_reply})
            self.memory.save_message("user", user_message, tokens_used=result.get("input_tokens", 0), provider=provider_name, model=result.get("model"))
            self.memory.save_message("assistant", ai_reply, tokens_used=result.get("output_tokens", 0), provider=provider_name, model=result.get("model"))
            log_chat("assistant", ai_reply, provider=provider_name)

            if self.show_tokens and result.get("total_tokens", 0) > 0:
                print(f"\n   📊 Tokens: {result['total_tokens']}")

            return ai_reply
        except Exception as e:
            log_error(str(e), "SpideyBrain.chat")
            return f"Error: {str(e)}"

    def update_settings(self):
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)
        self.auto_context = settings.get("auto_context", True)
        self.auto_memory_enabled = settings.get("auto_memory", True)
        self.system_prompt = {"role": "system", "content": settings.get("system_prompt", SYSTEM_PROMPT)}

    def switch_provider(self, name):
        s = self.provider_manager.switch_provider(name)
        if s: settings.set("provider", name)
        return s

    def get_provider_info(self): return self.provider_manager.get_current_info()
    def get_provider_name(self): return self.provider_manager.get_current_name()
    def list_providers(self): return self.provider_manager.list_providers()
    def get_available_providers(self): return self.provider_manager.get_available_providers()

    def reset(self):
        if self.memory.current_conv_id: self.memory.save_summary()
        self.auto_memory.reset_session()
        self.start_new_conversation()

    def load_conversation(self, conv_id):
        if self.memory.load_conversation(conv_id):
            saved = self.memory.get_conversation_messages(conv_id)
            self.messages = [self.system_prompt]
            mc = self.memory.get_memory_context()
            if mc: self.messages.append({"role": "system", "content": mc})
            self.messages += saved
            return True
        return False

    def get_history_count(self): return self.memory.get_message_count()
    def get_all_conversations(self): return self.memory.get_all_conversations()
    def delete_conversation(self, cid): return self.memory.delete_conversation(cid)

    # Search
    def smart_search(self, q, n=10): return self.search_engine.smart_search(q, n)
    def semantic_search(self, q, n=5): return self.memory.semantic_search(q, n)
    def search_chats(self, q): return self.memory.search_messages(q)
    def search_summaries(self, q): return self.memory.search_summaries(q)

    # Memory
    def remember(self, k, v, c="general"): return self.memory.remember(k, v, c)
    def recall(self, k): return self.memory.recall(k)
    def smart_recall(self, q): return self.memory.smart_recall(q)
    def get_all_memories(self): return self.memory.get_all_memories()
    def forget(self, k): return self.memory.forget(k)
    def get_auto_detected(self): return self.auto_memory.get_detected_facts()

    # Notes
    def add_note(self, t, c, cat="general", imp=False): return self.memory.add_note(t, c, cat, imp)
    def get_notes(self, cat=None, imp=False): return self.memory.get_notes(cat, imp)
    def search_notes(self, q): return self.memory.search_notes(q)
    def delete_note(self, nid): return self.memory.delete_note(nid)

    # Tools
    def toggle_tools(self): return self.tools.toggle()
    def tools_enabled(self): return self.tools.is_enabled()

    # Agent
    def agent_execute(self, task): return self.agent.execute(task)
    def agent_plan(self, task): return self.agent.plan_task(task)
    def agent_tools(self): return self.agent.get_available_tools()

    # Stats
    def get_stats(self):
        s = self.memory.get_stats()
        s["auto_detected"] = self.auto_memory.get_detected_count()
        s["tools_enabled"] = self.tools.is_enabled()
        return s

    def close(self):
        if self.memory.current_conv_id: self.memory.save_summary()
        self.memory.close()