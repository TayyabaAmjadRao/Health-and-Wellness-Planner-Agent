import asyncio
from unittest.mock import AsyncMock, patch
from workflow_orchestrator import HealthWellnessWorkflow

# Mock data to simulate the expected format
mock_meal_plan = [
    'Breakfast: Oatmeal with berries and a sprinkle of nuts, Lunch: Salad with grilled chicken or fish, Dinner: Baked salmon with roasted vegetables',
    'Breakfast: Greek yogurt with fruit and granola, Lunch: Leftover baked salmon and vegetables, Dinner: Chicken stir-fry with brown rice',
    'Breakfast: Scrambled eggs with spinach and whole-wheat toast, Lunch: Lentil soup with a side salad, Dinner: Turkey meatballs with zucchini noodles',
    'Breakfast: Smoothie with spinach, banana, and protein powder, Lunch: Leftover turkey meatballs and zucchini noodles, Dinner: Chicken breast with quinoa and steamed broccoli',
    'Breakfast: Whole-wheat toast with avocado and a poached egg, Lunch: Tuna salad sandwich on whole-wheat bread (light mayo), Dinner: Shrimp scampi with whole-wheat pasta (smaller portion)',
    'Breakfast: Cottage cheese with sliced peaches, Lunch: Leftover shrimp scampi, Dinner: Lean ground beef and bean chili with a side salad',
    'Breakfast: Berries and a small protein bar, Lunch: Salad with chickpeas and a light vinaigrette, Dinner: Baked chicken breast with sweet potato and green beans'
]

mock_workout_plan = [
    '**Monday:**\n* Warm-up (5 min cardio, dynamic stretching)\n* Full Body Circuit:\n    * Squats: 3 sets of 10-12 reps\n    * Push-ups: 3 sets of as many reps as possible (AMRAP)\n    * Rows (using resistance bands or dumbbells): 3 sets of 10-12 reps\n    * Lunges (alternating legs): 3 sets of 10-12 reps per leg\n    * Plank: 3 sets, hold for 30-60 seconds\n* Cool-down (5 min static stretching)',
    '**Tuesday:**\n* Cardio: 30-45 minutes of moderate-intensity cardio (brisk walking, jogging, cycling, swimming)',
    '**Wednesday:**\n* Warm-up (5 min cardio, dynamic stretching)\n* Upper Body Strength:\n    * Bench Press (using dumbbells or barbell): 3 sets of 8-12 reps\n    * Overhead Press (using dumbbells or barbell): 3 sets of 8-12 reps\n    * Bicep Curls: 3 sets of 10-15 reps\n    * Triceps Extensions: 3 sets of 10-15 reps\n* Cool-down (5 min static stretching)',
    '**Thursday:**\n* Cardio: 30-45 minutes of moderate-intensity cardio (choose a different activity than Tuesday)',
    '**Friday:**\n* Warm-up (5 min cardio, dynamic stretching)\n* Lower Body Strength:\n    * Squats: 3 sets of 10-12 reps\n    * Deadlifts (using dumbbells or barbell): 1 set of 5 reps, 1 set of 3 reps, 1 set of 1 rep (focus on form)\n    * Hamstring Curls: 3 sets of 10-15 reps\n    * Calf Raises: 3 sets of 15-20 reps\n* Cool-down (5 min static stretching)',
    '**Saturday:**\n* Active Rest:  30-60 minutes of light activity like yoga, a leisurely walk, or swimming.  Focus on flexibility and recovery.',
    '**Sunday:**\n* Rest: Complete rest or very light activity like a short walk.'
]

async def test_workflow_with_mock():
    workflow = HealthWellnessWorkflow()
    
    # Mock the tools to return our expected data
    workflow.tools['meal_planner'].run = AsyncMock(return_value=mock_meal_plan)
    workflow.tools['workout_recommender'].run = AsyncMock(return_value=mock_workout_plan)
    workflow.tools['goal_analyzer'].run = AsyncMock(return_value={'goals': {'quantity': None, 'metric': 'weight', 'duration': None, 'goal_type': 'weight loss'}})
    workflow.main_agent.run = AsyncMock(return_value="Mock agent response")
    
    # Simulate the workflow
    print("Step 1: Starting workflow with 'i am fat'")
    response1 = await workflow.process_input("i am fat")
    print(f"Current stage: {workflow.current_stage}")
    
    if workflow.current_stage == 'goal_collection':
        print("\nStep 2: Providing goal")
        response2 = await workflow.process_input("I want to lose weight")
        print(f"Current stage: {workflow.current_stage}")
    
    if workflow.current_stage == 'profile_setup':
        print("\nStep 3: Setting up profile")
        response3 = await workflow.process_input("I am a beginner, no dietary restrictions")
        print(f"Current stage: {workflow.current_stage}")
    
    if workflow.current_stage == 'plan_generation':
        print("\nStep 4: Generating plans")
        response4 = await workflow.process_input("generate plans")
        print(f"Current stage: {workflow.current_stage}")
        
        print("\n=== FINAL RESPONSE FORMAT ===")
        print(response4)
        
        print("\n=== FORMATTED AS REQUESTED ===")
        print(repr(response4))

if __name__ == "__main__":
    asyncio.run(test_workflow_with_mock())
