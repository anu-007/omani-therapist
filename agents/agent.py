from google.adk.agents import SequentialAgent
from agents.callbacks.after_agent import modify_output_after_agent
from agents.sub_agents.therapist.agent import primary_therapist_agent
from agents.sub_agents.validation.agent import fallback_therapist_agent

# root agent
root_agent = SequentialAgent(
    name = "omani_therapist_pipeline",
    description = "Process the user input using sub agents",
    sub_agents = [primary_therapist_agent, fallback_therapist_agent],
)