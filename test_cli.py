import asyncio
import sys
from workflow_orchestrator import HealthWellnessWorkflow

async def test_cli():
    workflow = HealthWellnessWorkflow()
    print("Welcome to the Health & Wellness Planner!")
    print("Commands: 'quit' to exit, 'clear' to reset, 'help' for help, 'status' to check workflow stage")
    
    # Simulate the sequence: "i am fat" -> goals -> profile -> generate plans
    inputs = [
        "i am fat",
        "I want to lose weight", 
        "I am a beginner, no dietary restrictions",
        "generate plans"
    ]
    
    for i, user_input in enumerate(inputs):
        print(f"\nYou: {user_input}")
        print("Assistant:")
        
        # Process user input through workflow
        response = await workflow.process_input(user_input)
        
        # Handle structured response format - just print the dict as expected
        print(response)
        
        # Show current stage
        print(f"\n[Current Stage: {workflow.current_stage}]")
        
        # If we reach real_time_delivery stage with the final response, print it clearly
        if workflow.current_stage == 'real_time_delivery' and i == len(inputs) - 1:
            print("\n" + "="*80)
            print("FINAL CLI OUTPUT (this is what main.py should produce):")
            print("="*80)
            print(response)

if __name__ == "__main__":
    asyncio.run(test_cli())
