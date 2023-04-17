#!/usr/bin/env python
# coding: utf-8

import asyncio
import configparser
from graph import Graph
import os
import openai
from keys import *
from bs4 import BeautifulSoup
import time

openai.api_key = OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"
PREFACE = f"I am a teaching assistant and a student in my course has posed the following question. What should the answer be? Question: "
EMAIL_ID = "varun15@illinois.edu"
QUESTION_ID_TO_EMAIL_COMPLETED_FILE = "question_id_to_emails_completed.txt"


def read_previous_questions_answered():
    Questions_to_emails_completed = set()
    if os.path.exists(QUESTION_ID_TO_EMAIL_COMPLETED_FILE):
        with open(QUESTION_ID_TO_EMAIL_COMPLETED_FILE, "r") as f:
            lines = f.readlines()
            for line in lines: 
                question_id, email_id = line.split(",")
                Questions_to_emails_completed.add((question_id, email_id))
    return Questions_to_emails_completed

async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user is not None:
        print('Hello,', user.display_name)
        print('Email:', user.mail or user.user_principal_name, '\n')

async def retrieve_emails(graph: Graph):
    message_page = await graph.get_inbox()
    if message_page is not None and message_page.value is not None:
        return message_page.value

async def send_mail(graph: Graph, subject, content, email=None):

    if email is None:
        if  user is not None:
            user = await graph.get_user()
            email = user.mail or user.user_principal_name
    print(subject, content, email)
    await graph.send_mail(subject, content, email)
#         await graph.send_mail('Testing Microsoft Graph', 'Hello world!', "ssehgal4@illinois.edu" or '')
    print('Mail sent.\n')


def api_call(preface, question, model):
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": preface + question}
        ]
    )
    return completion.choices[0].message.content

def extract_relevant_and_uncompleted_questions(emailObjects, Questions_to_emails_completed):
    filteredQuestionIdToContent = {}
    for msg in emailObjects:
        bodyContent = msg._body._content
        parsed_html = BeautifulSoup(bodyContent, "html.parser")
        
        heading = parsed_html.find("h1").text
        if "asked a question in Advanced Information Retrieval" in heading:
            if (msg._id, EMAIL_ID) not in  Questions_to_emails_completed:
                question = extract_question(parsed_html)
                filteredQuestionIdToContent[msg._id] = [heading, question]
    return filteredQuestionIdToContent

def extract_question(parsed_html):
    start = parsed_html.find("p", attrs={'class':'markdown_tester'})
    question = f"{start.text}\n"
    for tr in start.find_next_siblings("p"):
        question += tr.text
        images = tr.find_all("img")
        if images:
            question += images[0].attrs['src'] + "\n"
    return question

def formulate_email_content(questionContent, answer):
    subject = f"QuickAns Assitant replies to '{questionContent[0]}'"
    emailContent = f"Hi there! I am QuickAns assistant and I am here to help you with questions on CampusWire.\n\n"
    emailContent += f"The following question was posed on CampusWire: \n\n``{questionContent[1]}``\n\n Here is a baseline response / some helpful tips to answer the question: \n\n ``{answer}`` \n\n" 
    emailContent += "Thanks, Hope you have a great day on Campus (wire)!\n QuickAns Assistant"
    return subject, emailContent

async def main():
    print('Welcome to QuickAns!\n')
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)
    await greet_user(graph)
    QuestionsToEmailsCompleted = read_previous_questions_answered()
    emailObjects = await retrieve_emails(graph)
    filteredQuestionIdToContent = extract_relevant_and_uncompleted_questions(emailObjects, QuestionsToEmailsCompleted)

    for questionId, questionContent in filteredQuestionIdToContent.items():
        answer = api_call(PREFACE, questionContent[1], MODEL)
        subject, emailContent = formulate_email_content(questionContent, answer)
        await send_mail(graph, subject, emailContent, EMAIL_ID)
        with open(QUESTION_ID_TO_EMAIL_COMPLETED_FILE, "a") as f:
            f.write(f"{questionId},{EMAIL_ID}\n")
        break
        time.sleep(20)

# Run main
asyncio.run(main())