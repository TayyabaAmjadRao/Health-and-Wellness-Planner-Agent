class Agent:
    def __init__(self, name, description, tools=None, handoffs=None):
        self.name = name
        self.description = description
        self.tools = tools or []
        self.handoffs = handoffs or {}

    async def on_handoff(self, handoff_type, context):
        # Default: do nothing special
        return None

    async def run(self, input, context):
        # Default: subclasses should override
        raise NotImplementedError("Subclasses must implement run()") 