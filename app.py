"""
Main application for the Agentic RAG system.
Demonstrates the plug-and-play architecture.
"""

import sys
import os
import logging
from pathlib import Path
import json

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.component_registry import register_all_components
from dotenv import load_dotenv
load_dotenv("./.env")


from orchestrator.rag_orchestrator import RAGOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    logger.info("Starting Agentic RAG System")
    logger.info("=" * 50)

    try:

        logger.info("Loading configuration...")
        orchestrator = RAGOrchestrator("config.json")

        logger.info("System Information:")
        info = orchestrator.get_system_info()
        logger.info(
            f"System: {info['config']['system']['name']} v{info['config']['system']['version']}"
        )
        logger.info(f"Parser: {info['components']['parser']}")
        logger.info(f"Chunker: {info['components']['chunker']}")
        logger.info(f"Vector Store: {info['components']['vector_store']}")
        logger.info(f"Manager Agent: {info['components']['manager_agent']}")
        logger.info(f"Assistant Agent: {info['components']['assistant_agent']}")

        logger.info("Processing Document...")
        # document_path = [
        #     {
        #         "path": "documents/Family Health Optima Insurance Plan.pdf",
        #         "name": "familyHealthOptimaInsurancePlan",
        #     },
        #     {
        #         "path": "documents/Senior Citizens Red Carpet Health Insurance Policy.pdf",
        #         "name": "seniorCitizensRedCarpetHealthInsurancePolicy",
        #     },
        #     {
        #         "path": "documents/Star Comprehensive Insurance Policy.pdf",
        #         "name": "starComprehensiveInsurancePolicy",
        #     },
        #     {
        #         "path": "documents/Star Health Gain Insurance Policy.pdf",
        #         "name": "starHealthGainInsurancePolicy",
        #     },
        # ]

        # for document in document_path:
        #     if os.path.exists(document["path"]):
        #         try:
        #             node_ids = orchestrator.process_document(document)
        #             logger.info(
        #                 f"Document processed successfully! Added {len(node_ids)} nodes to vector store."
        #             )
        #         except Exception as e:
        #             logger.error(f"Error processing document: {e}")
        #     else:
        #         logger.warning(f"Document not found: {document['path']}")

        questions = json.load(open("./question.json"))

        for question in questions:
            logger.info(f"Question: {question}")
            try:

                response = orchestrator.query(question, use_manager=True)
                logger.info(f"Manager Response: {response}...")

            except Exception as e:
                logger.error(f"Error processing query: {e}")

        logger.info("Demonstrating Component Switching...")

        # # Switch to hierarchical chunker
        # logger.info("Switching to hierarchical chunker...")
        # try:
        #     orchestrator.switch_chunker("hierarchical")
        #     logger.info("Switched to hierarchical chunker")
        # except Exception as e:
        #     logger.error(f"Error switching chunker: {e}")

        # # Display updated system info
        # logger.info("Updated System Information:")
        # info = orchestrator.get_system_info()
        # logger.info(f"Chunker: {info['components']['chunker']}")

        # logger.info("Demo completed successfully!")

    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
