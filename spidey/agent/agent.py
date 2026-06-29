"""
Spidey Agent — Main Agent Interface
Day 48 — With Complex Tasks + Safety + Reasoning
"""

from spidey.agent.react_agent import ReActAgent
from spidey.agent.reasoning import ReasoningEngine
from spidey.agent.complex_tasks import ComplexTaskHandler
from spidey.agent.safety import SafetyChecker
from spidey.logger import log_event, log_error


class SpideyAgent:

    def __init__(self, brain):
        self.brain = brain
        self.react_agent = None
        self.reasoning = None
        self.complex_handler = None
        self.safety = None
        self._init_agent()

    def _init_agent(self):
        try:
            self.react_agent = ReActAgent(self.brain)
            self.reasoning = ReasoningEngine(self.brain)
            self.complex_handler = ComplexTaskHandler(self.brain)
            self.safety = SafetyChecker()
            log_event("SpideyAgent initialized")
        except Exception as e:
            log_error(str(e), "SpideyAgent init")
            self.react_agent = None
            self.reasoning = None
            self.complex_handler = None
            self.safety = None

    def execute(self, task):
        """Execute a task — safety check → complex handler → ReAct agent"""
        if not self.react_agent:
            return "⚠️ Agent not initialized."
        if not task or not task.strip():
            return "⚠️ Please provide a task."

        try:
            # Step 1: Safety check
            if self.safety:
                safety_result = self.safety.check_command(task)

                if safety_result["action"] == "block":
                    return f"🚫 Task BLOCKED: {safety_result['reason']}"

                if safety_result["action"] == "confirm":
                    if not self.safety.ask_confirmation(
                        safety_result["reason"],
                        safety_result["risk_level"]
                    ):
                        return "❌ Task cancelled by user."

            # Step 2: Try complex task handler (fast, pre-built patterns)
            if self.complex_handler:
                complex_result = self.complex_handler.detect_and_handle(task)
                if complex_result:
                    return complex_result

            # Step 3: Show analysis
            if self.reasoning:
                analysis = self.reasoning.should_use_agent(task)
                complexity = analysis.get("complexity", "unknown")
                tools = ", ".join(analysis.get("tools_needed", []))
                if tools:
                    print(f"   🧠 Complexity: {complexity} | Tools: {tools}")

            # Step 4: Execute with ReAct agent
            return self.react_agent.execute(task.strip())

        except Exception as e:
            log_error(str(e), "Agent execute")
            return f"⚠️ Agent error: {str(e)}"

    def smart_execute(self, task):
        """Smart execution — AI analyzes first, then executes"""
        if not self.react_agent or not self.reasoning:
            return self.execute(task)

        try:
            # Safety check first
            if self.safety:
                safety_result = self.safety.check_command(task)
                if safety_result["action"] == "block":
                    return f"🚫 Task BLOCKED: {safety_result['reason']}"
                if safety_result["action"] == "confirm":
                    if not self.safety.ask_confirmation(
                        safety_result["reason"],
                        safety_result["risk_level"]
                    ):
                        return "❌ Task cancelled by user."

            # Try complex handler first
            if self.complex_handler:
                complex_result = self.complex_handler.detect_and_handle(task)
                if complex_result:
                    return complex_result

            # AI analysis
            print(f"\n   🧠 Analyzing task...")
            analysis = self.reasoning.analyze_task(task)

            if "error" in analysis:
                print(f"   ⚠️ Analysis failed, using standard agent")
                return self.react_agent.execute(task)

            task_type = analysis.get("task_type", "unknown")
            steps = analysis.get("steps", [])

            print(f"   📋 Task type: {task_type}")
            print(f"   📊 Planned steps: {len(steps)}")

            if steps:
                for s in steps:
                    print(f"      {s['step']}. {s.get('description', '')} → {s.get('tool', '?')}")

            return self.react_agent.execute(task)

        except Exception as e:
            log_error(str(e), "Smart execute")
            return f"⚠️ Smart execute error: {str(e)}"

    def analyze(self, task):
        """Analyze a task without executing"""
        if not self.reasoning:
            return "⚠️ Reasoning engine not available."

        try:
            # Safety analysis
            safety_info = ""
            if self.safety:
                safety_result = self.safety.check_command(task)
                risk_icons = {
                    "none": "✅", "low": "💡",
                    "medium": "⚠️", "high": "🔴", "critical": "🚫"
                }
                icon = risk_icons.get(safety_result["risk_level"], "?")
                safety_info = (
                    f"\n🛡️ Safety: {icon} {safety_result['risk_level'].upper()}"
                    f" — {safety_result['action'].upper()}"
                )

            # Reasoning analysis
            should_agent = self.reasoning.should_use_agent(task)
            suggestions = self.reasoning.suggest_tools(task)
            ai_analysis = self.reasoning.analyze_task(task)

            lines = [
                f"\n🧠 Task Analysis",
                "━" * 40,
                f"📌 Task: {task}",
                f"📊 Complexity: {should_agent.get('complexity', '?')}",
                f"🤖 Use Agent: {'Yes' if should_agent.get('use_agent') else 'No'}",
                f"💡 Reason: {should_agent.get('reason', '?')}",
            ]

            if safety_info:
                lines.append(safety_info)

            if should_agent.get("tools_needed"):
                lines.append(f"🔧 Tools needed: {', '.join(should_agent['tools_needed'])}")

            if suggestions:
                lines.append(f"\n📋 Tool Suggestions:")
                for s in suggestions:
                    lines.append(f"  🔧 {s['tool']} | {s['action']} | confidence: {s['confidence']}%")
                    if s.get("params"):
                        lines.append(f"     Params: {s['params']}")

            if ai_analysis and ai_analysis.get("steps"):
                lines.append(f"\n📋 AI Planned Steps:")
                for step in ai_analysis["steps"]:
                    lines.append(
                        f"  {step['step']}. {step.get('description', '')} "
                        f"→ {step.get('tool', '?')} | {step.get('action', '?')}"
                    )

            lines.append("━" * 40)
            return "\n".join(lines)

        except Exception as e:
            return f"⚠️ Analysis error: {str(e)}"

    def check_safety(self, command):
        """Check safety of a command and show report"""
        if not self.safety:
            return "⚠️ Safety checker not available."
        return self.safety.get_risk_report(command)

    def plan_task(self, task):
        if not self.react_agent:
            return "⚠️ Agent not initialized."
        if not task or not task.strip():
            return "⚠️ Please provide a task."
        try:
            return self.react_agent.plan_task(task.strip())
        except Exception as e:
            log_error(str(e), "Agent plan")
            return f"⚠️ Planning error: {str(e)}"

    def get_available_tools(self):
        if not self.react_agent:
            return "⚠️ Agent not initialized."
        return self.react_agent.get_available_tools()

    def get_last_log(self):
        if not self.react_agent:
            return "⚠️ Agent not initialized."
        return self.react_agent.get_last_log()

    def get_task_history(self):
        if not self.react_agent:
            return "⚠️ Agent not initialized."
        return self.react_agent.get_task_history()