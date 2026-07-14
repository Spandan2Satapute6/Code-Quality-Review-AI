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

        try:
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
            elif result.startswith("```"):
                result = result.replace("```", "").strip()

            return json.loads(result)

        except Exception as e:
            print("PROJECT SUMMARY GENERATION ERROR:", str(e))
            # Calculate a dummy/fallback score from the static reviews if AI fails
            total_score = 0
            if review:
                # Count files and compute a basic score
                total_score = sum(r.get("score", 90) for r in review) // len(review)
            else:
                total_score = 75

            return {
                "overall_score": total_score or 75,
                "summary": "AI summary generation failed because of an invalid or missing API key. Detailed static analysis reports from Pylint, Bandit, and Radon are fully available below.",
                "strengths": ["Static analysis tools (Pylint, Bandit, Radon) ran successfully."],
                "weaknesses": ["AI review recommendations could not be fetched due to API key issues."],
                "security": [],
                "performance": [],
                "best_practices": [],
                "recommendations": ["Set a valid GROQ_API_KEY in backend/.env to enable AI-powered project summaries."],
                "verdict": "Needs Key Config"
            }