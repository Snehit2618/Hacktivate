import google.generativeai as genai
import asyncio
import re

# Configure the API key
genai.configure(api_key="AIzaSyDkKn6vu2Qgx87jfsrevovbU8y7i0qdOy0")

# =========================
# Chatbot Functions
# =========================

async def generate_question(skill):
    """Generates a technical interview question for a given skill."""
    prompt = f"Generate a technical interview question for a candidate proficient in {skill}. Only provide the question."
    model = genai.GenerativeModel("gemini-pro")
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating question: {str(e)}"


async def evaluate_answer(candidate_answer, question):
    """Evaluates the candidate's answer and returns a score out of 5."""
    prompt = f"Evaluate the following answer: '{candidate_answer}' to the question: '{question}'. Provide ONLY a numerical score out of 5, without explanation."
    model = genai.GenerativeModel("gemini-pro")
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        score = extract_score(response.text)
        return score
    except Exception as e:
        return 0  # Default score if there's an issue


def extract_score(response_text):
    """Extracts a numerical score from the response text."""
    match = re.search(r"\b([0-5])\b", response_text)  # Matches numbers 0-5
    return int(match.group(1)) if match else 0


# =========================
# Interview Process
# =========================

async def start_interview(skills):
    """Runs an interview session with 5 questions, evaluating each answer."""
    total_score = 0
    num_questions = 5
    questions_and_scores = []

    for i in range(num_questions):
        skill = skills[i % len(skills)]  # Rotate through skills
        question = await generate_question(skill)
        
        # Get candidate answer
        print(f"\nQuestion {i+1}: {question}")
        candidate_answer = input("Your answer: ")
        
        score = await evaluate_answer(candidate_answer, question)
        total_score += score

        questions_and_scores.append({
            "question": question,
            "score": score
        })

    return {
        "questions": questions_and_scores,
        "total_score": total_score,
        "max_score": num_questions * 5
    }

# =========================
# Main Function for CLI
# =========================

def main():
    # Get skills input from user
    skills_input = input("Enter skills (comma-separated): ")
    skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
    
    if not skills:
        print("No skills provided. Please enter at least one skill.")
        return
    
    # Run the interview process asynchronously
    interview_results = asyncio.run(start_interview(skills))

    # Print interview results
    print("\nInterview Summary:")
    for i, item in enumerate(interview_results['questions'], 1):
        print(f"Question {i}: {item['question']}")
        print(f"Score: {item['score']}/5")
    
    print(f"\nTotal Score: {interview_results['total_score']} out of {interview_results['max_score']}")

if __name__ == "__main__":
    main()
