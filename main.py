import streamlit as st
import requests


API_TOKEN = st.secrets['API_TOKEN']
API_URL = "https://api-inference.huggingface.co/models/steeldream/letov"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    """Send a request to the API and return the response."""
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


if __name__ == '__main__':

    page_title = "Нейронная оборона 2.0"
    page_icon = "🎸"
    layout = "centered"

    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

    streamlit_style = """
        <style>
        [data-testid="stText"] {
            font-size: 1rem;
            font-family: "Source Serif Pro", serif;
        }
        </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True)

    st.title(page_title + " " + page_icon)
    st.markdown("""
        >_Когда я умер, не было никого, кто бы это опроверг._

        Егор Летов — советский и российский музыкант, поэт и «патриарх»
        русского панк-рока. Основанный им музыкальный проект
        [«Гражданская оборона»](https://gr-oborona.ru/) (ГрОб) был одним
        из влиятельнейших панк-групп России и СССР, и распался в
        2008 году в связи с кончиной Егора.
        
        Я обучил языковую модель [ruGPT3](https://sbercloud.ru/ru/datahub/rugpt3family/demo-ru-gpt3-xl)
        на 600+ песнях ГрОба для генерации текстов песен по названию, чтобы
        понять как данная модель «видит» его творчество. Гитхаб с этим проектом доступен
        [тут](http://github.com/armanbolatov/grob).
        
        По вопросам писать — `a.bol[at]bc-pf[dot]org`.
        """)

    st.image("yegor.jpg", use_column_width=True)

    input = st.text_input(
        "Для генерации придумайте название песни",
        max_chars=50,
        placeholder="Всё идет по плану",
    )

    if input:

        payload = {
            "inputs": f"<s>Название песни: {input}\nТекст песни:",
            "parameters": {
                "max_new_tokens": 250,
                "temperature": 1.0,
                "repetition_penalty": 1.05,
                "top_k": 5,
                "top_p": 1,
                "return_full_text": False,
            },
            "options": {
                "wait_for_model": True,
            }
        }

        with st.spinner("Идёт генерация..."):
            output = query(payload)
            if "error" in output:
                if output["error"].startswith("Rate limit reached"):
                    st.error("""
                    Модель запускается на моем базовом аккаунте HuggingFace и на ней
                    достигнут лимит бесплатного использования (сбрасывается ежечасно).
                    Подождите попробуйте подождать ~час и запустить снова.
                    """)
                else:
                    st.error(output["error"])

        if "error" not in output:
            st.success("Готово!")
            st.subheader(input)
            output_text = output[0]["generated_text"]
            try:
                result = str(output_text[:output_text.index("</s>") + 1])[:-1]
            except:
                result = output_text
                result += "..."

            st.text(result)