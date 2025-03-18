import logging
from MassReport import app
from MassReport.module import report
from MassReport.module import start
from MassReport.database import database

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mass_report.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

if __name__ == "__main__":
    logger.info("Mass Report Bot Started!")
    try:
        app.run()
    except Exception as e:
        logger.exception(f"Bot Crashed: {e}")
