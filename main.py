import streamlit as st
import openai
# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# api key setting for deploy
openai.api_key = st.secrets.ChatGptKey.key

# api key setting for local
# load_dotenv(join(dirname(__file__), '.env'))
# openai.api_key = os.environ.get("API_KEY")


def main():

    # initialize messages
    messages = []

    st.title('Summary Bot')
    st.text_area('sentence:', height=250, key='input_sentence')
    st.selectbox(
        'length:',
        [
            '指定なし',
            '300文字以内で',
            '100文字以内で',
            '50文字以内で',
        ],
        key='input_length'
    )
    st.multiselect(
        'option:',
        [
            'カジュアルに',
            'フォーマルに',
            '箇条書きで',
            '英語で',
        ],
        key='input_option'
    )

    # summary
    def do_summary():

        # setting prompt
        sentence = st.session_state.input_sentence.strip()
        length = st.session_state.input_length.strip()
        option = ''
        for text in st.session_state.input_option:
            option = option + '・' + text + '\n'
        if sentence:
            str1 = "条件に従い、以下の文章を要約してください。"
            str2 = "文章:"
            str3 = "条件:"
            prompt = f"{str1}\n{str2}\n{sentence}\n{str3}\n・{length}\n・{option}"
            messages.append({"role": "user", "content": prompt})

            # make response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            # add response to messages
            messages.append(response.choices[0]["message"])

    st.button("summarize", on_click=do_summary())

    if messages:
        st.write(messages[1]['content'])


if __name__ == "__main__":
    main()
