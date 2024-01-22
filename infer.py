import pandas as pd
# from feedback_error import *
from tools.codemanager.helpers.code_manager_cus import CodeManager
from tools.dataframe import generate_dataframes, code_prompt, plot_code_prompt
import re
from tools.dataframe import *
import pandas as pd
import numpy as np
from test import llm
import time
import re

def generate_prompt(instruction):
    return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:"""

def extract_code(code):
    if "```python" in code:
        try:
            code = re.findall(r"```python(.*?)```",code, re.DOTALL)[0].strip()
        except:
            code = re.findall(r"```python(.*?)$", code, re.DOTALL)[0].strip()
    elif "```" in code:
        try:
            code = re.findall(r"```(.*?)```",code, re.DOTALL)[0].strip()
        except:
            start = code.find("```")
            code = code[start+3:].strip()
    return code

def run_one_code(code, codemanager):
    code = extract_code(code)
    result, code_to_run = codemanager.execute_code(code)
    return result, code_to_run



def infer(df: pd.DataFrame,
          question: str,
          model,
          df_name: str = None,
          df_description: str = None,
          plot: bool = False,
          save_img: str = None):
    """
    :param df: pd.DataFrame
    :param question:
    :param model:
    :param tokenizer:
    :param df_name:
    :param df_description:
    :param try_n: batch size
    :param plot: if ask model to plot chart
    :param save_img: the path_name to save chart
    :return:
    """

    df_dec = generate_dataframes(df, df_name, df_description)

    if plot:
        _, instruction = plot_code_prompt(df_dec, question)
    else:
        _ ,instruction = code_prompt(df_dec, question)

    

    prompts = generate_prompt(instruction)
    print("prompt_done...\n", prompts)

    # start_time= time.time()
    # print(model(prompts))
    output=model(prompts)
    # print("Time taken to complete is {} seconds".format(time.time()-start_time))
    print("LLM output:\n ",output)



    if plot:
        anly_codemanager = CodeManager(df=df, func_name="plot_chart")
    else:
        anly_codemanager = CodeManager(df=df, func_name="analyze_data")

    
    # print("LLM output: ",output)
    # try:
    #     final_output = output[0].split("### Response:")[1].strip()
    # except:
    #     print("input prompt is too long, return empty answer")
    #     return "", ""

    for output_code in output:

        if plot and save_img:
            output_code=output_code.replace("./charts/temp_chart2.png", save_img)

        answer, code_to_run = run_one_code(output, anly_codemanager)

        if code_to_run:
            print("code running successfully")
            return answer, code_to_run

    return None, None

# question_for_plot = "whats the average of column3?"

# Example: Create a pandas DataFrame
# data = {'Column1': [1, 2, 3, np.nan, 5],
#         'Column2': ['apple', 'banana', 'orange', 'banana', 'apple'],
#         'Column3': [1.1, 2.2, 3.3, 4.4, 5.5],
#         'Column4': ['True', 'False', 'True', 'False', 'True']
#         }

# df = pd.DataFrame(data)
df = pd.read_csv("./data/CancerDeath.csv")
print("Processing...")

model=llm

# output=infer(df, question_for_plot, llm, plot=False)
# print("Extracted Code below: ",extract_code(output))
# output_result1 = run_one_code(extract_code(output), df)
# print("Final Result:", output_result1)

# print("Got LLM Response Successfully")
start_time=time.time()
result, code_to_run = infer(
    df=df,
    question="summarise the changes happened between 2015 to 2016",
    model=llm,
    df_name="CancerDeath",
    plot=False,
    save_img="./charts"
)

# Use the result and code_to_run as needed
print("Thought Process :", code_to_run)
print("Result:", result)

print("Time taken to execute: {} seconds".format(time.time()-start_time))
