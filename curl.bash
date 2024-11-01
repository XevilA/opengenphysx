curl --location 'https://api.opentyphoon.ai/v1/chat/completions' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer sk-kdTPGlP6akWgbfw0V0CCQ4IPz9GfYjPTEU1X7cC1OMqLMMie' \
    --data '{
        "model": "typhoon-v1.5x-70b-instruct",
        "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant. You must answer only in Thai."
        },
        {
            "role": "user",
            "content": "Write me Swift Sample"
        }
        ],
        "max_tokens":2048,
        "temperature": 0.6,
        "top_p": 0.95,
        "repetition_penalty": 1.05,
        "stream": false
        
        }'
        
