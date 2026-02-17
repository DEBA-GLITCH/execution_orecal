import json
import re
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME


client = Groq(api_key=GROQ_API_KEY)


class AutonomousCoder:

    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def _clean_markdown(self, text: str):
        text = text.replace("```json", "").replace("```", "")
        return text.strip()

    def _extract_json_block(self, text: str):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group()
        return None

    def generate_file_code(
        self,
        project_description: str,
        file_path: str,
        additional_context: str = ""
    ):
        """
        Resilient file generation with multi-level fallback.
        """

        strict_prompt = f"""
You are a senior software engineer.

Return ONLY valid JSON.

Format:
{{
  "file_path": "{file_path}",
  "content": "FULL file content here"
}}

No markdown. No explanation.

Project:
{project_description}

Target File:
{file_path}
"""

        raw_code_prompt = f"""
You are a senior software engineer.

Generate FULL production-ready code for this file.

Return ONLY the raw file content.
No markdown. No explanation.

Project:
{project_description}

Target File:
{file_path}
"""

        for attempt in range(self.max_retries):

            try:
                # First attempt: strict JSON
                res = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": strict_prompt}],
                    temperature=0.2,
                    max_tokens=2000
                )

                raw = self._clean_markdown(
                    res.choices[0].message.content
                )

                # Try direct JSON parse
                try:
                    parsed = json.loads(raw)
                    if "content" in parsed:
                        return parsed["content"]
                except:
                    pass

                # Try extracting JSON block
                extracted = self._extract_json_block(raw)
                if extracted:
                    try:
                        parsed = json.loads(extracted)
                        if "content" in parsed:
                            return parsed["content"]
                    except:
                        pass

            except Exception:
                pass

        # Fallback strategy: raw code mode
        try:
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": raw_code_prompt}],
                temperature=0.2,
                max_tokens=2000
            )

            raw_code = self._clean_markdown(
                res.choices[0].message.content
            )

            return raw_code

        except Exception:
            raise Exception("AutonomousCoder failed after all fallback strategies.")
