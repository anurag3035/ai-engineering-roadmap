import logging
import json
import uuid


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "N/A")
        }

        return json.dumps(log_data)


logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(JsonFormatter())

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(levelname)s - %(message)s")
)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class AppError(Exception):
    pass


class DocumentNotFoundError(AppError):
    pass


class EmbeddingError(AppError):
    pass


class RetrievalError(AppError):
    pass


class APIConnectionError(AppError):
    pass


def process_document(document_name):
    request_id = str(uuid.uuid4())

    logger.info(
        "Starting document processing",
        extra={"request_id": request_id}
    )

    if document_name == "":
        raise DocumentNotFoundError("Document name is empty")

    logger.info(
        f"Successfully processed {document_name}",
        extra={"request_id": request_id}
    )


try:
    process_document("sample.txt")
    process_document("")
except AppError as e:
    logger.error(str(e))