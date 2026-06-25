"""
Spidey AI — File Manager
"""
import os
import shutil
import time
from datetime import datetime
from spidey.config import DATA_DIR
from spidey.logger import app_logger, log_event, log_error


class FileManager:

    def __init__(self):
        self.home = os.path.expanduser("~")
        app_logger.info("FileManager initialized")

    def search(self, query, directory=None, extension=None, max_results=20):
        search_dir = directory or self.home
        results = []
        try:
            for root, dirs, files in os.walk(search_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git', 'AppData']]
                for file in files:
                    if query.lower() in file.lower():
                        if extension and not file.lower().endswith(extension.lower()):
                            continue
                        filepath = os.path.join(root, file)
                        try:
                            size = os.path.getsize(filepath)
                            modified = os.path.getmtime(filepath)
                            results.append({"name": file, "path": filepath, "size": size, "size_str": self._format_size(size), "modified": datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M")})
                        except (OSError, PermissionError):
                            continue
                        if len(results) >= max_results:
                            return results
                if root.count(os.sep) - search_dir.count(os.sep) > 4:
                    break
            return results
        except Exception as e:
            log_error(str(e), "search")
            return []

    def search_by_extension(self, extension, directory=None, max_results=20):
        search_dir = directory or self.home
        if not extension.startswith('.'):
            extension = '.' + extension
        results = []
        try:
            for root, dirs, files in os.walk(search_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]
                for file in files:
                    if file.lower().endswith(extension.lower()):
                        filepath = os.path.join(root, file)
                        try:
                            results.append({"name": file, "path": filepath, "size_str": self._format_size(os.path.getsize(filepath))})
                        except (OSError, PermissionError):
                            continue
                        if len(results) >= max_results:
                            return results
                if root.count(os.sep) - search_dir.count(os.sep) > 4:
                    break
            return results
        except Exception as e:
            log_error(str(e), "search_by_extension")
            return []

    def search_recent(self, directory=None, hours=24, max_results=20):
        search_dir = directory or self.home
        cutoff = time.time() - (hours * 3600)
        results = []
        try:
            for root, dirs, files in os.walk(search_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git', 'AppData']]
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(filepath)
                        if mtime > cutoff:
                            results.append({"name": file, "path": filepath, "size_str": self._format_size(os.path.getsize(filepath)), "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M"), "mtime": mtime})
                    except (OSError, PermissionError):
                        continue
                if root.count(os.sep) - search_dir.count(os.sep) > 3:
                    break
            results.sort(key=lambda x: x.get("mtime", 0), reverse=True)
            return results[:max_results]
        except Exception as e:
            log_error(str(e), "search_recent")
            return []

    def search_large_files(self, directory=None, min_size_mb=100, max_results=20):
        search_dir = directory or self.home
        min_bytes = min_size_mb * 1024 * 1024
        results = []
        try:
            for root, dirs, files in os.walk(search_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        size = os.path.getsize(filepath)
                        if size >= min_bytes:
                            results.append({"name": file, "path": filepath, "size": size, "size_str": self._format_size(size)})
                    except (OSError, PermissionError):
                        continue
                if root.count(os.sep) - search_dir.count(os.sep) > 3:
                    break
            results.sort(key=lambda x: x.get("size", 0), reverse=True)
            return results[:max_results]
        except Exception as e:
            log_error(str(e), "search_large_files")
            return []

    def list_folder(self, path=None, show_hidden=False):
        folder = path or self.home
        try:
            items = []
            for item in os.listdir(folder):
                if not show_hidden and item.startswith('.'):
                    continue
                full_path = os.path.join(folder, item)
                is_dir = os.path.isdir(full_path)
                try:
                    size = os.path.getsize(full_path) if not is_dir else 0
                except (OSError, PermissionError):
                    size = 0
                items.append({"name": item, "is_dir": is_dir, "size_str": self._format_size(size) if not is_dir else "Folder", "icon": "📁" if is_dir else "📄"})
            items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
            return items
        except Exception as e:
            log_error(str(e), "list_folder")
            return []

    def create_folder(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            return f"✅ Folder created: {path}"
        except Exception as e:
            return f"❌ Error: {e}"

    def get_disk_space(self, drive="C:"):
        try:
            total, used, free = shutil.disk_usage(drive + "\\")
            return {"drive": drive, "total": self._format_size(total), "used": self._format_size(used), "free": self._format_size(free), "percent_used": round((used / total) * 100, 1)}
        except Exception as e:
            return f"❌ Error: {e}"

    def format_results(self, results, title="Search Results"):
        if not results:
            return "📭 No files found."
        output = f"📂 {title} ({len(results)} found):\n"
        for r in results:
            size = r.get("size_str", "")
            modified = r.get("modified", "")
            output += f"   📄 {r['name']}"
            if size:
                output += f" ({size})"
            if modified:
                output += f" — {modified}"
            output += "\n"
        return output

    def _format_size(self, bytes_size):
        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{round(bytes_size / 1024, 1)} KB"
        elif bytes_size < 1024 * 1024 * 1024:
            return f"{round(bytes_size / (1024 * 1024), 1)} MB"
        else:
            return f"{round(bytes_size / (1024 * 1024 * 1024), 1)} GB"