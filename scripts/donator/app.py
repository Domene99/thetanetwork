import streamlit as st
import re
from donate import donate

def toIntOrZero(num):
    if num.isnumeric():
        return int(num)
    return 0

def toListOrEmpty(string):
    res_list = []
    single_quote_no_spaces = "\[(\'\w+\'\,?)+\]"
    single_quote_with_spaces = "\[(\'\w+\'\,?\ )+(\'\w+\')\]"
    double_quote_no_spaces = "\[(\"\w+\"\,?)+\]"
    double_quote_with_spaces = "\[(\"\w+\"\,?\ )+(\"\w+\")\]"
    if re.search(single_quote_no_spaces, string) or re.search(double_quote_no_spaces, string):
        res_list = string[1:-1].split(',')
        res_list = [el[1:-1] for el in res_list]
        
    if re.search(single_quote_with_spaces, string) or re.search(double_quote_with_spaces, string):
        res_list = string[1:-1].split(', ')
        res_list = [el[1:-1] for el in res_list]
    return res_list

def app():
    st.set_page_config(page_title="Video Donator",
                       page_icon=":movie_camera:", layout="wide")
    st.title("Donate to videos :clapper:")

    swear_count = st.text_input('What\'s the maximum number of swear words?', placeholder = '10')
    topicKeys = st.text_input('What topics does the video need to talk about?', placeholder = '["technology", "science", "slavery"]')
    topicValues = st.text_input('What must be the sentiment of this topics(same order)?', placeholder = '["positive", "positive", "negative"]')
    safety_score = st.text_input('What\'s the minimum brand safety score(0-100)?', placeholder = '50')
    language = st.text_input('What language should the video be in?', placeholder = 'English')
    amount = st.text_input('How much do you wish to donate?', placeholder='15')

    swear_count = toIntOrZero(swear_count)
    safety_score = toIntOrZero(safety_score)
    topicKeys = toListOrEmpty(topicKeys)
    topicValues = toListOrEmpty(topicValues)
    amount = toIntOrZero(amount)

    if st.button("Send"):
        tx = donate(swear_count, topicKeys, topicValues, safety_score, language, amount)
        st.write(tx)

# Run the Streamlit app
if __name__ == '__main__':
    app()