import time

class QuestionBank:
    def __init__(self):
        self.pending_questions = []
        self.conversation_context = ""
    
    def add_questions(self, questions, context):
        for q in questions:
            self.pending_questions.append({
                'question': q,
                'context': context,
                'timestamp': time.time()
            })
    
    def get_relevant_questions(self, current_topic):
        # Placeholder: Return all for now; enhance with topic relevance logic
        return [q for q in self.pending_questions if self.still_relevant(q, current_topic)]
    
    def still_relevant(self, question_entry, current_topic):
        # Placeholder: Always true; implement topic drift detection
        return True
    
    def offer_return_to_questions(self):
        if self.pending_questions and self.conversation_has_drifted():
            return "I'm noticing we've moved in a different direction. I still have some questions from earlier if you'd like to return to them."
        return None
    
    def conversation_has_drifted(self):
        # Placeholder: Always returns True for demo; implement real drift logic
        return True
