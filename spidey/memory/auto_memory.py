"""
Spidey AI — Auto Memory Detector
Automatically detects facts about user from conversations
"""
import re
from spidey.logger import app_logger, log_event


DETECTION_PATTERNS = [
    # Name
    {
        "patterns": [
            r"my name is (\w+)",
            r"call me (\w+)",
            r"mera naam (\w+)",
            r"mera name (\w+)",
        ],
        "key": "name",
        "category": "personal",
        "exclude_values": [
            "a", "an", "the", "not", "very", "really", "so",
            "just", "also", "here", "there", "doing", "going",
            "looking", "trying", "working", "learning", "using",
            "interested", "happy", "sad", "tired", "fine", "good",
            "great", "okay", "ok", "sure", "new", "old"
        ]
    },
    # Age
    {
        "patterns": [
            r"i'?m (\d{1,2}) years old",
            r"i am (\d{1,2}) years old",
            r"my age is (\d{1,2})",
            r"i'?m (\d{1,2}) yrs",
            r"i'?m (\d{1,2}) saal",
            r"meri age (\d{1,2})",
            r"meri umar (\d{1,2})",
        ],
        "key": "age",
        "category": "personal",
        "exclude_values": []
    },
    # City/Location
    {
        "patterns": [
            r"i live in (\w+(?:\s\w+)?)",
            r"i'?m from (\w+(?:\s\w+)?)",
            r"i am from (\w+(?:\s\w+)?)",
            r"i stay in (\w+(?:\s\w+)?)",
            r"my city is (\w+(?:\s\w+)?)",
            r"ma (\w+) ma rehta",
            r"mera shehar (\w+)",
        ],
        "key": "city",
        "category": "personal",
        "exclude_values": []
    },
    # Favorite Language
    {
        "patterns": [
            r"i love (\w+) programming",
            r"i love coding in (\w+)",
            r"my favorite language is (\w+)",
            r"my favourite language is (\w+)",
            r"i prefer (\w+) for coding",
            r"i use (\w+) for programming",
        ],
        "key": "favorite_language",
        "category": "coding",
        "exclude_values": []
    },
    # Favorite Color
    {
        "patterns": [
            r"my favorite color is (\w+)",
            r"my favourite colour is (\w+)",
            r"i love (\w+) color",
            r"i like (\w+) colour",
            r"mera favorite color (\w+)",
        ],
        "key": "favorite_color",
        "category": "personal",
        "exclude_values": []
    },
    # Hobby
    {
        "patterns": [
            r"my hobby is (\w+(?:\s\w+)?)",
            r"i enjoy (\w+(?:\s\w+)?)",
            r"mera shoq (\w+(?:\s\w+)?)",
        ],
        "key": "hobby",
        "category": "personal",
        "exclude_values": ["you", "it", "that", "this"]
    },
    # Job/Occupation
    {
        "patterns": [
            r"i work as (?:a |an )?(\w+(?:\s\w+)?)",
            r"i'?m a (\w+ developer)",
            r"i'?m a (\w+ engineer)",
            r"i'?m a (\w+ student)",
            r"i am a (\w+ developer)",
            r"i am a (\w+ engineer)",
            r"i am a (\w+ student)",
            r"my job is (\w+(?:\s\w+)?)",
            r"i study (\w+(?:\s\w+)?)",
        ],
        "key": "occupation",
        "category": "work",
        "exclude_values": []
    },
    # Education
    {
        "patterns": [
            r"i study at (\w+(?:\s\w+)?(?:\s\w+)?)",
            r"i go to (\w+(?:\s\w+)?(?:\s\w+)?)",
            r"my university is (\w+(?:\s\w+)?(?:\s\w+)?)",
            r"my college is (\w+(?:\s\w+)?(?:\s\w+)?)",
            r"my school is (\w+(?:\s\w+)?(?:\s\w+)?)",
        ],
        "key": "education",
        "category": "personal",
        "exclude_values": []
    },
]


class AutoMemory:
    """Automatically detects and saves user information"""

    def __init__(self, memory_instance):
        self.memory = memory_instance
        self.detected_this_session = {}
        app_logger.info("AutoMemory initialized")

    def detect_and_save(self, message):
        """
        Analyze a user message and auto-save detected info

        Returns:
            List of detected facts
        """
        detected = []
        message_lower = message.lower().strip()

        for pattern_config in DETECTION_PATTERNS:
            key = pattern_config["key"]
            category = pattern_config["category"]
            exclude = pattern_config.get("exclude_values", [])

            for pattern in pattern_config["patterns"]:
                match = re.search(pattern, message_lower)
                if match:
                    value = match.group(1).strip()

                    # Skip excluded values
                    if value.lower() in exclude:
                        continue

                    # Skip very short values
                    if len(value) < 2:
                        continue

                    # Skip if same value already detected this session
                    if key in self.detected_this_session:
                        if self.detected_this_session[key].lower() == value.lower():
                            continue

                    # Capitalize properly
                    if key in ["name", "city", "education"]:
                        value = value.title()

                    # Save to memory
                    self.memory.remember(key, value, category)
                    self.detected_this_session[key] = value

                    detected.append({
                        "key": key,
                        "value": value,
                        "category": category
                    })

                    log_event("Auto-detected", f"{key} = {value}")

                    # Only first match per key
                    break

        return detected

    def get_detected_count(self):
        """How many facts detected this session"""
        return len(self.detected_this_session)

    def get_detected_facts(self):
        """Get all facts detected this session"""
        return self.detected_this_session.copy()

    def reset_session(self):
        """Reset detected facts for new session"""
        self.detected_this_session = {}