"""
Spidey Agent — Main Agent Interface
Day 45
"""

from spidey.agent.react_agent import ReActAgent
from spidey.logger import log_event, log_error


class SpideyAgent:

    def __init__(self, brain):
        self.brain = brain
        self.react_agent = None
        self._init_agent()

    def _init_agent(self):
        try:
            self.react_agent = ReActAgent(self.brain)
            log_event("SpideyAgent initialized")
        except Exception as e:
            log_error(str(e), "SpideyAgent init")
            self.react_agent = None

    def execute(self, task):
        if not self.react_agent:
            return "⚠️ Agent not initialized."
        if not task or not task.strip():
            return "⚠️ Please provide a task. Example: agent What is weather in Karachi"
        try:
            return self.react_agent.execute(task.strip())
        except Exception as e:
            log_error(str(e), "Agent execute")
            return f"⚠️ Agent error: {str(e)}"

    def plan_task(self, task):
        if not self.react_agent:
            return "⚠️ Agent not initialized."
        if not task or not task.strip():
            return "⚠️ Please provide a task to plan."
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