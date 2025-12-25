"""
title: TA_API_Tool
author: me
description: 呼叫 TA LLM API
requirements: ollama, requests
version: 0.1.0
"""

import os
from ollama import Client

# 從環境變數取得 API key
api_key = "2e1a94af2dd9695add161d77ffc47143d78eeccc1e6d7956bd106e0fd37f6c50"
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
