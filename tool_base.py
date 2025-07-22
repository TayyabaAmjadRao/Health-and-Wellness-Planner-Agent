class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    async def run(self, input, context):
        raise NotImplementedError("Subclasses must implement run()") 