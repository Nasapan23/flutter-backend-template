from typing import Dict, Any, List, Optional
import os
from transformers import pipeline
import asyncio

# Cache for loaded models
model_cache = {}


async def load_model(model_name: str, task: str):
    """
    Load a Hugging Face model asynchronously
    """
    # Check if the model is already loaded
    cache_key = f"{model_name}_{task}"
    if cache_key in model_cache:
        return model_cache[cache_key]
    
    # Load model in a separate thread to not block the event loop
    loop = asyncio.get_event_loop()
    
    def _load_model():
        return pipeline(task=task, model=model_name)
    
    # Load model
    model = await loop.run_in_executor(None, _load_model)
    
    # Cache the model
    model_cache[cache_key] = model
    
    return model


async def text_generation(
    prompt: str,
    model_name: str = "gpt2",
    max_length: int = 50,
    temperature: float = 0.7,
    num_return_sequences: int = 1
) -> List[str]:
    """
    Generate text using a Hugging Face model
    """
    try:
        # Load the model
        generator = await load_model(model_name, "text-generation")
        
        # Run generation in a separate thread
        loop = asyncio.get_event_loop()
        
        def _generate():
            return generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=num_return_sequences
            )
        
        # Generate text
        result = await loop.run_in_executor(None, _generate)
        
        # Extract generated text
        return [item['generated_text'] for item in result]
    
    except Exception as e:
        raise Exception(f"Error generating text: {str(e)}")


async def sentiment_analysis(
    text: str,
    model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
) -> List[Dict[str, Any]]:
    """
    Perform sentiment analysis using a Hugging Face model
    """
    try:
        # Load the model
        classifier = await load_model(model_name, "sentiment-analysis")
        
        # Run analysis in a separate thread
        loop = asyncio.get_event_loop()
        
        def _analyze():
            return classifier(text)
        
        # Analyze text
        result = await loop.run_in_executor(None, _analyze)
        
        return result
    
    except Exception as e:
        raise Exception(f"Error analyzing sentiment: {str(e)}")


async def question_answering(
    question: str,
    context: str,
    model_name: str = "distilbert-base-cased-distilled-squad"
) -> Dict[str, Any]:
    """
    Answer a question using a Hugging Face model
    """
    try:
        # Load the model
        qa_pipeline = await load_model(model_name, "question-answering")
        
        # Run QA in a separate thread
        loop = asyncio.get_event_loop()
        
        def _answer():
            return qa_pipeline(question=question, context=context)
        
        # Get answer
        result = await loop.run_in_executor(None, _answer)
        
        return result
    
    except Exception as e:
        raise Exception(f"Error answering question: {str(e)}") 