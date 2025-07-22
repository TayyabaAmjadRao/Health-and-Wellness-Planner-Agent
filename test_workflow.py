import asyncio
from workflow_orchestrator import HealthWellnessWorkflow

async def test_workflow():
    workflow = HealthWellnessWorkflow()
    
    # Step 1: Start with user input
    print("Step 1: Starting workflow with 'i am fat'")
    response1 = await workflow.process_input("i am fat")
    print(f"Response 1: {response1}")
    print(f"Current stage: {workflow.current_stage}")
    
    # Step 2: Continue with goal collection 
    if workflow.current_stage == 'goal_collection':
        print("\nStep 2: Providing goal")
        response2 = await workflow.process_input("I want to lose weight")
        print(f"Response 2: {response2}")
        print(f"Current stage: {workflow.current_stage}")
    
    # Step 3: Profile setup 
    if workflow.current_stage == 'profile_setup':
        print("\nStep 3: Setting up profile")
        response3 = await workflow.process_input("I am a beginner, no dietary restrictions")
        print(f"Response 3: {response3}")
        print(f"Current stage: {workflow.current_stage}")
    
    # Step 4: Plan generation
    if workflow.current_stage == 'plan_generation':
        print("\nStep 4: Generating plans")
        response4 = await workflow.process_input("generate plans")
        print(f"Response 4: {response4}")
        print(f"Current stage: {workflow.current_stage}")
        
        print("\n=== FINAL RESPONSE FORMAT ===")
        print(response4)

if __name__ == "__main__":
    asyncio.run(test_workflow())
