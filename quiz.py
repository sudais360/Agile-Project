import easygui

class Question:
    def __init__(self, text, choices, correct_answer, image=None):
        self.text = text
        self.choices = choices
        self.correct_answer = correct_answer
        self.image = image

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.current_question_index = 0

    def get_current_question(self):
        return self.questions[self.current_question_index]

    def check_answer(self, answer):
        return self.get_current_question().correct_answer == answer

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            return True
        return False

