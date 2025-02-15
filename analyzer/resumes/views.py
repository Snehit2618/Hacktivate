
from django.http import JsonResponse
from django.shortcuts import render
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
# Django Views
# =========================

def interview_view(request):
    """Handles the interview process by generating and scoring questions."""
    if request.method == 'POST':
        candidate_name = request.POST.get('candidate_name', 'Candidate')
        skills_input = request.POST.get('skills', '')

        skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]

        if not skills:
            return JsonResponse({'error': 'No skills provided. Please enter at least one skill.'}, status=400)

        # Run the interview process asynchronously
        questions_and_scores = asyncio.run(start_interview(skills))

        return JsonResponse(questions_and_scores, safe=False)

    return render(request, 'interview.html')


async def start_interview(skills):
    """Runs an interview session with 5 questions, evaluating each answer."""
    total_score = 0
    num_questions = 5
    questions_and_scores = []

    for i in range(num_questions):
        skill = skills[i % len(skills)]  # Rotate through skills
        question = await generate_question(skill)

        # Placeholder for actual user input handling
        candidate_answer = "Simulated answer"  # Replace this with user input in production

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


async def evaluate_answer_view(request):
    """Evaluates a candidate's answer to a specific question."""
    if request.method == 'POST':
        candidate_answer = request.POST.get('answer', '')
        question = request.POST.get('question', '')

        if not candidate_answer or not question:
            return JsonResponse({'error': 'Both question and answer are required.'}, status=400)

        score = await evaluate_answer(candidate_answer, question)

        return JsonResponse({"score": score})






