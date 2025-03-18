from typing import List, Dict, Any, Optional
import openai
from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.ai import Message

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def list_available_models():
    """
    List available models from OpenAI
    """
    try:
        response = await client.models.list()
        return [
            {
                "id": model.id,
                "owned_by": model.owned_by,
                "created": model.created
            } 
            for model in response.data
        ]
    except Exception as e:
        raise Exception(f"Error listing models: {str(e)}")


async def generate_chat_completion(
    messages: List[Message],
    model: str = settings.DEFAULT_LLM_MODEL,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
):
    """
    Generate a chat completion using OpenAI's API
    """
    try:
        # Convert Message objects to dictionaries
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        completion_params = {
            "model": model,
            "messages": messages_dict,
            "temperature": temperature,
        }
        
        if max_tokens:
            completion_params["max_tokens"] = max_tokens
        
        response = await client.chat.completions.create(**completion_params)
        
        # Convert response to expected format
        return {
            "id": response.id,
            "object": response.object,
            "created": response.created,
            "model": response.model,
            "choices": [
                {
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content
                    },
                    "finish_reason": choice.finish_reason
                }
                for choice in response.choices
            ],
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        raise Exception(f"Error generating completion: {str(e)}") 