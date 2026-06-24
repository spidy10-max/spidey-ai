"""
Spidey AI — System Info
Get PC info: battery, CPU, RAM, network, etc.
"""
import os
import platform
import subprocess
import time
from spidey.logger import app_logger


class SystemInfo:
    """Get system information"""

    def __init__(self):
        app_logger.info("SystemInfo initialized")

    def get_all_info(self):
        """Get complete system info"""
        info = []
        info.append("💻 SYSTEM INFO:")
        info.append(f"   Computer: {platform.node()}")
        info.append(f"   OS: {platform.system()} {platform.release()}")
        info.append(f"   Version: {platform.version()}")
        info.append(f"   Machine: {platform.machine()}")
        info.append(f"   Processor: {platform.processor()}")
        info.append(f"   Python: {platform.python_version()}")
        info.append(f"   User: {os.getenv('USERNAME', 'Unknown')}")
        info.append(f"   Home: {os.path.expanduser('~')}")
        return "\n".join(info)

    def get_battery(self):
        """Get battery info (laptops only)"""
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "(Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus).EstimatedChargeRemaining"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip():
                percent = result.stdout.strip()

                # Get charging status
                result2 = subprocess.run(
                    ["powershell", "-Command",
                     "(Get-WmiObject Win32_Battery).BatteryStatus"],
                    capture_output=True, text=True, timeout=5
                )
                status_code = result2.stdout.strip()
                status = "Charging" if status_code == "2" else "Discharging"

                return f"🔋 Battery: {percent}% ({status})"
            return "🔋 Battery info not available (desktop PC?)"
        except Exception as e:
            return f"🔋 Battery: Could not check ({e})"

    def get_wifi(self):
        """Get current WiFi network"""
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True, text=True, timeout=5
            )
            output = result.stdout

            ssid = "Not connected"
            signal = "N/A"

            for line in output.split("\n"):
                line = line.strip()
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":", 1)[1].strip()
                if "Signal" in line:
                    signal = line.split(":", 1)[1].strip()

            return f"📶 WiFi: {ssid} (Signal: {signal})"
        except Exception as e:
            return f"📶 WiFi: Could not check ({e})"

    def get_ip(self):
        """Get IP address"""
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike '*Loopback*'}).IPAddress"],
                capture_output=True, text=True, timeout=5
            )
            ips = [ip.strip() for ip in result.stdout.strip().split("\n") if ip.strip()]
            if ips:
                return f"🌐 IP: {', '.join(ips[:3])}"
            return "🌐 IP: Not found"
        except Exception as e:
            return f"🌐 IP: Could not check ({e})"

    def get_uptime(self):
        """Get system uptime"""
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime | Select-Object Days, Hours, Minutes"],
                capture_output=True, text=True, timeout=5
            )
            output = result.stdout.strip()
            # Parse output
            lines = [l.strip() for l in output.split("\n") if l.strip() and not l.strip().startswith("-")]
            if len(lines) >= 2:
                parts = lines[-1].split()
                if len(parts) >= 3:
                    return f"⏰ Uptime: {parts[0]} days, {parts[1]} hours, {parts[2]} minutes"
            return f"⏰ Uptime: {output}"
        except Exception as e:
            return f"⏰ Uptime: Could not check ({e})"

    def get_running_apps(self):
        """Get list of running applications"""
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | Select-Object -Property Name, MainWindowTitle | Format-Table -AutoSize"],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout.strip()
            lines = [l.strip() for l in output.split("\n") if l.strip() and not l.strip().startswith("-")]

            if len(lines) > 1:
                result_str = "🖥️ Running Apps:\n"
                for line in lines[1:]:  # Skip header
                    parts = line.split(None, 1)
                    if len(parts) >= 2:
                        result_str += f"   • {parts[0]}: {parts[1]}\n"
                    elif parts:
                        result_str += f"   • {parts[0]}\n"
                return result_str
            return "🖥️ No apps with windows running"
        except Exception as e:
            return f"🖥️ Could not check ({e})"

    def get_date_time(self):
        """Get current date and time"""
        now = time.strftime("%A, %B %d, %Y — %I:%M %p")
        return f"📅 {now}"

    def get_quick_info(self):
        """Quick system summary"""
        info = []
        info.append(self.get_date_time())
        info.append(self.get_battery())
        info.append(self.get_wifi())
        info.append(f"💻 {platform.node()} — {platform.system()} {platform.release()}")
        return "\n".join(info)