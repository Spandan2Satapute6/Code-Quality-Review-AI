import os
import json
from groq import Groq


class ProjectSummaryService:

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    @staticmethod
    def generate_summary(review):

        prompt = f"""
You are a senior software architect.

Based on the following code review results, generate an overall project assessment.

Review Results:
{json.dumps(review)}

Return ONLY valid JSON in this format:

{{
    "overall_score": 90,
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "security": [],
    "performance": [],
    "best_practices": [],
    "recommendations": [],
    "verdict": ""
}}
"""

        response = ProjectSummaryService.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        if result.startswith("```json"):
            result = result.replace("```json", "").replace("```", "").strip()

        return json.loads(result)