import asyncio
import logging
import signal
import sys
from typing import Any

from orchestrator.bot_manager import BotManager
from orchestrator.config_parser import parse_interface_config

# Setup console logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

async def run_orchestrator() -> None:
    """Main lifecycle entrypoint for the async orchestrator."""
    logger.info("Initializing Orchestrator...")
    
    # 1. Simulate an incoming task payload from the Web Interface
    mock_payload = {
        "site": "fnac",
        "search_query": "L'Attaque Des Titans Tome 02",
        "keyword_groups": [
            ["attaque", "titans", "tome", "02"]
        ],
        "exclude": [],
        "products": [
            {
                "display_name": "Attack On Titan - Tome 02",
                "match": {
                    "required_groups": [
                        ["attaque", "titans", "tome", "02"]
                    ],
                    "exclude": []
                }
            }
        ]
    }
    
    # 2. Parse and normalize the config
    logger.info("Parsing incoming task configuration...")
    try:
        parsed_config = parse_interface_config(mock_payload)
        logger.info(f"Config successfully parsed: {parsed_config['products'][0]['display_name']}")
    except ValueError as e:
        logger.error(f"Failed to parse config: {e}")
        return

    # 3. Instantiate Manager
    manager = BotManager()
    
    # 4. Handle graceful shutdown (Ctrl+C)
    def handle_signal(*args: Any) -> None:
        logger.info("Interrupt signal received. Shutting down...")
        asyncio.create_task(manager.shutdown())
        
        # Give it a bit of time to print shutdown logs then exit
        loop = asyncio.get_running_loop()
        loop.call_later(2.0, lambda: sys.exit(0))
        
    # Bind signals
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, handle_signal)

    # 5. Spawn a worker for the task
    manager.spawn_worker(worker_id="Alpha-1", task_config=parsed_config)
    # manager.spawn_worker(worker_id="Alpha-2", task_config={"site": "pokemon_center"})
    
    # 6. Keep the main loop alive
    logger.info("Orchestrator running. Press Ctrl+C to stop.")
    while True:
        await asyncio.sleep(3600)

def main() -> None:
    try:
        asyncio.run(run_orchestrator())
    except KeyboardInterrupt:
        # Handled by signal handler, this just catches the final sys.exit trace ideally
        pass

if __name__ == "__main__":
    main()
