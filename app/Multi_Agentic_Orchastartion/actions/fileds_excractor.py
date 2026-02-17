import re
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_fields_from_message(message: str, required_fields: List[str]) -> Dict[str, str]:
    extracted = {}
    logger.info("Extracting fields from message: %s", message)

    if not required_fields:
        return extracted

    message_lower = message.lower()

    for field in required_fields:
        field_lower = field.lower()
        value = None

        # Explicit format: "field: value" or "field = value"
        pattern = rf"{field_lower}\s*[:=]\s*(['\"]?)(.+?)\1(?=,|;|$)"
        match = re.search(pattern, message_lower, re.IGNORECASE)
        if match:
            value = match.group(2).strip()
            logger.info("Found explicit field '%s': %s", field, value)
            extracted[field] = value
            continue

        # Simple natural language patterns
        if field_lower == "summary":
            summary_match = re.search(r"(?:summary|ticket for|title)\s*[:=]?\s*(.+?)(?:,|;|$)", message_lower)
            if summary_match:
                value = summary_match.group(1).strip()
                logger.info("Detected summary: %s", value)
        elif field_lower == "description":
            desc_match = re.search(r"(?:description|desc|details)\s*[:=]?\s*(.+?)(?:,|;|$)", message_lower)
            if desc_match:
                value = desc_match.group(1).strip()
                logger.info("Detected description: %s", value)

        extracted[field] = value

        if value is None:
            logger.info("Field '%s' missing in message.", field)

    return extracted
