from dotenv import load_dotenv
load_dotenv()

from workflow_orchestrator import HealthWellnessWorkflow
import streamlit as st
import asyncio
import json

# Configure page
st.set_page_config(
    page_title="Health & Wellness Planner",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(90deg, #E8F5E8, #F0FFF0);
        border-radius: 10px;
    }
    
    .step-container {
        background: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2E8B57;
    }
    
    .step-title {
        color: #2E8B57;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .progress-bar {
        background: #E9ECEF;
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #2E8B57, #32CD32);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    .response-container {
        background: #FFFFFF;
        border: 1px solid #E9ECEF;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "workflow" not in st.session_state:
    st.session_state.workflow = HealthWellnessWorkflow()

if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {
        "initial": "",
        "goals": "",
        "profile": ""
    }

if "final_response" not in st.session_state:
    st.session_state.final_response = None

if "step_responses" not in st.session_state:
    st.session_state.step_responses = {}

# Header
st.markdown('<div class="main-header">🏥 Health & Wellness Planner</div>', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align: center; color: #888; font-size: 1rem; margin-bottom: 1rem;">'
    'Made with <span style="color: red;">❤️</span> by Rubab'
    '</div>',
    unsafe_allow_html=True
)

# Progress bar
progress_percentage = min((st.session_state.current_step - 1) * 25, 100)
st.markdown(f"""
<div class="progress-bar">
    <div class="progress-fill" style="width: {progress_percentage}%;"></div>
</div>
<p style="text-align: center; margin-top: 0.5rem; color: #666;">
    Step {st.session_state.current_step} of 4 - {progress_percentage}% Complete
</p>
""", unsafe_allow_html=True)

async def process_workflow_step(user_input, step):
    """Process a single step in the workflow"""
    try:
        if step == 1:
            response = await st.session_state.workflow.process_input(user_input)
        elif step == 2:
            # If we're in goal collection stage
            if st.session_state.workflow.current_stage == 'goal_collection':
                response = await st.session_state.workflow.process_input(user_input)
            else:
                # Skip goal collection if goal was already detected
                response = await st.session_state.workflow.process_input(user_input)
        elif step == 3:
            response = await st.session_state.workflow.process_input(user_input)
        elif step == 4:
            response = await st.session_state.workflow.process_input("generate plans")
        
        return response
    except Exception as e:
        return {"error": str(e)}

# Step 1: Initial Health Information
if st.session_state.current_step == 1:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 1: Tell us about your current health situation</div>', unsafe_allow_html=True)
    
    with st.form(key="step1_form"):
        initial_input = st.text_area(
            "Describe your current health situation, what you'd like to improve, or any concerns you have:",
            placeholder="e.g., I am overweight and want to lose weight, I want to get fitter, I have low energy...",
            height=100,
            key="initial_input"
        )
        
        st.markdown("💡 **Tip:** Click the button below to proceed to the next step.")
        
        submitted = st.form_submit_button("Next Step →", type="primary")
        
        if submitted:
            if initial_input.strip():
                st.session_state.user_inputs["initial"] = initial_input
                
                # Process with workflow
                with st.spinner("Processing your information..."):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        response = loop.run_until_complete(process_workflow_step(initial_input, 1))
                        st.session_state.step_responses[1] = response
                        
                        # Move to next appropriate step
                        if st.session_state.workflow.current_stage == 'goal_collection':
                            st.session_state.current_step = 2
                        else:
                            st.session_state.current_step = 3
                        st.rerun()
                    finally:
                        loop.close()
            else:
                st.error("Please enter your health information before proceeding.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Goals (only if needed)
elif st.session_state.current_step == 2:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 2: What are your specific health and wellness goals?</div>', unsafe_allow_html=True)
    
    # Back button outside form
    if st.button("← Back", key="back_step2"):
        st.session_state.current_step = 1
        st.rerun()
    
    with st.form(key="step2_form"):
        goals_input = st.text_area(
            "Please specify your goals in more detail:",
            placeholder="e.g., I want to lose 20 pounds in 3 months, I want to build muscle, I want to improve my cardiovascular health...",
            height=100,
            key="goals_input"
        )
        
        st.markdown("💡 **Tip:** Click the button below to proceed to the next step.")
        
        submitted = st.form_submit_button("Next Step →", type="primary")
        
        if submitted:
            if goals_input.strip():
                st.session_state.user_inputs["goals"] = goals_input
                
                # Process with workflow
                with st.spinner("Analyzing your goals..."):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        response = loop.run_until_complete(process_workflow_step(goals_input, 2))
                        st.session_state.step_responses[2] = response
                        st.session_state.current_step = 3
                        st.rerun()
                    finally:
                        loop.close()
            else:
                st.error("Please enter your goals before proceeding.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Profile Setup
elif st.session_state.current_step == 3:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 3: Tell us about your profile and preferences</div>', unsafe_allow_html=True)
    
    # Back button outside form
    if st.button("← Back", key="back_step3"):
        if 2 in st.session_state.step_responses:
            st.session_state.current_step = 2
        else:
            st.session_state.current_step = 1
        st.rerun()
    
    with st.form(key="step3_form"):
        profile_input = st.text_area(
            "Share information about your fitness level, dietary preferences, any restrictions, and lifestyle:",
            placeholder="e.g., I am a beginner, no dietary restrictions, I work from home, I have 30 minutes per day for exercise...",
            height=100,
            key="profile_input"
        )
        
        st.markdown("💡 **Tip:** Click the button below to proceed to the next step.")
        
        submitted = st.form_submit_button("Next Step →", type="primary")
        
        if submitted:
            if profile_input.strip():
                st.session_state.user_inputs["profile"] = profile_input
                
                # Process with workflow
                with st.spinner("Setting up your profile..."):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        response = loop.run_until_complete(process_workflow_step(profile_input, 3))
                        st.session_state.step_responses[3] = response
                        st.session_state.current_step = 4
                        st.rerun()
                    finally:
                        loop.close()
            else:
                st.error("Please enter your profile information before proceeding.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Step 4: Generate Plans
elif st.session_state.current_step == 4:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 4: Generate Your Personalized Plans</div>', unsafe_allow_html=True)
    
    st.markdown("Ready to generate your personalized meal and workout plans based on your information!")
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("← Back"):
            st.session_state.current_step = 3
            st.rerun()
    
    with col2:
        if st.button("Generate Plans 🚀", type="primary"):
            # Generate final plans
            with st.spinner("Generating your personalized plans... This may take a moment."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    response = loop.run_until_complete(process_workflow_step("", 4))
                    st.session_state.final_response = response
                    st.rerun()
                finally:
                    loop.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Display final response if generated
if st.session_state.final_response:
    st.markdown('<div class="response-container">', unsafe_allow_html=True)
    st.markdown("## 🎉 Your Personalized Health & Wellness Plans")
    
    response = st.session_state.final_response
    
    if isinstance(response, dict):
        if 'response' in response:
            st.markdown(response['response'])
        
        if 'context' in response:
            context = response['context']
            
            # Display meal plan
            if 'meal_plan' in context and context['meal_plan']:
                st.markdown("### 🍽️ Your Meal Plan")
                for i, meal in enumerate(context['meal_plan'], 1):
                    st.markdown(f"**Day {i}:** {meal}")
            
            # Display workout plan
            if 'workout_plan' in context and context['workout_plan']:
                st.markdown("### 🏋️ Your Workout Plan")
                for i, workout in enumerate(context['workout_plan'], 1):
                    st.markdown(f"**Day {i}:** {workout}")
        
        # Show raw response in expander
        with st.expander("View Raw Response (Developer)"):
            st.json(response)
    else:
        st.markdown(str(response))
    
    # Reset button
    if st.button("Start Over", type="secondary"):
        st.session_state.workflow = HealthWellnessWorkflow()
        st.session_state.current_step = 1
        st.session_state.user_inputs = {"initial": "", "goals": "", "profile": ""}
        st.session_state.final_response = None
        st.session_state.step_responses = {}
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Show summary of inputs so far
if st.session_state.current_step > 1:
    with st.expander("Review Your Inputs"):
        if st.session_state.user_inputs["initial"]:
            st.markdown(f"**Initial Information:** {st.session_state.user_inputs['initial']}")
        if st.session_state.user_inputs["goals"]:
            st.markdown(f"**Goals:** {st.session_state.user_inputs['goals']}")
        if st.session_state.user_inputs["profile"]:
            st.markdown(f"**Profile:** {st.session_state.user_inputs['profile']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
    💡 <strong>Tip:</strong> Be as detailed as possible in your responses for the best personalized recommendations!
    <br>
    🔒 Your health information is kept private and secure.
</div>
""", unsafe_allow_html=True)
