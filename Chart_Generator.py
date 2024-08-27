import streamlit as st
import os
#import langchain_helper
st.title("Restaurant Name Generator")



from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

llm = OpenAI(temperature=0.7, openai_api_key=os.getenv('OPENAI_API_KEY'))

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

cuisine = st.sidebar.selectbox("Pick a cuisine",("Indian","Italian","Mexican","Arabic","American"))

if cuisine:
    response = generate_restaurant_name_and_item(cuisine)
    st.header(response['restaurant_name'])
    menu_items = response['menu_items'].split(",")
    st.write("**Menu Items**")
    for item in menu_items:
        st.write("-",item)
