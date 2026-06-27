"""
Spidey ReAct Agent v2
Enhanced with multi-step task handling, better parsing, and tool chaining
Day 44 — AI Agent Brain
"""

import json
import re
import time
from datetime import datetime


class ReActAgent:
    """
    ReAct Agent v2 for Spidey AI
    - Better prompt engineering
    - Multi-step task handling
    - Tool chaining
    - Error recovery
    - Execution summary
    """

    def __init__(self, brain):
        self.brain = brain
        self.max_steps = 8
        self.tools = {}
        self.execution_log = []
        self.task_history = []
        self._register_tools()

    def _register_tools(self):
        """Register all available tools from ToolConnector"""
        if hasattr(self.brain, 'tools') and hasattr(self.brain.tools, 'tools'):
            for name, info in self.brain.tools.tools.items():
                self.tools[name] = {
                    "instance": info["instance"],
                    "name": info["name"],
                    "description": info["description"]
                }

        self.tools["ai_think"] = {
            "instance": None,
            "name": "AI Think",
            "description": "Use AI to analyze, summarize, compare, or generate text"
        }

        self.tools["final_answer"] = {
            "instance": None,
            "name": "Final Answer",
            "description": "Give the final combined answer to the user"
        }

    def get_tools_description(self):
        """Generate tools description for AI prompt"""
        lines = []
        for name, info in self.tools.items():
            lines.append(f"  - {name}: {info['description']}")
        return "\n".join(lines)

    def build_react_prompt(self, task, steps_so_far):
        """Build enhanced ReAct prompt"""
        steps_text = ""
        if steps_so_far:
            for step in steps_so_far:
                steps_text += f"\nThought: {step.get('thought', '')}"
                steps_text += f"\nAction: {step.get('action', '')}"
                steps_text += f"\nObservation: {step.get('observation', '')}\n"

        prompt = f"""You are Spidey AI Agent. You solve complex tasks step by step.

AVAILABLE TOOLS:
{self.get_tools_description()}

ACTION FORMAT (use EXACTLY this):
  weather | current | city=CityName
  weather | forecast | city=CityName, days=3
  search | text | query=YourSearchQuery
  search | news | query=NewsQuery
  search | videos | query=VideoQuery
  wiki | summary | topic=TopicName
  wiki | fact | topic=TopicName
  news | headlines | country=us
  news | headlines | country=pk, category=technology
  ai_think | analyze | question=Your question here
  final_answer | Your complete final answer here

RULES:
1. ALWAYS start with "Thought:" then "Action:"
2. Break complex tasks into simple steps
3. Use tools to get REAL data — don't make up facts
4. After getting observations, THINK about next step
5. When you have enough info, use final_answer
6. Combine all observations in final_answer
7. Maximum {self.max_steps} steps
8. For multi-part tasks, handle each part separately

TASK: {task}
{steps_text}
Next step (Thought then Action):"""

        return prompt

    def parse_ai_response(self, response):
        """Parse AI response to extract Thought and Action"""
        thought = ""
        action_raw = ""

        # Extract Thought
        thought_match = re.search(
            r"Thought:\s*(.+?)(?=\nAction:|$)",
            response,
            re.DOTALL
        )
        if thought_match:
            thought = thought_match.group(1).strip()

        # Extract Action
        action_match = re.search(
            r"Action:\s*(.+?)(?=\nThought:|$)",
            response,
            re.DOTALL
        )
        if action_match:
            action_raw = action_match.group(1).strip()
            # Clean up — remove extra lines
            action_raw = action_raw.split("\n")[0].strip()

        # Fallback — try to find tool pattern directly
        if not action_raw:
            tool_match = re.search(
                r"(weather|search|wiki|news|ai_think|final_answer)\s*\|",
                response
            )
            if tool_match:
                # Extract from this point
                start = tool_match.start()
                action_raw = response[start:].split("\n")[0].strip()

        return thought, action_raw

    def parse_action(self, action_raw):
        """Parse action string into tool_name, action_type, params"""
        parts = [p.strip() for p in action_raw.split("|")]

        if len(parts) < 2:
            # Maybe it's a final_answer without pipe
            if action_raw.lower().startswith("final_answer"):
                answer = action_raw.replace("final_answer", "").strip()
                return "final_answer", answer, {}
            return None, None, {}

        tool_name = parts[0].strip().lower()
        action_type = parts[1].strip()

        params = {}
        if len(parts) >= 3:
            params_str = parts[2].strip()
            for param in params_str.split(","):
                if "=" in param:
                    key, value = param.strip().split("=", 1)
                    params[key.strip()] = value.strip()

        return tool_name, action_type, params

    def execute_action(self, tool_name, action_type, params):
        """Execute a tool action and return the observation"""

        if tool_name == "final_answer":
            return action_type

        if tool_name == "ai_think":
            question = params.get("question", action_type)
            try:
                result = self.brain.provider_manager.chat(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant. Give concise, useful answers."},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                return result.get("content", "No response")
            except Exception as e:
                return f"AI Think error: {str(e)}"

        if tool_name == "weather":
            if "weather" not in self.tools or not self.tools["weather"]["instance"]:
                return "Weather tool not available"
            tool = self.tools["weather"]["instance"]
            city = params.get("city", action_type)
            if not city or city == "current":
                return "No city provided. Please specify a city."
            if action_type == "forecast":
                days = int(params.get("days", 3))
                return tool.get_forecast(city, days=days)
            else:
                return tool.get_current_weather(city)

        if tool_name == "search":
            if "search" not in self.tools or not self.tools["search"]["instance"]:
                return "Search tool not available"
            tool = self.tools["search"]["instance"]
            query = params.get("query", action_type)
            count = int(params.get("count", 3))
            if action_type == "news":
                return tool.search_news(query, count=count)
            elif action_type == "videos":
                return tool.search_videos(query, count=count)
            elif action_type == "images":
                return tool.search_images(query, count=count)
            else:
                return tool.search(query, count=count)

        if tool_name == "wiki":
            if "wiki" not in self.tools or not self.tools["wiki"]["instance"]:
                return "Wiki tool not available"
            tool = self.tools["wiki"]["instance"]
            topic = params.get("topic", action_type)
            sentences = int(params.get("sentences", 5))
            if action_type == "fact":
                return tool.quick_fact(topic)
            elif action_type == "search":
                return tool.search(topic)
            else:
                return tool.get_summary(topic, sentences=sentences)

        if tool_name == "news":
            if "news" not in self.tools or not self.tools["news"]["instance"]:
                # Fallback to search news
                if "search" in self.tools and self.tools["search"]["instance"]:
                    query = params.get("query", params.get("category", "latest news"))
                    return self.tools["search"]["instance"].search_news(query, count=3)
                return "News tool not available"
            tool = self.tools["news"]["instance"]
            country = params.get("country", "us")
            category = params.get("category", None)
            count = int(params.get("count", 3))
            if category:
                return tool.get_category_news(category, country=country, count=count)
            else:
                return tool.get_top_headlines(country=country, count=count)

        return f"Unknown tool: {tool_name}. Available: {', '.join(self.tools.keys())}"

    def execute(self, task):
        """Main execution loop"""
        print(f"\n🤖 Agent starting task: {task}")
        print("━" * 50)

        self.execution_log = []
        steps = []
        final_answer = None
        start_time = time.time()
        errors = 0
        max_errors = 3

        for step_num in range(1, self.max_steps + 1):
            print(f"\n📍 Step {step_num}/{self.max_steps}")

            prompt = self.build_react_prompt(task, steps)

            try:
                result = self.brain.provider_manager.chat(
                    messages=[
                        {"role": "system", "content": "You are Spidey AI Agent. Follow ReAct format: Thought then Action."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=800
                )
                ai_response = result.get("content", "")
            except Exception as e:
                print(f"   ❌ AI Error: {e}")
                errors += 1
                if errors >= max_errors:
                    print(f"   ❌ Too many errors. Stopping.")
                    break
                continue

            thought, action_raw = self.parse_ai_response(ai_response)

            if not thought and not action_raw:
                print(f"   ⚠️ Could not parse response")
                errors += 1
                if errors >= max_errors:
                    break

                # Try to use the raw response as final answer
                if len(ai_response) > 50:
                    final_answer = ai_response
                    break
                continue

            # Show thought (truncated)
            thought_preview = thought[:120] + "..." if len(thought) > 120 else thought
            print(f"   💭 Thought: {thought_preview}")

            if not action_raw:
                print(f"   ⚠️ No action found, trying to continue...")
                errors += 1
                if errors >= max_errors:
                    break
                continue

            # Parse action
            tool_name, action_type, params = self.parse_action(action_raw)

            if not tool_name:
                print(f"   ⚠️ Could not parse action: {action_raw[:80]}")
                errors += 1
                if errors >= max_errors:
                    break
                continue

            print(f"   🔧 Action: {tool_name} | {action_type} | {params}")

            # Final answer check
            if tool_name == "final_answer":
                final_answer = action_type
                print(f"   ✅ Final Answer reached!")
                step_data = {
                    "step": step_num,
                    "thought": thought,
                    "action": f"final_answer",
                    "observation": "Task complete"
                }
                steps.append(step_data)
                self.execution_log.append(step_data)
                break

            # Execute the action
            print(f"   ⏳ Executing {tool_name}...")
            try:
                observation = self.execute_action(tool_name, action_type, params)
            except Exception as e:
                observation = f"Error executing {tool_name}: {str(e)}"
                print(f"   ❌ {observation}")
                errors += 1

            # Show observation preview
            obs_preview = str(observation)[:150].replace("\n", " ")
            print(f"   👁️ Observation: {obs_preview}...")

            # Save step
            step_data = {
                "step": step_num,
                "thought": thought,
                "action": action_raw[:200],
                "observation": str(observation)[:1500]
            }
            steps.append(step_data)
            self.execution_log.append(step_data)

        # Calculate time
        elapsed = time.time() - start_time

        # If no final answer, compile from observations
        if not final_answer:
            if steps:
                # Ask AI to summarize all observations
                observations_text = ""
                for s in steps:
                    if s["observation"] != "Task complete":
                        observations_text += f"\n--- Step {s['step']} ---\n{s['observation']}\n"

                if observations_text:
                    try:
                        summary_result = self.brain.provider_manager.chat(
                            messages=[
                                {"role": "system", "content": "Summarize these results into a clear, helpful answer."},
                                {"role": "user", "content": f"Task: {task}\n\nResults:\n{observations_text}\n\nGive a clear summary answer:"}
                            ],
                            temperature=0.5,
                            max_tokens=600
                        )
                        final_answer = summary_result.get("content", observations_text)
                    except Exception:
                        final_answer = observations_text
                else:
                    final_answer = "Could not complete the task."
            else:
                final_answer = "Could not process the task. Please try rephrasing."

        # Build report
        report = self._build_report(task, steps, final_answer, elapsed)

        # Save to history
        self.task_history.append({
            "task": task,
            "steps": len(steps),
            "time": elapsed,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print("━" * 50)
        print(f"✅ Task completed in {elapsed:.1f}s with {len(steps)} steps")

        return report

    def plan_task(self, task):
        """Plan a task without executing"""
        prompt = f"""You are Spidey AI Agent. Create a step-by-step plan for this task.

Available Tools:
{self.get_tools_description()}

TASK: {task}

Create a numbered plan (3-7 steps). For each step:
- What to do
- Which tool to use
- Expected result

Format each step as:
Step 1: [Description] → Tool: [tool_name] with [params]
Step 2: [Description] → Tool: [tool_name] with [params]
...
Final: [How to combine everything into answer]"""

        try:
            result = self.brain.provider_manager.chat(
                messages=[
                    {"role": "system", "content": "You are a task planning assistant. Be specific about tools and parameters."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )

            plan = result.get("content", "Could not generate plan")

            return (
                f"\n📋 Task Plan\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📌 Task: {task}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{plan}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 Run it: agent {task}"
            )

        except Exception as e:
            return f"⚠️ Planning error: {str(e)}"

    def _build_report(self, task, steps, final_answer, elapsed):
        """Build formatted execution report"""
        lines = [
            f"\n🤖 Agent Report",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"📌 Task: {task}",
            f"📊 Steps: {len(steps)} | ⏱️ Time: {elapsed:.1f}s",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ]

        for step in steps:
            action_preview = step['action'][:60]
            lines.append(f"\n  Step {step['step']}:")
            lines.append(f"    💭 {step['thought'][:80]}")
            lines.append(f"    🔧 {action_preview}")

        lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"\n📝 Result:\n{final_answer}")
        lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        return "\n".join(lines)

    def get_available_tools(self):
        """List all available tools"""
        lines = [
            "\n🔧 Agent Tools",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for name, info in self.tools.items():
            status = "✅" if info["instance"] or name in ["ai_think", "final_answer"] else "❌"
            lines.append(f"  {status} {name}: {info['description']}")

        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        lines.append("\n📌 Usage Examples:")
        lines.append("  agent What is the weather in Karachi")
        lines.append("  agent Tell me about Python from Wikipedia")
        lines.append("  agent Search best laptops 2025 and summarize")
        lines.append("  agent Weather in Lahore and suggest activities")
        lines.append("  agent Compare Python vs JavaScript")
        lines.append("  plan Search AI news and summarize")
        lines.append("  agent tools")
        lines.append("  agent log")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        return "\n".join(lines)

    def get_last_log(self):
        """Get execution log of last task"""
        if not self.execution_log:
            return "No execution log available. Run a task first!"

        lines = ["\n📋 Last Execution Log", "━" * 40]
        for step in self.execution_log:
            lines.append(f"\nStep {step['step']}:")
            lines.append(f"  💭 Thought: {step['thought'][:120]}")
            lines.append(f"  🔧 Action: {step['action'][:120]}")
            obs = step['observation'][:200].replace('\n', ' ')
            lines.append(f"  👁️ Result: {obs}")
        lines.append("━" * 40)

        return "\n".join(lines)

    def get_task_history(self):
        """Get history of all executed tasks"""
        if not self.task_history:
            return "No tasks executed yet."

        lines = ["\n📋 Task History", "━" * 40]
        for i, t in enumerate(self.task_history, 1):
            lines.append(f"  {i}. {t['task'][:50]} — {t['steps']} steps, {t['time']:.1f}s")
        lines.append("━" * 40)

        return "\n".join(lines)