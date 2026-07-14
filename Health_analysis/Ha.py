import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()  

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash") #gemma-4-31b-it

with open("Health_analysis/blood_work.txt" , "r")as f:
    blood_report = f.read()

extraction_prompt = f"""
You are a medical data extraction assistant.

From the blood report below, extract ALL test values and classify each one as HIGH, LOW, or NORMAL 
based on the reference ranges provided in the report.

Format your response as:
- Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range

Blood Report:
{blood_report}
"""

ext_resp = llm.invoke(extraction_prompt)
ext_val = ext_resp.text
print("==== Stage 1: Report ====")
print(ext_val)

diet_prompt = f"""
You are a clinical nutritionist specializing in Pakistani dietary habits.

Based on the blood work analysis below, write:
1. A short health summary in 2 lines explaining the patient's condition in simple language
2. A short, practical Pakistani diet plan having only two sections (1) Foods to avoid (2) Foods to eat more of. 
   Do not include any other sections in diet plan.

Blood Work Analysis:
{ext_val}
"""

diet_resp = llm.invoke(diet_prompt)
print("==== Stage 2: Health Summary and Diet Plans ====")
print(diet_resp.text)
