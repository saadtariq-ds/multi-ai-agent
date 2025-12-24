""" Main application entry point to start backend and frontend services """

import subprocess
import threading
import time
from src.common.logger import get_logger
from src.common.custom_exception import CustomException
from dotenv import load_dotenv
load_dotenv()

logger=get_logger(__name__)


def run_backend():
    try:
        logger.info("starting backend service..")
        subprocess.run(["uvicorn" , "src.backend.api:app" , "--host" , "127.0.0.1" , "--port" , "9999"], check=True)
    except CustomException as e:
        logger.error("Problem with backend service")
        raise CustomException("Failed to start backend" , e)
    
def run_frontend():
    try:
        logger.info("Starting Frontend service")
        subprocess.run(["streamlit" , "run" , "src/frontend/ui.py"],check=True)
    except CustomException as e:
        logger.error("Problem with frontend service")
        raise CustomException("Failed to start frontend" , e)
    
if __name__=="__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()
    
    except CustomException as e:
        logger.exception(f"Custom Exception occured : {str(e)}")


    