import requests
endpoint = 'https://api.opentyphoon.ai/v1/chat/completions'
res = requests.post(endpoint, json={
    "model": "typhoon-v1.5x-70b-instruct",
    "max_tokens": 1024,
    "messages": [...],
    "temperature": 0.88,
    "top_p": 0.9,
    "top_k": 0,https://github.com/github-copilot/signup
    "repetition_penalty": 1.05,
    "min_p": 0
}, headers={
    "Authorization": "Bearer sk-kdTPGlP6akWgbfw0V0CCQ4IPz9GfYjPTEU1X7cC1OMqLMMie",
})
