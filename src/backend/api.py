""" FastAPI backend for the application. """

from fastapi import FastAPI,HTTPException
from src.entity.artifacts import RequestState
from src.core.agent import get_response_from_ai_agents
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="MULTI AI AGENT")


@app.post("/chat")
def chat_endpoint(request:RequestState):
    logger.info(f"Received request for model : {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODELS_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400 , detail="Invalid model name")
    
    try:
        response = get_response_from_ai_agents(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )

        logger.info(f"Sucesfully got response from AI Agent {request.model_name}")

        return {"response" : response}
    
    except Exception as e:
        logger.error("Some error ocuured during reponse generation")
        raise HTTPException(
            status_code=500 , 
            detail=str(CustomException("Failed to get AI response" , error_detail=e))
            )