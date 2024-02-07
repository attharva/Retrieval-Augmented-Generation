import json
from collections import defaultdict
from datetime import datetime

class ConversationState:
    def __init__(self):
        self.topic_distribution = defaultdict(int)
        self.topic_hit = defaultdict(int)
        self.topic_miss = defaultdict(int)
        self.error_count = 0
        self.chitchat_state = {}
        self.qa_state = {}
        self.conversation_history = []  # List to store conversation history

    @classmethod
    def from_serialized(cls, data):
        instance = cls()
        print("umm", data)
        instance.topic_distribution = defaultdict(int, data.get("topic_distribution", {}))
        instance.topic_hit = defaultdict(int, data.get("topic_hit", {}))
        instance.topic_miss = defaultdict(int, data.get("topic_miss", {}))
        instance.error_count = data.get("error_count", 0)
        instance.chitchat_state = data.get("chitchat_state", {})
        instance.qa_state = data.get("qa_state", {})
        instance.conversation_history = data.get("conversation_history", [])
        return instance

    def serialize(self):
        return {
            "topic_distribution": self.topic_distribution,
            "topic_hit": self.topic_hit,
            "topic_miss": self.topic_miss,
            "error_count": self.error_count,
            "chitchat_state": self.chitchat_state,
            "qa_state": self.qa_state,
            "conversation_history": self.conversation_history,
        }

    def add_to_history(self, query, response, duration):
        timestamp = datetime.now().isoformat()
        self.conversation_history.append({
            'query': query,
            'response': response,
            'timestamp': timestamp,
            'duration': duration,
            'feedback': 0
        })
