"""
Spidey AI - Main (With Agent + Registry!)
Day 45
"""
from spidey.brain.chat import SpideyBrain
from spidey.config import settings, APP_NAME, APP_VERSION, LOGS_DIR
from spidey.logger import log_startup, log_shutdown
import os

try:
    from spidey.voice.voice_manager import VoiceManager
    VOICE_AVAILABLE = True
except (ImportError, OSError):
    VOICE_AVAILABLE = False


def print_banner():
    print()
    print("=" * 55)
    print("   SPIDEY AI v" + APP_VERSION)
    print("=" * 55)
    print("   [AGENT]   agent <task> | plan <task> | agent tools")
    print("   [AGENT]   agent registry | agent info <tool>")
    print("   [AGENT]   agent log | agent history")
    print("   [VOICE]   spidey beta | v | speakmode")
    print("   [LANG]    urdu | english | hindi | setvoice")
    print("   [CHAT]    quit | reset | count")
    print("   [HISTORY] history | load | delete")
    print("   [SEARCH]  search | smart")
    print("   [AI]      provider | switch | models")
    print("   [MEMORY]  remember | recall | memories | forget")
    print("   [NOTES]   note | notes")
    print("   [OTHER]   stats | voicestatus | mictest")
    print("   Ctrl+C = Cancel (NOT exit!)")
    print("=" * 55)
    print()


def show_history(brain):
    conversations = brain.get_all_conversations()
    if not conversations:
        print("\n   No conversations.\n")
        return
    for i, conv in enumerate(conversations, 1):
        print("   " + str(i) + ". [" + conv['conv_id'] + "] " + conv['title'][:30] + " (" + str(conv['message_count']) + " msgs)")
    print()


def show_providers(brain):
    all_p = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()
    for key, config in all_p.items():
        if key == current:
            status = "[ON]"
        elif key in available:
            status = "[OK]"
        else:
            status = "[--]"
        print("   " + status + " " + key + " -- " + config['name'])
    print()


