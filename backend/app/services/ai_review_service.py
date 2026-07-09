import os
import json
from groq import Groq


class AIReviewService:

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    @staticmethod
    def review_file(file):

        print("\n==============================")
        print("Sending to AI:", file["filename"])
        print("==============================")

        prompt = f"""
You are a senior software engineer and code reviewer.

Review the following source code.

Filename:
{file["filename"]}

Code:
{file["content"]}

IMPORTANT RULES:
- Return ONLY valid JSON.
- Do NOT write explanations.
- Do NOT write markdown.
- Do NOT use ```json.
- Do NOT write any text before or after the JSON.

Return exactly in this format:

{{
    "score": 90,
    "issues": [
        "Issue 1",
        "Issue 2"
    ],
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2"
    ]
}}
"""

        try:

            response = AIReviewService.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=1024
            )

            result = response.choices[0].message.content.strip()

            print("\n========== RAW AI RESPONSE ==========")
            print(result)
            print("=====================================\n")

            # Remove markdown if the model still returns it
            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()
            elif result.startswith("```"):
                result = result.replace("```", "").strip()

            return json.loads(result)

        except Exception as e:

            print("AI ERROR:", str(e))

            return {
                "score": 0,
                "issues": [str(e)],
                "suggestions": [
                    "AI review failed."
                ]
            }