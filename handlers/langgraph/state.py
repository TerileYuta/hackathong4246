class AgentState:
    def __init__(self, query, history = None):
        self.query = query
        self.history = history if history else []
        self.next_action = None
        self.tool_name = None
        self.tool_args = None
        self.tool_result = None