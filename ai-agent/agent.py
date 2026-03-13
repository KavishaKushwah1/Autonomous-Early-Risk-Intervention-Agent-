import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

# 1. Load the secret API key
load_dotenv()

# 2. Initialize the Gemini brain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2, # Lowered to 0.2 so it acts more like a logical teacher
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 3. Define the Agent's Memory (State)
class AgentState(TypedDict):
    student_data: str
    risk_analysis: str

# 4. Define the Agent's Job (Node)
def analyze_student(state: AgentState):
    print("🤖 Agent is analyzing the student data...")
    
    # We give the AI a specific instruction and pass in the student data
    prompt = f"""
    You are an expert Education Intervention Agent. 
    Review the following student data and provide a brief 2-sentence analysis 
    on whether this student is at risk and what intervention is needed.
    
    Student Data: {state['student_data']}
    """
    
    # The AI thinks and generates a response
    response = llm.invoke(prompt)
    
    # Save the response back to the agent's memory
    return {"risk_analysis": response.content}

# 5. Build the Flowchart (Graph)
workflow = StateGraph(AgentState)

# Add our node to the graph
workflow.add_node("analyze", analyze_student)

# Connect the flow: START -> analyze -> END
workflow.add_edge(START, "analyze")
workflow.add_edge("analyze", END)

# Compile the graph into a working app
ai_app = workflow.compile()

# 6. Test the Agent with some fake data!
if __name__ == "__main__":
    print("Starting the Early Risk Intervention Agent...\n")
    
    # Fake data for our test
    test_input = {
        "student_data": "Sarah is in 8th grade. Her recent math score was a 55% (a drop from her usual 85%). Her behavioral notes say she has been sleeping in class and seems disconnected."
    }
    
    # Run the graph!
    result = ai_app.invoke(test_input)
    
    print("\n--- AGENT ANALYSIS ---")
    print(result["risk_analysis"])
    print("----------------------")