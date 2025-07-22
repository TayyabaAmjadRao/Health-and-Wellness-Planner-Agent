from typing import Dict, Any, List, Optional
import asyncio
from context import UserSessionContext
from agents.agent import WellnessPlannerAgent
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from tools.tracker import ProgressTrackerTool
from tools.scheduler import CheckinSchedulerTool
from agents.injury_support_agent import InjurySupportAgent
from agents.nutrition_expert_agent import NutritionExpertAgent
from agents.escalation_agent import EscalationAgent

class HealthWellnessWorkflow:
    """
    Orchestrates the complete health and wellness agent workflow.
    
    Workflow Stages:
    1. User Starts Chat
    2. Goal Collection
    3. Profile Setup
    4. Plan Generation
    5. Real-Time Delivery
    6. Progress Tracking
    7. Specialized Help
    8. Ongoing Support
    """
    
    def __init__(self):
        self.context = UserSessionContext()
        self.main_agent = WellnessPlannerAgent()
        self.specialized_agents = {
            'injury_support': InjurySupportAgent(),
            'nutrition_expert': NutritionExpertAgent(),
            'escalation': EscalationAgent()
        }
        self.tools = {
            'goal_analyzer': GoalAnalyzerTool(),
            'meal_planner': MealPlannerTool(),
            'workout_recommender': WorkoutRecommenderTool(),
            'progress_tracker': ProgressTrackerTool(),
            'checkin_scheduler': CheckinSchedulerTool()
        }
        self.current_stage = 'user_starts_chat'
        self.workflow_complete = False
    
    async def start_workflow(self, initial_input: str) -> Dict[str, Any]:
        """
        Starts the complete workflow based on user input.
        """
        print(f"🚀 Starting Health & Wellness Workflow")
        print(f"📝 Initial Input: {initial_input}")
        
        # Stage 1: User Starts Chat
        response = await self._handle_user_starts_chat(initial_input)
        
        return {
            'stage': self.current_stage,
            'response': response,
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    async def _handle_user_starts_chat(self, input_text: str) -> str:
        """
        Stage 1: Handle initial user interaction and determine next steps.
        """
        self.current_stage = 'user_starts_chat'
        print(f"🎯 Stage 1: User Starts Chat")
        
        # Set user profile based on initial input
        self.context.user_profile = input_text
        
        # Use main agent to understand user intent
        response = await self.main_agent.run(input_text, self.context)
        
        # Convert response to string if it's a dict
        if isinstance(response, dict):
            response_text = response.get('response', str(response))
        else:
            response_text = str(response)
        
        # Check if goal was detected from the main agent response
        if self.context.goal:
            # Goal was detected, move to profile setup
            self.current_stage = 'profile_setup'
            return f"{response_text}\n\n📋 Now let's set up your profile. Could you share your current fitness level, dietary preferences, and any health considerations?"
        else:
            # No goal detected, move to goal collection
            self.current_stage = 'goal_collection'
            return f"{response_text}\n\n🎯 Let's start by understanding your health and wellness goals. What would you like to achieve?"
    
    async def handle_goal_collection(self, goals_input: str) -> Dict[str, Any]:
        """
        Stage 2: Collect and analyze user goals.
        """
        self.current_stage = 'goal_collection'
        print(f"🎯 Stage 2: Goal Collection")
        
        # Use GoalAnalyzerTool to process goals
        goals_result = await self.tools['goal_analyzer'].run(goals_input, self.context)
        
        # Update context with analyzed goals
        if isinstance(goals_result, dict) and 'goal' in goals_result:
            self.context.goal = goals_result['goal']
        elif isinstance(goals_result, dict) and 'goals' in goals_result:
            self.context.goal = goals_result['goals']
        else:
            # Set a default goal structure based on user input
            self.context.goal = {
                'quantity': None,
                'metric': 'weight',
                'duration': None,
                'goal_type': 'weight loss'
            }
        
        # Move to profile setup
        self.current_stage = 'profile_setup'
        
        return {
            'stage': self.current_stage,
            'response': f"✅ Great! I've analyzed your goals: {goals_result}\n\n📋 Now let's set up your profile. Could you share your current fitness level, dietary preferences, and any health considerations?",
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    async def handle_profile_setup(self, profile_input: str) -> Dict[str, Any]:
        """
        Stage 3: Set up user profile and preferences.
        """
        self.current_stage = 'profile_setup'
        print(f"🎯 Stage 3: Profile Setup")
        
        # Process profile information
        profile_response = await self.main_agent.run(f"Profile setup: {profile_input}", self.context)
        
        # Update user profile in context
        self.context.user_profile = profile_input
        
        # Move to plan generation
        self.current_stage = 'plan_generation'
        
        return {
            'stage': self.current_stage,
            'response': f"✅ Profile updated! {profile_response}\n\n🏗️ Now I'll generate personalized plans for you.",
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    async def handle_plan_generation(self) -> Dict[str, Any]:
        """
        Stage 4: Generate personalized meal and workout plans.
        """
        self.current_stage = 'plan_generation'
        print(f"🎯 Stage 4: Plan Generation")
        
        # Generate meal plan
        meal_plan = await self.tools['meal_planner'].run(
            f"Create meal plan for goals: {self.context.goal}", 
            self.context
        )
        
        # Generate workout plan
        workout_plan = await self.tools['workout_recommender'].run(
            f"Create workout plan for goals: {self.context.goal}", 
            self.context
        )
        
        # Update context with plans
        self.context.meal_plan = meal_plan
        self.context.workout_plan = workout_plan
        
        # Move to real-time delivery
        self.current_stage = 'real_time_delivery'
        
        return {
            'stage': self.current_stage,
            'response': f"🍽️ **Meal Plan Generated:**\n{meal_plan}\n\n🏋️ **Workout Plan Generated:**\n{workout_plan}\n\n🚀 Your personalized plans are ready! Let's start your journey.",
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    async def handle_real_time_delivery(self, user_input: str) -> Dict[str, Any]:
        """
        Stage 5: Provide real-time support and guidance.
        """
        self.current_stage = 'real_time_delivery'
        print(f"🎯 Stage 5: Real-Time Delivery")
        
        # Check if user needs specialized help
        if any(keyword in user_input.lower() for keyword in ['injury', 'pain', 'hurt']):
            self.current_stage = 'specialized_help'
            return await self.handle_specialized_help(user_input, 'injury_support')
        
        if any(keyword in user_input.lower() for keyword in ['nutrition', 'diet', 'meal', 'food']):
            self.current_stage = 'specialized_help'
            return await self.handle_specialized_help(user_input, 'nutrition_expert')
        
        # Regular real-time support
        response = await self.main_agent.run(user_input, self.context)
        
        return {
            'stage': self.current_stage,
            'response': response,
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    async def handle_progress_tracking(self, progress_input: str) -> Dict[str, Any]:
        """
        Stage 6: Track and analyze user progress.
        """
        self.current_stage = 'progress_tracking'
        print(f"🎯 Stage 6: Progress Tracking")
        
        # Use ProgressTrackerTool
        progress_result = await self.tools['progress_tracker'].run(progress_input, self.context)
        
        # Update context with progress
        if not hasattr(self.context, 'progress_history'):
            self.context.progress_history = []
        self.context.progress_history.append(progress_result)
        
        return {
            'stage': self.current_stage,
            'response': f"📊 Progress Updated: {progress_result}\n\n🎯 Keep up the great work! Your consistency is key to achieving your goals.",
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    async def handle_specialized_help(self, user_input: str, agent_type: str) -> Dict[str, Any]:
        """
        Stage 7: Provide specialized help through expert agents.
        """
        self.current_stage = 'specialized_help'
        print(f"🎯 Stage 7: Specialized Help - {agent_type}")
        
        # Route to appropriate specialized agent
        if agent_type in self.specialized_agents:
            response = await self.specialized_agents[agent_type].run(user_input, self.context)
        else:
            response = await self.specialized_agents['escalation'].run(user_input, self.context)
        
        return {
            'stage': self.current_stage,
            'response': response,
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    async def handle_ongoing_support(self, user_input: str) -> Dict[str, Any]:
        """
        Stage 8: Provide ongoing support and check-ins.
        """
        self.current_stage = 'ongoing_support'
        print(f"🎯 Stage 8: Ongoing Support")
        
        # Schedule check-ins if needed
        if 'schedule' in user_input.lower() or 'checkin' in user_input.lower():
            checkin_result = await self.tools['checkin_scheduler'].run(user_input, self.context)
            response = f"📅 Check-in scheduled: {checkin_result}"
        else:
            response = await self.main_agent.run(user_input, self.context)
        
        return {
            'stage': self.current_stage,
            'response': response,
            'context': self.context.__dict__,
            'next_actions': self._get_next_actions()
        }
    
    def clear_context(self):
        """
        Clear the current workflow context and reset to initial state.
        """
        print("🔄 Clearing workflow context and resetting to initial state...")
        
        # Reset context
        self.context = UserSessionContext()
        
        # Reset workflow state
        self.current_stage = 'user_starts_chat'
        self.workflow_complete = False
        
        print("✅ Context cleared! Ready for a new session.")
    
    def _get_next_actions(self) -> List[str]:
        """
        Get suggested next actions based on current stage.
        """
        next_actions = {
            'user_starts_chat': ['Collect goals', 'Ask about preferences'],
            'goal_collection': ['Set up profile', 'Gather health info'],
            'profile_setup': ['Generate plans', 'Create meal plan', 'Create workout plan'],
            'plan_generation': ['Start real-time delivery', 'Begin guided support'],
            'real_time_delivery': ['Track progress', 'Get specialized help', 'Schedule check-ins'],
            'progress_tracking': ['Continue real-time delivery', 'Update plans'],
            'specialized_help': ['Return to real-time delivery', 'Get more specialized help'],
            'ongoing_support': ['Schedule next check-in', 'Update goals', 'Continue support']
        }
        return next_actions.get(self.current_stage, ['Continue conversation'])
    
    async def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input based on current workflow stage.
        """
        if self.current_stage == 'user_starts_chat':
            return await self.start_workflow(user_input)
        elif self.current_stage == 'goal_collection':
            return await self.handle_goal_collection(user_input)
        elif self.current_stage == 'profile_setup':
            return await self.handle_profile_setup(user_input)
        elif self.current_stage == 'plan_generation':
            return await self.handle_plan_generation()
        elif self.current_stage == 'real_time_delivery':
            return await self.handle_real_time_delivery(user_input)
        elif self.current_stage == 'progress_tracking':
            return await self.handle_progress_tracking(user_input)
        elif self.current_stage == 'specialized_help':
            return await self.handle_specialized_help(user_input, 'escalation')
        elif self.current_stage == 'ongoing_support':
            return await self.handle_ongoing_support(user_input)
        else:
            # Default to real-time delivery
            return await self.handle_real_time_delivery(user_input)
