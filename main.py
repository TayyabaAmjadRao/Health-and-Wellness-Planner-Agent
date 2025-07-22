from dotenv import load_dotenv
load_dotenv()

from workflow_orchestrator import HealthWellnessWorkflow
import asyncio

async def main():
    workflow = HealthWellnessWorkflow()
    print("Welcome to the Health & Wellness Planner!")
    print("Commands: 'quit' to exit, 'clear' to reset, 'help' for help, 'status' to check workflow stage")
    
    try:
        while True:
            try:
                user_input = input("You: ")
            except EOFError:
                # Handle EOF (when input is piped)
                break
            
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            elif user_input.lower() == "clear":
                workflow.clear_context()
                print("Session cleared. Starting fresh!")
                continue
            elif user_input.lower() == "help":
                print("Available commands:")
                print("  'quit' - Exit the program")
                print("  'clear' - Clear current session and start fresh")
                print("  'status' - Show current workflow stage")
                print("  'help' - Show this help message")
                continue
            elif user_input.lower() == "status":
                print(f"Current workflow stage: {workflow.current_stage}")
                continue
            
            print("Assistant:")
            
            # Process user input through workflow
            response = await workflow.process_input(user_input)
            
            # Handle structured response format
            if isinstance(response, dict):
                # Print formatted structured response
                print(response)
            else:
                # Print simple string response
                print(response)
            
            # Show current stage
            print(f"\n[Current Stage: {workflow.current_stage}]")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    asyncio.run(main())
