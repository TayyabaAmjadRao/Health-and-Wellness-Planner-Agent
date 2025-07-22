from agents import RunHooks

class LoggingHooks(RunHooks):
    async def on_tool_start(self, tool_name: str, input: str):
        print(f"Tool {tool_name} started with input: {input}")
    
    async def on_tool_end(self, tool_name: str, output: str):
        print(f"Tool {tool_name} completed with output: {output}")