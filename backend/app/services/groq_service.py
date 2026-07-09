import os
import json
from groq import Groq


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class AIReviewService:

    @staticmethod
    def review_code(filename, content):

        prompt = f"""
You are an expert software code reviewer.

Review the following source code.

Filename:
{filename}

Code:
{content}

Return ONLY valid JSON in this format:

{{
    "score": 95,
    "issues": [
        "...",
        "..."
    ],
    "suggestions": [
        "...",
        "..."
    ]
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1024
        )

        result = response.choices[0].message.content

        try:
            return json.loads(result)

        except Exception:
            return {
                "score": 70,
                "issues": [
                    "Unable to parse AI response."
                ],
                "suggestions": [
                    result
                ]
            }