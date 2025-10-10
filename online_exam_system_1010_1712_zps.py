# 代码生成时间: 2025-10-10 17:12:42
# online_exam_system.py

"""
Online Exam System using Pyramid framework.
This includes the following components:
- Exam model: Represents an exam
- Question model: Represents a question in an exam
- Answer model: Represents an answer to a question
- ExamService: Handles business logic for exams
- routes: Defines the URL routes for the application
- main: Sets up the Pyramid application
"""

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import Allow, Authenticated
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

# Define the database connection
DB_URL = 'sqlite:///exam.db'
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define the Exam model
class Exam(Base):
    __tablename__ = 'exams'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    questions = relationship('Question', backref='exam')

    def __init__(self, name):
        self.name = name

# Define the Question model
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey('exams.id'))
    statement = Column(String, nullable=False)
    answers = relationship('Answer', backref='question')

    def __init__(self, exam_id, statement):
        self.exam_id = exam_id
        self.statement = statement

# Define the Answer model
class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    def __init__(self, question_id, answer_text, is_correct):
        self.question_id = question_id
        self.answer_text = answer_text
        self.is_correct = is_correct

# Define the ExamService
class ExamService:
    def create_exam(self, exam_name):
        exam = Exam(exam_name)
        session.add(exam)
        session.commit()
        return exam

    def add_question_to_exam(self, exam_id, question_statement):
        question = Question(exam_id, question_statement)
        session.add(question)
        session.commit()
        return question

    def add_answer_to_question(self, question_id, answer_text, is_correct):
        answer = Answer(question_id, answer_text, is_correct)
        session.add(answer)
        session.commit()
        return answer

# Define the Pyramid views
@view_config(route_name='create_exam', request_method='POST', permission='authenticated')
def create_exam_view(request):
    try:
        data = json.loads(request.body)
        exam_name = data['exam_name']
        exam_service = ExamService()
        exam = exam_service.create_exam(exam_name)
        return Response(json.dumps({'message': 'Exam created successfully', 'exam_id': exam.id}),
                       content_type='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

@view_config(route_name='add_question', request_method='POST', permission='authenticated')
def add_question_view(request):
    try:
        data = json.loads(request.body)
        exam_id = data['exam_id']
        question_statement = data['question_statement']
        exam_service = ExamService()
        question = exam_service.add_question_to_exam(exam_id, question_statement)
        return Response(json.dumps({'message': 'Question added successfully', 'question_id': question.id}),
                       content_type='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

@view_config(route_name='add_answer', request_method='POST', permission='authenticated')
def add_answer_view(request):
    try:
        data = json.loads(request.body)
        question_id = data['question_id']
        answer_text = data['answer_text']
        is_correct = data.get('is_correct', False)
        exam_service = ExamService()
        answer = exam_service.add_answer_to_question(question_id, answer_text, is_correct)
        return Response(json.dumps({'message': 'Answer added successfully', 'answer_id': answer.id}),
                       content_type='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

# Define the Pyramid routes
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('create_exam', '/create_exam')
    config.add_route('add_question', '/add_question')
    config.add_route('add_answer', '/add_answer')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})