import time
import argparse
import json
import os
from tqdm import tqdm
import logging
from openai import OpenAI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_API_RETRY = 5
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

def get_res(inst: str, constraint: str,api_key: str, max_tokens: int = 4096):
    if constraint == "Content_open":
        user_prompt = f"""
        You are an Instruction Rewriting Expert. You need to rewrite #Given Instruction# based on #Rewriting Requirement#, in order to obtain a #Rewritten Instruction#. 
        Basically, #Rewritten Instruction# should adhere to the following guidelines:
        1. Your rewriting cannot omit the non-text parts such as the table and code in #Given Instruction#.
        2. #Rewritten Instruction# must be reasonable and must be understood and responded by humans.
        3. You should try your best not to make the #Rewritten Instruction# become verbose. #Rewritten Instruction# can only add 10 to 20 words into #Given Instruction#.
        #Given Instruction#
        {inst}
        #Rewriting Requirement#
        Please add one proper content constraint to the #Given Instruction#. The content constraints include but are not limited to:
        1. Add a Subtask or Another Related Question.
        2. Narrow Down the Topic: Instead of a general theme or topic, provide a more specific subset.
        3. Set a Higher Standard: Raise the bar for what's considered acceptable or successful.
        4. Limit Resources: Restrict the number or type of resources someone can use.
        5. Introduce Specific Criteria: Mandate particular components or features that must be included.
        6. Specifying Sequence: Dictate the order in which certain steps or actions should be taken.
        Please output in JSON format with the fields 'modified_instruction' for the modified instruction and 'added_constraint' for the added constraint.
        """
    elif constraint == "Content_language":
        user_prompt = f"""
        You are an Instruction Rewriting Expert. You need to rewrite #Given Instruction# based on #Rewriting Requirement#, in order to obtain a #Rewritten Instruction#. 
        Basically, #Rewritten Instruction# should adhere to the following guidelines:
        1. Your rewriting cannot omit the non-text parts such as the table and code in #Given Instruction#.
        2. #Rewritten Instruction# must be reasonable and must be understood and responded to by humans.
        3. You should try your best not to make the #Rewritten Instruction# become verbose. #Rewritten Instruction# can only add 10 to 20 words into #Given Instruction#.
        #Given Instruction#
        {inst}
        #Rewriting Requirement#
        Please add one proper content constraint to the #Given Instruction#. The content constraints include but are not limited to:
        1. Specify Language Complexity: Determine whether the text should use simple, intermediate, or advanced language.
        2. Control Output Length: Set limits on the text's length, such as maximum word count or number of paragraphs.
        3. Restrict Vocabulary: Include or exclude specific words or phrases, or limit the range of vocabulary.
        4. Mandate Structure: Require a specific format, such as headings, bullet points, or a particular narrative style.
        Please output in JSON format with the fields 'modified_instruction' for the modified instruction and 'added_constraint' for the added constraint.
        """
    elif constraint == "Situation_suggest":
        user_prompt = f"""
        You are an Instruction Rewriting Expert. You need to rewrite #Given Instruction# based on #Rewriting Requirement#, in order to obtain a #Rewritten Instruction#. 
        Basically, #Rewritten Instruction# should adhere to the following guidelines:
        1. Your rewriting cannot omit the non-text parts such as the table and code in #Given Instruction#.
        2. #Rewritten Instruction# must be reasonable and must be understood and responded to by humans.
        3. You should try your best not to make the #Rewritten Instruction# become verbose. #Rewritten Instruction# can only add 10 to 20 words into #Given Instruction#.
        #Given Instruction#
        {inst}
        #Rewriting Requirement#
        Please add one proper situation constraint to the #Given Instruction#. The content constraints include but are not limited to:
        1. Define the Context: Specify a particular situation or environment that the suggestions should be relevant to.
        2. Introduce a Specific Problem: Focus on addressing a distinct problem or challenge that needs suggestions.
        3. Impose Urgency: Include a time constraint or urgency for when the suggestions should be applied.
        4. Limit Options: Restrict the scope of potential suggestions to a narrower set of choices.
        5. Add Dependencies: Require that suggestions consider certain conditions or prerequisites.
        6. Prioritize Outcomes: Highlight specific outcomes or goals that the suggestions should aim to achieve.
        Please output in JSON format with the fields 'modified_instruction' for the modified instruction and 'added_constraint' for the added constraint.
        """
    elif constraint == "Situation_role":
        user_prompt = f"""
        You are an Instruction Rewriting Expert. You need to rewrite #Given Instruction# based on #Rewriting Requirement#, in order to obtain a #Rewritten Instruction#. 
        Basically, #Rewritten Instruction# should adhere to the following guidelines:
        1. Your rewriting cannot omit the non-text parts such as the table and code in #Given Instruction#.
        2. #Rewritten Instruction# must be reasonable and must be understood and responded to by humans.
        3. You should try your best not to make the #Rewritten Instruction# become verbose. #Rewritten Instruction# can only add 10 to 20 words into #Given Instruction#.
        #Given Instruction#
        {inst}
        #Rewriting Requirement#
        Please add one proper situation constraint to the #Given Instruction#. The situation constraints include but are not limited to:
        1. Specify a Role: Clearly define the role or persona to be taken on during the role-play.
        2. Define the Setting: Outline the environment or context in which the role-play should occur.
        3. Add Conflict or Challenge: Introduce a specific problem, conflict, or challenge that must be addressed within the role-play.
        4. Limit the Actions: Restrict the types or number of actions that can be taken during the role-play.
        5. Set Specific Goals: Define clear objectives that the role-player must achieve.
        6. Introduce Time Constraints: Impose a time limit for the role-play to unfold or for certain actions to be completed.
        Please output in JSON format with the fields 'modified_instruction' for the modified instruction and 'added_constraint' for the added constraint.
        """
    elif constraint == "Story":
        user_prompt = f"""
        You are an Instruction Rewriting Expert. You need to rewrite #Given Instruction# based on #Rewriting Requirement#, in order to obtain a #Rewritten Instruction#. 
        Basically, #Rewritten Instruction# should adhere to the following guidelines:
        1. Your rewriting cannot omit the non-text parts such as the table and code in #Given Instruction#.
        2. #Rewritten Instruction# must be reasonable and must be understood and responded to by humans.
        3. You should try your best not to make the #Rewritten Instruction# become verbose. #Rewritten Instruction# can only add 10 to 20 words into #Given Instruction#.
        #Given Instruction#
        {inst}
        #Rewriting Requirement#
        Please add one proper situation constraint to the #Given Instruction#. The situation constraints include but are not limited to:
        1. Define Character Archetypes: Specify certain archetypes or roles characters should fulfill, such as a hero, mentor, or antagonist.
        2. Include Specific Plot Points: Mandate the inclusion of certain events or plot twists that must occur.
        3. Moral Dilemmas: Introduce a scenario where the characters must make a tough decision that involves competing ethical principles or risks.
        Please output in JSON format with the fields 'modified_instruction' for the modified instruction and 'added_constraint' for the added constraint.
        """
    elif constraint == "Style":
        user_prompt = f"""
        You are an Instruction Rewriting Expert. You need to rewrite #Given Instruction# based on #Rewriting Requirement#, in order to obtain a #Rewritten Instruction#. 
        Basically, #Rewritten Instruction# should adhere to the following guidelines:
        1. Your rewriting cannot omit the non-text parts such as the table and code in #Given Instruction#.
        2. #Rewritten Instruction# must be reasonable and must be understood and responded by humans.
        3. You should try your best not to make the #Rewritten Instruction# become verbose. #Rewritten Instruction# can only add 10 to 20 words into #Given Instruction#.
        #Given Instruction#
        {inst}
        #Rewriting Requirement#
        Please add one proper style constraint that #Given Instruction# does not have. The style constraints include but are not limited to:
        1. Tone and Emotion: Specify the desired emotional tone for the response.
        2. Writing Style: Ask the AI to mimic a specific author's writing style.
        3. Contradiction: Ask the AI to provide a response that contradicts the previous statement or take a stance opposite to its prior response.
        4. Ambiguity: Instruct the AI to create responses with intentional ambiguity or double meanings.
        5. Humor or Satire: Request that the response be humorous or satirical, requiring the AI to generate jokes or witty remarks.
        Please output in JSON format with the fields 'modified_instruction' for the modified instruction and 'added_constraint' for the added constraint.
        """
    else:
        print("error")
    logging.basicConfig(level=logging.INFO)
    for i in range(MAX_API_RETRY):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model='gpt-4o',
                max_tokens=max_tokens,
                temperature=0.0,
                messages=[{
                    'role': 'user',
                    'content': user_prompt,
                }],
            )
            content = response.choices[0].message.content
            logger.info(content)
            return content
        except Exception as e:
            logger.error(e)
            time.sleep(20)
    logger.error(f'Failed after {MAX_API_RETRY} retries.')
    return 'error'
