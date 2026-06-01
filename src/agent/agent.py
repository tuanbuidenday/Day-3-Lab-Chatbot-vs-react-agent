import os
import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger

class ReActAgent:
    """
    SKELETON: A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Students should implement the core loop logic and tool execution.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        Implement the system prompt that instructs the agent to follow ReAct.
        Includes:
        1. Available tools and their descriptions.
        2. Format instructions: Thought, Action, Observation.
        """
        tool_descriptions = "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])
        return f"""You are an intelligent assistant. You have access to the following tools:
{tool_descriptions}

You MUST follow the ReAct framework. Do not output anything other than this exact format:
Thought: your line of reasoning.
Action: tool_name(arguments)
Observation: result of the tool call.
... (repeat Thought/Action/Observation if needed)
Final Answer: your final response.

Always start with a Thought. If you have enough information, output a Final Answer.
"""

    def run(self, user_input: str) -> str:
        """
        Implement the ReAct loop logic.
        1. Generate Thought + Action or Final Answer.
        2. Parse Action and execute Tool if found.
        3. Append Observation to prompt and repeat until Final Answer or max_steps is reached.
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        
        current_prompt = f"User Input: {user_input}\n"
        steps = 0
        final_answer = None

        while steps < self.max_steps:
            # Generate LLM response
            result = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            content = result.get("content", "")
            
            logger.log_event("AGENT_STEP", {"step": steps + 1, "llm_output": content})
            
            # Check for Action pattern: Action: tool_name(arguments)
            action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((.*)\)", content)
            # Check for Final Answer pattern: Final Answer: final response text
            final_answer_match = re.search(r"Final Answer:\s*(.*)", content, re.DOTALL)
            
            if action_match:
                tool_name = action_match.group(1).strip()
                tool_args = action_match.group(2).strip()
                
                # Strip leading/trailing quotes if they wrap the whole argument
                if (tool_args.startswith('"') and tool_args.endswith('"')) or (tool_args.startswith("'") and tool_args.endswith("'")):
                    tool_args = tool_args[1:-1]
                
                logger.log_event("TOOL_CALL", {"tool": tool_name, "args": tool_args})
                
                # Execute tool
                observation = self._execute_tool(tool_name, tool_args)
                logger.log_event("TOOL_OBSERVATION", {"tool": tool_name, "observation": observation})
                
                # Append execution details to history and current prompt
                current_prompt += f"{content}\nObservation: {observation}\n"
            elif final_answer_match:
                final_answer = final_answer_match.group(1).strip()
                break
            else:
                # Fallback: if no structured ReAct format but has "Final Answer" text
                if "Final Answer:" in content:
                    final_answer = content.split("Final Answer:")[-1].strip()
                else:
                    final_answer = content.strip()
                break
            
            steps += 1
            
        if final_answer is None:
            final_answer = "Error: Exceeded max steps without finding a final answer."
            logger.log_event("AGENT_TIMEOUT", {"steps": steps})
            
        logger.log_event("AGENT_END", {"steps": steps, "final_answer": final_answer})
        return final_answer

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Helper method to execute tools by name.
        Supports both static mocking and callable dynamic execution.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                if 'func' in tool and callable(tool['func']):
                    try:
                        return str(tool['func'](args))
                    except Exception as e:
                        return f"Error executing tool {tool_name}: {str(e)}"
                return f"Result of {tool_name}"
        return f"Tool {tool_name} not found."
