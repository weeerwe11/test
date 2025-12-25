"""
title: LANG_Tool
author: me
description: 呼叫 LANG API
requirements: ollama, requests
version: 0.1.0
"""

import os
import json
from ollama import Client

# 從環境變數取得 API key
api_key = os.environ.get("2e1a94af2dd9695add161d77ffc47143d78eeccc1e6d7956bd106e0fd37f6c50")
if not api_key:
    raise ValueError("請先設定 TA_LLM_API_KEY 環境變數")

client = Client(
    host="https://api-gateway.netdb.csie.ncku.edu.tw",
    headers={'Authorization': f'Bearer {api_key}'}
)

class Tools:
    def run(self, input_text: str) -> str:
        """
        WebUI 呼叫 Tool 時會傳入 input_text
        回傳結果會顯示在對話框
        """
        messages = [{'role': 'user', 'content': input_text}]
        response_text = ""
        for part in client.chat('gemma3:4b', messages=messages, stream=True):
            response_text += part['message']['content']
        return response_text


    class LanguageTool:
        def generate_example(self, word_or_phrase: str) -> str:
            """
            給定一個單字或片語，返回 LLM 生成的例句
            """
            prompt = f"""
            Please generate one clear example sentence using the word or phrase "{word_or_phrase}".
            Return only the sentence in plain text.
            """
            messages = [{'role': 'user', 'content': prompt}]
            response_text = ""
            for part in client.chat('gemma3:4b', messages=messages, stream=True):
                response_text += part['message']['content']
            return response_text

        def generate_multiple_examples(self, word_or_phrase: str, n: int = 5) -> list:
            """
            給定一個單字或片語，返回 LLM 生成的多個例句
            """
            prompt = f"""
            Please generate {n} example sentences using the word or phrase "{word_or_phrase}".
            Return the result as a JSON list of sentences.
            Example:
            ["sentence1", "sentence2", "sentence3"]
            """
            messages = [{'role': 'user', 'content': prompt}]
            response_text = ""
            for part in client.chat('gemma3:4b', messages=messages, stream=True):
                response_text += part['message']['content']
            try:
                return json.loads(response_text)
            except:
                # 如果 LLM 沒有完全遵守 JSON 格式，回傳原始文字
                return response_text
