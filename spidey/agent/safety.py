"""
Spidey Safety System
Checks commands before execution — prevents harmful actions
Day 48 — Safety first!
"""

import re


class SafetyChecker:
    """
    Checks user commands and agent actions for safety.
    Blocks dangerous commands, asks confirmation for risky ones.
    """

    def __init__(self):
        # BLOCKED — Never execute these
        self.blocked_patterns = [
            r"rm\s+-rf",
            r"del\s+/[sfq]",
            r"format\s+[a-z]:",
            r"rmdir\s+/s",
            r"drop\s+table",
            r"delete\s+from",
            r"truncate\s+table",
            r"shutdown\s+/s",
            r"shutdown\s+-s",
            r"mkfs\.",
            r"dd\s+if=",
            r":(){ :|:& };:",
            r"fork\s*bomb",
            r"rm\s+-r\s+/",
            r"del\s+\*\.\*",
            r"format\s+c:",
            r"erase\s+/[sfq]",
        ]

        # CONFIRM — Ask user before executing
        self.confirm_patterns = [
            r"delete",
            r"remove",
            r"hatao",
            r"mita\s*do",
            r"erase",
            r"clear\s+all",
            r"reset\s+all",
            r"uninstall",
            r"overwrite",
            r"replace\s+all",
            r"send\s+email",
            r"post\s+to",
            r"publish",
            r"share\s+on",
            r"upload",
            r"download\s+and\s+run",
            r"execute\s+script",
            r"run\s+command",
            r"open\s+url",
            r"visit\s+website",
            r"install\s+",
            r"pip\s+install",
            r"change\s+password",
            r"modify\s+system",
        ]

        # SAFE — Always allowed
        self.safe_patterns = [
            r"weather",
            r"news",
            r"search",
            r"wiki",
            r"tell\s+me",
            r"what\s+is",
            r"who\s+is",
            r"how\s+to",
            r"explain",
            r"summarize",
            r"compare",
            r"suggest",
            r"recommend",
            r"hello",
            r"help",
            r"show",
            r"list",
            r"find",
            r"get",
        ]

        # Sensitive data patterns
        self.sensitive_patterns = [
            r"password",
            r"credit\s*card",
            r"ssn",
            r"social\s*security",
            r"bank\s*account",
            r"api\s*key",
            r"secret\s*key",
            r"private\s*key",
            r"token",
        ]

    def check_command(self, command):
        """
        Check if a command is safe to execute.

        Args:
            command: User's command string

        Returns:
            dict with:
                - safe: True/False
                - action: "allow", "confirm", "block"
                - reason: Why blocked/needs confirmation
                - risk_level: "none", "low", "medium", "high", "critical"
        """
        cmd = command.lower().strip()

        # Check blocked patterns first
        for pattern in self.blocked_patterns:
            if re.search(pattern, cmd):
                return {
                    "safe": False,
                    "action": "block",
                    "reason": f"Dangerous command detected: matches '{pattern}'",
                    "risk_level": "critical"
                }

        # Check sensitive data
        for pattern in self.sensitive_patterns:
            if re.search(pattern, cmd):
                return {
                    "safe": False,
                    "action": "confirm",
                    "reason": f"Sensitive data detected: '{pattern}'. Be careful sharing this.",
                    "risk_level": "high"
                }

        # Check confirm patterns
        for pattern in self.confirm_patterns:
            if re.search(pattern, cmd):
                return {
                    "safe": True,
                    "action": "confirm",
                    "reason": f"This action may modify data: '{pattern}'",
                    "risk_level": "medium"
                }

        # Check safe patterns
        for pattern in self.safe_patterns:
            if re.search(pattern, cmd):
                return {
                    "safe": True,
                    "action": "allow",
                    "reason": "Safe command",
                    "risk_level": "none"
                }

        # Default — allow but with low risk
        return {
            "safe": True,
            "action": "allow",
            "reason": "No known risk patterns detected",
            "risk_level": "low"
        }

    def check_agent_action(self, tool_name, action, params):
        """
        Check if an agent's tool action is safe.

        Args:
            tool_name: Name of tool being called
            action: Action type
            params: Parameters dict

        Returns:
            dict with safety info
        """
        # Safe tools — always allowed
        safe_tools = ["weather", "news", "search", "wiki", "ai_think", "final_answer"]

        if tool_name in safe_tools:
            return {
                "safe": True,
                "action": "allow",
                "reason": f"Tool '{tool_name}' is safe",
                "risk_level": "none"
            }

        # File operations — need confirmation
        file_tools = ["file_manager", "file_search", "file_delete"]
        if tool_name in file_tools:
            if action in ["delete", "remove", "move"]:
                return {
                    "safe": True,
                    "action": "confirm",
                    "reason": f"File operation: {action}",
                    "risk_level": "high"
                }

        # System operations — need confirmation
        system_tools = ["app_launcher", "system_control", "computer"]
        if tool_name in system_tools:
            return {
                "safe": True,
                "action": "confirm",
                "reason": f"System operation: {tool_name}.{action}",
                "risk_level": "medium"
            }

        # Unknown tool — allow with caution
        return {
            "safe": True,
            "action": "allow",
            "reason": f"Unknown tool '{tool_name}' — proceeding with caution",
            "risk_level": "low"
        }

    def ask_confirmation(self, reason, risk_level="medium"):
        """
        Ask user for confirmation before executing risky action.

        Args:
            reason: Why confirmation is needed
            risk_level: none/low/medium/high/critical

        Returns:
            True if user confirms, False otherwise
        """
        risk_icons = {
            "none": "✅",
            "low": "💡",
            "medium": "⚠️",
            "high": "🔴",
            "critical": "🚫"
        }

        icon = risk_icons.get(risk_level, "⚠️")

        print(f"\n   {icon} Safety Check [{risk_level.upper()}]")
        print(f"   📌 {reason}")

        try:
            response = input("   ➡️ Continue? (y/n): ").strip().lower()
            return response in ["y", "yes", "haan", "ha"]
        except (KeyboardInterrupt, EOFError):
            print("\n   ❌ Cancelled!")
            return False

    def sanitize_input(self, text):
        """
        Clean user input — remove potentially harmful content.

        Args:
            text: Raw user input

        Returns:
            Cleaned text
        """
        # Remove shell injection attempts
        dangerous_chars = [";", "&&", "||", "`", "$(", "${"]
        cleaned = text
        for char in dangerous_chars:
            cleaned = cleaned.replace(char, "")

        # Remove script tags
        cleaned = re.sub(r"<script.*?>.*?</script>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)

        # Remove SQL injection attempts
        sql_patterns = [
            r"'\s*or\s+'1'\s*=\s*'1",
            r";\s*drop\s+table",
            r";\s*delete\s+from",
            r"union\s+select",
        ]
        for pattern in sql_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        return cleaned.strip()

    def get_risk_report(self, command):
        """
        Generate a detailed risk report for a command.

        Args:
            command: Command to analyze

        Returns:
            Formatted risk report string
        """
        check = self.check_command(command)

        risk_bars = {
            "none": "▓░░░░",
            "low": "▓▓░░░",
            "medium": "▓▓▓░░",
            "high": "▓▓▓▓░",
            "critical": "▓▓▓▓▓"
        }

        risk_colors = {
            "none": "✅",
            "low": "💡",
            "medium": "⚠️",
            "high": "🔴",
            "critical": "🚫"
        }

        bar = risk_bars.get(check["risk_level"], "?????")
        icon = risk_colors.get(check["risk_level"], "?")

        return (
            f"\n🛡️ Safety Report\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Command: {command[:50]}\n"
            f"{icon} Risk Level: {check['risk_level'].upper()} [{bar}]\n"
            f"🔧 Action: {check['action']}\n"
            f"💡 Reason: {check['reason']}\n"
            f"{'✅ SAFE' if check['safe'] else '❌ BLOCKED'}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )


# ========================================
# Standalone Test
# ========================================
if __name__ == "__main__":
    print("🕷️ Spidey Safety System — Testing\n")

    safety = SafetyChecker()

    # Test commands
    test_commands = [
        # Safe
        "Weather in Karachi",
        "Search Python tutorials",
        "Tell me about Pakistan",
        "Latest news",

        # Needs confirmation
        "Delete this file",
        "Send email to someone",
        "Install new package",
        "Download and run this script",
        "Remove all data",

        # Blocked
        "rm -rf /",
        "format c:",
        "DROP TABLE users",
        "del /s /q *.*",
        "shutdown /s",

        # Sensitive
        "My password is 12345",
        "Credit card number 4111",
        "API key is sk-abc123",
    ]

    print("=" * 60)
    print("SAFETY CHECK TESTS")
    print("=" * 60)

    for cmd in test_commands:
        check = safety.check_command(cmd)

        risk_icons = {
            "none": "✅",
            "low": "💡",
            "medium": "⚠️",
            "high": "🔴",
            "critical": "🚫"
        }

        icon = risk_icons.get(check["risk_level"], "?")
        action = check["action"].upper()

        print(f"\n  {icon} '{cmd[:40]}...'")
        print(f"     Action: {action} | Risk: {check['risk_level']} | {check['reason'][:50]}")

    # Test risk report
    print("\n" + "=" * 60)
    print("RISK REPORTS")
    print("=" * 60)

    print(safety.get_risk_report("Weather in Karachi"))
    print(safety.get_risk_report("Delete all my files"))
    print(safety.get_risk_report("rm -rf /"))

    # Test sanitize
    print("\n" + "=" * 60)
    print("SANITIZE TESTS")
    print("=" * 60)

    dirty_inputs = [
        "Hello; rm -rf /",
        "Search <script>alert('hack')</script>",
        "' OR '1'='1",
        "Normal safe input",
    ]

    for dirty in dirty_inputs:
        clean = safety.sanitize_input(dirty)
        changed = "🔧 CLEANED" if dirty != clean else "✅ SAME"
        print(f"\n  Input:  '{dirty[:40]}'")
        print(f"  Output: '{clean[:40]}' [{changed}]")