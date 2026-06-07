import logging
import logging.handlers
import json
from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logger(name: str = "app_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONFormatter())
        logger.addHandler(console_handler)

        # File Handler
        log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        try:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                log_file, when="midnight", interval=1, backupCount=7
            )
            file_handler.setFormatter(JSONFormatter())
            logger.addHandler(file_handler)
        except OSError as exc:
            logger.warning("File logging disabled: %s", exc)

    return logger

logger = setup_logger("app_logger")
