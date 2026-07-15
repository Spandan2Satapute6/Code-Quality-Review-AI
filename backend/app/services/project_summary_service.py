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
You are a Principal Software Architect, Senior Code Reviewer, Security Engineer, and Performance Expert.

Analyze the following complete project review data and generate an executive-level software quality report.

Review Data:
{json.dumps(review)}

Evaluate the project on the following:

1. Overall Code Quality
2. Readability
3. Maintainability
4. Security
5. Performance
6. Scalability
7. Architecture
8. Error Handling
9. Best Practices
10. Documentation

IMPORTANT RULES

- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT use ```json.
- Do NOT explain outside JSON.

Return exactly in this format:

{{
    "overall_score": 90,
    "quality_grade": "A",
    "severity": "Low",

    "summary": "",

    "strengths": [],

    "weaknesses": [],

    "security": [],

    "performance": [],

    "maintainability": [],

    "architecture": [],

    "best_practices": [],

    "recommendations": [],

    "future_improvements": [],

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
                temperature=0,
                max_tokens=1500
            )

            result = response.choices[0].message.content.strip()

            print("\n========== PROJECT SUMMARY ==========")
            print(result)
            print("=====================================\n")

            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()

            elif result.startswith("```"):
                result = result.replace("```", "").strip()

            return json.loads(result)

        except Exception as e:

            print("PROJECT SUMMARY ERROR:", str(e))

            total_score = 75

            if review:
                total_score = round(
                    sum(r.get("score", 75) for r in review) / len(review)
                )

            return {

                "overall_score": total_score,

                "quality_grade": "B",

                "severity": "Unknown",

                "summary": "AI project summary could not be generated. Static analysis results are available.",

                "strengths": [
                    "Project scanned successfully.",
                    "Static analysis completed."
                ],

                "weaknesses": [
                    "AI summary unavailable."
                ],

                "security": [],

                "performance": [],

                "maintainability": [],

                "architecture": [],

                "best_practices": [],

                "recommendations": [
                    "Configure a valid GROQ_API_KEY."
                ],

                "future_improvements": [],

                "verdict": "Needs AI Review"
            }