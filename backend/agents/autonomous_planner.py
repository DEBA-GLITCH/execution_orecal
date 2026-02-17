import json
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME


client = Groq(api_key=GROQ_API_KEY)


class AutonomousPlanner:

    def __init__(self):
        pass

    def generate_plan(self, user_input: str):
        """
        Generates structured execution plan.
        Automatically adapts to complexity.
        """

        prompt = f"""
You are an autonomous software architect.

Analyze the user's request and return ONLY valid JSON.

Rules:
- Detect complexity: simple | medium | complex
- If simple (like single script), no phases required.
- If medium/complex, create structured phases.
- Always return file_structure.
- No markdown.
- No explanation.

Return JSON in this exact format:

{{
  "project_name": "",
  "complexity": "simple | medium | complex",
  "phases": [
      {{
        "phase_name": "",
        "description": ""
      }}
  ],
  "file_structure": [
      "path/to/file.py"
  ],
  "requires_features_input": true/false,
  "requires_tech_stack_input": true/false
}}

User Request:
{user_input}
"""

        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800
        )

        content = res.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except Exception:
            raise Exception("Planner did not return valid JSON.")
