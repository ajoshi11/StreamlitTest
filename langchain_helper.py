from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

llm = OpenAI(temperature=0.7, openai_api_key='sk-K4O4V6vVvmgp9g2Ia0p55LVRY0m3WGNaKDRBUoKDt7T3BlbkFJADl5vDJ3i2EFrex0SfH35wtDYqnSFxFLSZumO7q00A')

def generate_restaurant_name_and_item(cuisine):
    # Chain 1
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest a name."
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}.Return it as a comma separated list"

    )

    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key = "menu_items")

    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )

    response = chain({'cuisine': cuisine})
    return response
