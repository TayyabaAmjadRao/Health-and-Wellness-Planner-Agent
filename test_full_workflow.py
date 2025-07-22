import asyncio
from workflow_orchestrator import HealthWellnessWorkflow

async def test_full_workflow():
    workflow = HealthWellnessWorkflow()
    
    print("=== COMPLETE WORKFLOW TEST ===")
    print("Simulating: 'i am fat' -> goal collection -> profile setup -> plan generation")
    
    # Step 1: Start with user input "i am fat"
    response1 = await workflow.process_input("i am fat")
    print(f"Step 1 - Stage: {workflow.current_stage}")
    
    # Step 2: Provide goal info (if in goal_collection stage)
    if workflow.current_stage == 'goal_collection':
        response2 = await workflow.process_input("I want to lose weight")
        print(f"Step 2 - Stage: {workflow.current_stage}")
    
    # Step 3: Profile setup (if in profile_setup stage)
    if workflow.current_stage == 'profile_setup':
        response3 = await workflow.process_input("I am a beginner, no dietary restrictions")
        print(f"Step 3 - Stage: {workflow.current_stage}")
    
    # Step 4: Plan generation (if in plan_generation stage)
    if workflow.current_stage == 'plan_generation':
        final_response = await workflow.process_input("generate plans")
        print(f"Step 4 - Stage: {workflow.current_stage}")
        
        print("\n" + "="*80)
        print("FINAL RESPONSE (this should match your expected format):")
        print("="*80)
        print(final_response)
        
        # Print as repr to see exact format including escaped characters
        print("\n" + "="*80) 
        print("FINAL RESPONSE (repr format):")
        print("="*80)
        print(repr(final_response))

if __name__ == "__main__":
    asyncio.run(test_full_workflow())
