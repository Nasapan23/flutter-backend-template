from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional

from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_active_user
from app.schemas.ai import ChatCompletionRequest, ChatCompletionResponse, ModelInfoResponse
from app.ai.llm.openai_service import generate_chat_completion, list_available_models

router = APIRouter()


@router.get("/models", response_model=List[ModelInfoResponse])
async def get_available_models(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get list of available AI models
    """
    try:
        models = await list_available_models()
        return models
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve models: {str(e)}"
        )


@router.post("/chat", response_model=ChatCompletionResponse)
async def create_chat_completion(
    request: ChatCompletionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate a chat completion using OpenAI
    """
    try:
        response = await generate_chat_completion(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate completion: {str(e)}"
        ) 