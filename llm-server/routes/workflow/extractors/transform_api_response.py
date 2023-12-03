import os
import logging
import json
from langchain.schema import HumanMessage, SystemMessage
from routes.lossy_compressors.truncate_json import truncate_json
from utils import get_chat_model
from utils.chat_models import CHAT_MODELS


openai_api_key = os.getenv("OPENAI_API_KEY")


def transform_api_response_from_schema(server_url: str, responseText: str) -> str:
    chat = get_chat_model(CHAT_MODELS.gpt_3_5_turbo_16k)

    # responseText = truncate_json(json.loads(responseText))
    messages = [
        SystemMessage(
            content="You are a bot capable of comprehending API responses."
        ),
        HumanMessage(
            content=f"Here is the response from current REST API: {responseText} for endpoint: {server_url}"
        ),
        HumanMessage(
            content="Analyze the provided API responses and extract only the essential fields required for subsequent API interactions. Disregard any non-essential attributes such as CSS or color-related data. If there are generic fields like 'id,' provide them with more descriptive names in your response. Format your response as a minified JSON object with clear and meaningful keys that map to their respective values from the API response."
        ),
    ]

    result = chat(messages)
    logging.info(f"[OpenCopilot] Transformed Response: {result.content}")

    return result.content