def main():
    print_banner()

    brain = SpideyBrain()
    brain.start_new_conversation()
    info = brain.get_provider_info()
    username = settings.get("username", "User")

    vm = None
    if VOICE_AVAILABLE:
        try:
            print("   Loading voice...")
            vm = VoiceManager(whisper_model="base", tts_engine="edge")
            mic_ok = "OK" if vm.is_input_available() else "NO"
            voice_ok = "OK" if vm.is_output_available() else "NO"
            print("   Mic: " + mic_ok + " | Voice: " + voice_ok)
        except Exception as e:
            print("   Voice Error: " + str(e))
            vm = None

    log_startup(info['name'], settings.get_all())

    print("\nSpidey: Hey " + username + "!")
    print("   AI: " + info['name'])

    memories = brain.get_all_memories()
    if memories:
        print("   Memories: " + str(len(memories)))

    print("\n   'agent <task>' = Multi-step | 'spidey beta' = Voice\n")

    while True:
        try:
            provider = brain.get_provider_name()
            username = settings.get("username", "User")
            si = " [SPEAK]" if (vm and vm.speak_enabled) else ""
            user_input = input(username + " [" + provider + "]" + si + ": ").strip()

            if not user_input:
                continue

            cmd = user_input.lower()

            if cmd in ["quit", "exit"]:
                count = brain.get_history_count()
                log_shutdown(count)
                print("\nBye " + username + "! (" + str(count) + " msgs saved)")
                if vm and vm.speak_enabled:
                    vm.speak("Bye " + username + "!")
                brain.close()
                break

            # ========================================
            # AGENT COMMANDS
            # ========================================

            if cmd == "agent tools":
                print("\n" + brain.agent_tools() + "\n")
                continue

            if cmd == "agent log":
                if hasattr(brain.agent, 'get_last_log'):
                    print("\n" + brain.agent.get_last_log() + "\n")
                elif hasattr(brain.agent, 'react_agent') and brain.agent.react_agent:
                    print("\n" + brain.agent.react_agent.get_last_log() + "\n")
                else:
                    print("\n   No log available.\n")
                continue

            if cmd == "agent history":
                if hasattr(brain.agent, 'get_task_history'):
                    print("\n" + brain.agent.get_task_history() + "\n")
                else:
                    print("\n   No history available.\n")
                continue

            if cmd == "agent registry":
                try:
                    from spidey.agent.tool_registry import ToolRegistry
                    reg = ToolRegistry()
                    print(reg.display_all())
                except Exception as e:
                    print(f"\n   Error: {e}\n")
                continue

            if cmd.startswith("agent info "):
                tool_name = user_input[11:].strip()
                try:
                    from spidey.agent.tool_registry import ToolRegistry
                    reg = ToolRegistry()
                    print(reg.display_tool(tool_name))
                except Exception as e:
                    print(f"\n   Error: {e}\n")
                continue

            if cmd.startswith("agent "):
                task = user_input[6:].strip()
                if task:
                    try:
                        print()
                        result = brain.agent_execute(task)
                        print(result)
                        print()
                        if vm and vm.speak_enabled:
                            vm.speak(result)
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                continue

            if cmd == "agent":
                try:
                    task = input("   Agent Task: ").strip()
                    if task:
                        print()
                        result = brain.agent_execute(task)
                        print(result)
                        print()
                        if vm and vm.speak_enabled:
                            vm.speak(result)
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd.startswith("plan "):
                task = user_input[5:].strip()
                if task:
                    try:
                        result = brain.agent_plan(task)
                        print()
                        if isinstance(result, str):
                            print(result)
                        elif isinstance(result, list):
                            print("   Plan (" + str(len(result)) + " steps):")
                            for i, s in enumerate(result, 1):
                                print("   " + str(i) + ". " + str(s))
                        print()
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                continue

            if cmd == "plan":
                try:
                    task = input("   Plan Task: ").strip()
                    if task:
                        result = brain.agent_plan(task)
                        print()
                        if isinstance(result, str):
                            print(result)
                        elif isinstance(result, list):
                            print("   Plan (" + str(len(result)) + " steps):")
                            for i, s in enumerate(result, 1):
                                print("   " + str(i) + ". " + str(s))
                        print()
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd == "tools":
                print("\n" + brain.agent_tools() + "\n")
                continue

            # ========================================
            # VOICE COMMANDS
            # ========================================

            if cmd in ["spidey beta", "spideybeta", "beta"]:
                if vm and vm.is_input_available() and vm.is_output_available():
                    try:
                        vm.spidey_beta_loop(brain)
                    except KeyboardInterrupt:
                        print("\n   Beta cancelled!\n")
                else:
                    print("\n   Voice not available!\n")
                continue

            if cmd in ["v", "voice"]:
                if vm:
                    try:
                        vm.voice_chat(brain, mode="auto")
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                else:
                    print("\n   Voice not available!\n")
                continue

            if cmd == "voice5":
                if vm:
                    try:
                        vm.voice_chat(brain, mode="fixed", duration=5)
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                continue

            if cmd == "voice10":
                if vm:
                    try:
                        vm.voice_chat(brain, mode="fixed", duration=10)
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                continue

            if cmd == "speakmode":
                if vm:
                    on = vm.toggle_speak()
                    print("\n   Speak: " + ("ON" if on else "OFF"))
                    if on:
                        vm.speak("Speak mode on!")
                    print()
                continue

            if cmd == "saytest":
                if vm:
                    try:
                        vm.test_speak()
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                continue

            if cmd == "speak":
                if vm:
                    try:
                        t = input("   Text: ").strip()
                        if t:
                            vm.speak(t)
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                continue

            if cmd == "urdu":
                if vm:
                    vm.set_language("ur")
                    print("   Urdu voice!")
                    vm.speak("Urdu voice activated!")
                continue

            if cmd == "english":
                if vm:
                    vm.set_language("en")
                    print("   English voice!")
                    vm.speak("English voice activated!")
                continue

            if cmd == "hindi":
                if vm:
                    vm.set_language("hi")
                    print("   Hindi voice!")
                    vm.speak("Hindi voice activated!")
                continue

            if cmd == "setvoice":
                if vm:
                    try:
                        voices = vm.get_voices()
                        cv = vm.get_current_voice().get("voice", "")
                        for i, v in enumerate(voices, 1):
                            a = " <--" if v["id"] == cv else ""
                            print("   " + str(i) + ". [" + v['language'] + "] " + v['name'] + a)
                        c = int(input("\n   Number: ").strip()) - 1
                        if 0 <= c < len(voices):
                            vm.voice_output.set_voice(voices[c]["id"])
                            print("   Done: " + voices[c]['name'])
                            vm.speak("Hello! I am now " + voices[c]['name'] + "!")
                    except (ValueError, IndexError, KeyboardInterrupt):
                        print("   Invalid\n")
                continue

            if cmd == "voicestatus":
                if vm:
                    s = vm.get_status()
                    print("\n   Input:  " + ("OK" if s['voice_input'] else "NO"))
                    print("   Output: " + ("OK" if s['voice_output'] else "NO"))
                    print("   Speak:  " + ("ON" if s['speak_enabled'] else "OFF"))
                    v = s.get('current_voice', {})
                    print("   Voice:  " + str(v.get('voice', 'N/A')))
                    print()
                continue

            if cmd == "mictest":
                if vm:
                    try:
                        vm.test_mic()
                    except KeyboardInterrupt:
                        print("\n   Cancelled!\n")
                continue

            # ========================================
            # CHAT COMMANDS
            # ========================================

            if cmd == "reset":
                brain.reset()
                print("\n   Fresh start!\n")
                continue

            if cmd == "count":
                print("\n   " + str(brain.get_history_count()) + " messages\n")
                continue

            # ========================================
            # HISTORY COMMANDS
            # ========================================

            if cmd == "history":
                show_history(brain)
                continue

            if cmd == "load":
                try:
                    show_history(brain)
                    convs = brain.get_all_conversations()
                    if convs:
                        i = int(input("   Number: ").strip()) - 1
                        if 0 <= i < len(convs):
                            brain.load_conversation(convs[i]["conv_id"])
                            print("   Loaded!\n")
                except (ValueError, IndexError, KeyboardInterrupt):
                    print("\n   Cancelled!\n")
                continue

            if cmd == "delete":
                try:
                    show_history(brain)
                    convs = brain.get_all_conversations()
                    if convs:
                        i = int(input("   Number: ").strip()) - 1
                        if 0 <= i < len(convs):
                            if input("   Delete? (y/n): ").strip().lower() in ["y", "yes"]:
                                brain.delete_conversation(convs[i]["conv_id"])
                                print("   Deleted!\n")
                except (ValueError, IndexError, KeyboardInterrupt):
                    print("\n   Cancelled!\n")
                continue

            # ========================================
            # SEARCH COMMANDS
            # ========================================

            if cmd == "search":
                try:
                    q = input("   Search: ").strip()
                    if q:
                        for m in (brain.search_chats(q) or [])[:5]:
                            role = "You" if m['role'] == 'user' else "Spidey"
                            print("   [" + role + "] " + m['content'][:60] + "...")
                    print()
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd == "smart":
                try:
                    q = input("   Smart Search: ").strip()
                    if q:
                        for r in (brain.semantic_search(q) or [])[:5]:
                            print("   " + r['content'][:60] + "...")
                    print()
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            # ========================================
            # PROVIDER COMMANDS
            # ========================================

            if cmd == "provider":
                print("\n   AI: " + brain.get_provider_info()['name'] + "\n")
                continue

            if cmd == "switch":
                try:
                    show_providers(brain)
                    c = input("   Provider: ").strip().lower()
                    if brain.switch_provider(c):
                        print("   Switched!\n")
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd == "models":
                show_providers(brain)
                continue

            # ========================================
            # SETTINGS COMMANDS
            # ========================================

            if cmd == "settings":
                print(settings)
                continue

            if cmd == "tokens":
                cur = settings.get("show_tokens", False)
                settings.set("show_tokens", not cur)
                brain.update_settings()
                print("\n   Tokens: " + ("ON" if not cur else "OFF") + "\n")
                continue

            if cmd == "temp":
                try:
                    v = float(input("   Temp (0.0-2.0): "))
                    if 0.0 <= v <= 2.0:
                        settings.set("temperature", v)
                        brain.update_settings()
                        print("   Done: " + str(v) + "\n")
                except (ValueError, KeyboardInterrupt):
                    print("\n   Cancelled!\n")
                continue

            if cmd == "name":
                try:
                    v = input("   Name: ").strip()
                    if v:
                        settings.set("username", v)
                        print("   Done: " + v + "\n")
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            # ========================================
            # MEMORY COMMANDS
            # ========================================

            if cmd == "remember":
                try:
                    k = input("   Key: ").strip()
                    v = input("   Value: ").strip() if k else ""
                    if k and v:
                        brain.remember(k, v, input("   Category: ").strip() or "general")
                        print("   Done: " + k + " = " + v + "\n")
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd == "recall":
                try:
                    k = input("   Key: ").strip()
                    if k:
                        v = brain.recall(k)
                        if v:
                            print("   " + k + " = " + v + "\n")
                        else:
                            print("   Unknown\n")
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd == "smartrecall":
                try:
                    q = input("   Query: ").strip()
                    if q:
                        for r in brain.smart_recall(q):
                            print("      - " + r['content'])
                    print()
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd == "memories":
                m = brain.get_all_memories()
                if m:
                    for k, i in m.items():
                        print("   - " + k + ": " + i['value'])
                else:
                    print("   Empty")
                print()
                continue

            if cmd == "forget":
                try:
                    k = input("   Key: ").strip()
                    if k and brain.forget(k):
                        print("   Forgot!\n")
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            # ========================================
            # NOTES COMMANDS
            # ========================================

            if cmd == "note":
                try:
                    t = input("   Title: ").strip()
                    c = input("   Content: ").strip() if t else ""
                    if t and c:
                        brain.add_note(t, c)
                        print("   Added!\n")
                except KeyboardInterrupt:
                    print("\n   Cancelled!\n")
                continue

            if cmd == "notes":
                for n in brain.get_notes():
                    star = "*" if n["is_important"] else " "
                    print("   " + star + "[" + str(n['id']) + "] " + n['title'])
                print()
                continue

            # ========================================
            # OTHER COMMANDS
            # ========================================

            if cmd == "stats":
                s = brain.get_stats()
                print("\n   " + str(s['total_conversations']) + " convs | " + str(s['total_messages']) + " msgs | " + str(s['total_preferences']) + " memories\n")
                continue

            if cmd == "logs":
                if os.path.exists(LOGS_DIR):
                    for f in sorted(os.listdir(LOGS_DIR), reverse=True)[:5]:
                        print("   " + f)
                print()
                continue

            # ========================================
            # AI CHAT (LAST)
            # ========================================
            try:
                print()
                print("Spidey: ", end="", flush=True)
                response = brain.chat(user_input)
                print(response)
                print()
                if vm and vm.speak_enabled and response:
                    vm.speak(response)
            except KeyboardInterrupt:
                print("\n   Response cancelled!\n")

        except KeyboardInterrupt:
            print("\n   Cancelled! (Type 'quit' to exit)\n")
            continue
        except EOFError:
            print("\n   Input error.\n")
            continue
        except Exception as e:
            print("\n   Error: " + str(e) + "\n")
            continue

    print("\nSpidey AI closed.\n")


if __name__ == "__main__":
    main()