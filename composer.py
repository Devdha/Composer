#!/usr/bin/env python
import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv
from core.agent import Composer
from core.llm.factory import LLMClientFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    load_dotenv()  # Load environment variables from .env
    
    parser = argparse.ArgumentParser(
        description="Autonomous Service Composer - AI-powered service builder"
    )
    parser.add_argument(
        "requirements", 
        type=str,
        help="Service requirements description"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=Path("services"),
        help="Output directory for generated services"
    )
    parser.add_argument(
        "--llm-provider",
        choices=["deepseek", "openai"],
        default="deepseek",
        help="LLM provider to use"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/settings.yaml"),
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize LLM client via factory
        llm_client = LLMClientFactory.create_client(args.llm_provider)
        
        # Create autonomous agent
        agent = Composer(
            llm_client=llm_client,
            output_dir=args.output_dir,
            config_path=args.config
        )
        
        # Start build process
        result = agent.build_service(args.requirements)
        
        if result["status"] == "success":
            logger.info(f"Service built successfully at: {result['path']}")
        else:
            logger.error("Failed to build service")
            logger.error(f"Error details: {result.get('errors', 'No details')}")
            exit(1)
            
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()