
Health & Wellness Agent 🏥
A comprehensive AI-powered health and wellness planning assistant that provides personalized meal plans, workout recommendations, and ongoing support using Google's Gemini AI.

🌟 Features
Intelligent Goal Analysis: Analyzes user health goals and extracts structured data
Personalized Meal Planning: Generates 7-day meal plans based on dietary preferences
Custom Workout Recommendations: Creates workout plans tailored to fitness level and goals
Multi-Agent Architecture: Specialized agents for different health domains
Real-time Support: Interactive chat interface for ongoing assistance
Progress Tracking: Monitor and track health journey progress
Streamlit Web Interface: User-friendly web application
CLI Interface: Command-line interface for quick interactions
🏗️ Architecture
Core Components
Workflow Orchestrator (workflow_orchestrator.py)

Manages the complete health and wellness workflow
Handles 8 distinct stages from initial chat to ongoing support
Coordinates between different agents and tools
Agents (agents/)

WellnessPlannerAgent: Main planning assistant
InjurySupportAgent: Handles injury-specific recommendations
NutritionExpertAgent: Complex dietary needs and nutrition advice
EscalationAgent: Escalation to human coaches
Tools (tools/)

GoalAnalyzerTool: Extracts structured goal data from user input
MealPlannerTool: Generates personalized meal plans
WorkoutRecommenderTool: Creates custom workout routines
ProgressTrackerTool: Tracks user progress
CheckinSchedulerTool: Schedules recurring check-ins
Context Management (context.py)

Maintains user session state and preferences
Stores goals, profiles, and progress history
Workflow Stages
User Starts Chat: Initial interaction and intent detection
Goal Collection: Gather and analyze health/wellness goals
Profile Setup: Collect user preferences and constraints
Plan Generation: Create personalized meal and workout plans
Real-Time Delivery: Provide ongoing support and guidance
Progress Tracking: Monitor and analyze user progress
Specialized Help: Route to expert agents when needed
Ongoing Support: Continuous assistance and check-ins
🚀 Quick Start
Prerequisites
Python 3.8 or higher
Google API key for Gemini AI
Installation
Clone the repository:

git clone <repository-url>
cd health_wellness_agent
Install dependencies:

pip install -r requirements.txt
Set up environment variables: Create a .env file in the project root:

echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
Running the Application
Web Interface (Streamlit)
streamlit run app.py
Open your browser to http://localhost:8501

Command Line Interface
python main.py
Testing
# Run workflow tests
python test_workflow.py

# Run CLI tests
python test_cli.py

# Run full workflow test
python test_full_workflow.py

# Run with pytest
pytest
📋 Usage Examples
Basic Workflow
Start with your health situation:

"I am overweight and want to get in better shape"
Specify your goals (if needed):

"I want to lose 20 pounds in 3 months"
Share your profile:

"I'm a beginner, work from home, have 30 minutes per day for exercise, no dietary restrictions"
Generate plans: The system will create personalized meal and workout plans

Available Commands (CLI)
quit or exit: Exit the application
clear: Reset session and start fresh
help: Show available commands
status: Check current workflow stage
🛠️ Configuration
Environment Variables
GEMINI_API_KEY: Required for Gemini AI integration
Customization
You can customize the behavior by modifying:

Agent responses: Edit agent classes in agents/
Tool functionality: Modify tool classes in tools/
Workflow stages: Adjust the workflow in workflow_orchestrator.py
UI appearance: Customize Streamlit interface in app.py
📁 Project Structure
health_wellness_agent/
├── agents/                    # AI agents for different domains
│   ├── __init__.py
│   ├── agent.py              # Main wellness planner agent
│   ├── escalation_agent.py   # Human coach escalation
│   ├── injury_support_agent.py # Injury-specific support
│   └── nutrition_expert_agent.py # Nutrition expertise
├── tools/                     # Specialized tools
│   ├── goal_analyzer.py      # Goal extraction and analysis
│   ├── meal_planner.py       # Meal plan generation
│   ├── scheduler.py          # Check-in scheduling
│   ├── tracker.py            # Progress tracking
│   └── workout_recommender.py # Workout plan creation
├── utils/                     # Utility functions
│   └── streaming.py          # Conversation streaming
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── agent_base.py            # Base agent class
├── app.py                   # Streamlit web interface
├── context.py               # Session context management
├── guardrails.py            # Input validation
├── hooks.py                 # Logging and monitoring
├── main.py                  # CLI interface
├── requirements.txt         # Python dependencies
├── tool_base.py            # Base tool class
├── workflow_orchestrator.py # Main workflow management
└── test_*.py               # Test files
🧪 Testing
The project includes several test files:

test_workflow.py: Tests the complete workflow stages
test_cli.py: Tests the command-line interface
test_full_workflow.py: End-to-end workflow testing
test_mock_workflow.py: Mock testing scenarios
Run tests using:

python test_workflow.py
# or
pytest
🔒 Security & Privacy
API Keys: Store in environment variables, never commit to version control
User Data: All health information is processed locally and in session context
Data Validation: Input validation using Pydantic models
Error Handling: Comprehensive error handling throughout the application
🚧 Development
Adding New Agents
Create a new agent class inheriting from Agent:

from agent_base import Agent

class MyCustomAgent(Agent):
    def __init__(self):
        super().__init__(name="MyAgent", description="My custom agent")
    
    async def run(self, input, context):
       
        return "Agent response"
Register the agent in workflow_orchestrator.py

Adding New Tools
Create a new tool class inheriting from Tool:

from tool_base import Tool

class MyCustomTool(Tool):
    def __init__(self):
        super().__init__(name="MyTool", description="My custom tool")
    
    async def run(self, input, context):
        
        return "Tool result"
Register the tool in the workflow orchestrator

Code Style
Follow PEP 8 guidelines
Use type hints where appropriate
Add docstrings to classes and methods
Handle exceptions gracefully
📚 Dependencies
Core Dependencies
python-dotenv: Environment variable management
pydantic: Data validation and settings management
google-generativeai: Google Gemini AI integration
streamlit: Web interface framework
Development Dependencies
pytest: Testing framework
pytest-asyncio: Async testing support
🤝 Contributing
Fork the repository
Create a feature branch: git checkout -b feature/my-feature
Make your changes and add tests
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin feature/my-feature
Submit a pull request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
For support and questions:

Check the documentation in this README
Review the test files for usage examples
Open an issue on the repository
🔮 Future Enhancements
 Integration with fitness trackers and health apps
 Advanced progress analytics and visualizations
 Social features and community support
 Mobile app development
 Multi-language support
 Integration with nutrition databases
 AI-powered meal photo analysis
 Wearable device integration
Note: This application uses AI to provide health and wellness suggestions. Always consult with healthcare professionals for medical advice.
