import time
import random

# Interview questions
questions = [
    "Tell me about yourself.",
    "Why do you want this job?",
    "What are your strengths and weaknesses?",
    "Describe a challenge you faced and how you overcame it.",
    "Where do you see yourself in 5 years?",
    "Why should we hire you?",
]

# Feedback templates
positive_feedback = [
    "Interesting perspective!",
    "Thanks for the detailed response.",
    "Good answer—well structured.",
    "Nice! That shows insight.",
]

neutral_feedback = [
    "Alright, let's move on.",
    "Okay, noted.",
    "Got it.",
    "Thanks, next question.",
]

def ask_question(question_num, question):
    print(f"\nQuestion {question_num}: {question}")
    start = time.time()
    answer = input("Your answer: ")
    end = time.time()

    duration = end - start
    feedback = random.choice(positive_feedback + neutral_feedback)
    
    print(f"\n[Interviewer]: {feedback}")
    print(f"(Response time: {duration:.2f} seconds)")
    
    return {
        "question": question,
        "answer": answer,
        "time": duration,
        "feedback": feedback
    }

def main():
    print("👔 Welcome to the Interview Simulator!\n")
    name = input("What's your name? ")
    print(f"\nHi {name}, let's begin your mock interview.")

    responses = []
    
    for i, question in enumerate(questions, 1):
        responses.append(ask_question(i, question))
    
    print("\n✅ Interview complete!")
    print(f"Thanks for participating, {name}. Here's a quick summary:\n")
    
    for i, r in enumerate(responses, 1):
        print(f"{i}. {r['question']}")
        print(f"   Your answer: {r['answer']}")
        print(f"   Time: {r['time']:.2f}s")
        print(f"   Feedback: {r['feedback']}")
        print()

if __name__ == "__main__":
    main()
