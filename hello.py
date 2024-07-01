# -*- coding: utf-8 -*-

import requests
import json
import streamlit as st


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }
        
        ret = []

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request) as r:
            for line in r.iter_lines():
                if line:
                    ret.append(line.decode("utf-8"))
        return ret


if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY4SPwkWQYfeDOpCnevOaWbPtxXZLWD8zLLLk+jldf4Jt',
        api_key_primary_val='9sszCKk6dedJQapAf6Vjdn9We1H8ruLX1w5pBGTk',
        request_id='3441c7ee-3410-4619-9cc2-779dee27b8b4'
    )

    st.set_page_config(page_title="MBTI백과사전", page_icon=":smiley:")
    st.title("MBTI 백과사전")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    question = st.chat_input("MBTI의 궁금한것을 질문해봐")
    messages = st.container()
    
    if question :

        preset_text = [{"role":"system","content":"- MBTI에 대한 지식을 기반으로, MBTI 질문에 답해보세요.\n\n질문: ESFJ는 문제에 봉착했을때 어떻게 대응하는가?\n답: 현실적인 해결 방법을 찾기 위해 노력합니다.\n###\n질문: ISFJ는 연인에게 어떻게 대하는 편인가?\n답: 섬세하고 다정하게 케어해주는 편입니다.\n####\n질문: INTP는 사람들이 많은 곳에 가면 어떻게 행동하는가?\n답: 주변의 상황을 파악하기 위해 관찰하는 편입니다.\n###\n질문: ESFJ는 충동적인 선택을 많이 하는 편인가?\n답: 아니다. 계획적으로 움직이는 편입니다."},{"role":"user","content":question}]

        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 512,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

        response_text = completion_executor.execute(request_data)
        
        result = json.loads(response_text[-4][5:])
        messages.chat_message("user").write(question)
        messages.chat_message("assistant").write(result['message']['content'])
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": result['message']['content']})
        
