import re
import logging
from typing import List

logger = logging.getLogger(__name__)

def read_asins_from_file(file_path: str) -> List:
    asins_in_file = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if re.fullmatch(r"[A-Z0-9]{10}", line):
                asins_in_file.append(line)
            else:
                logger.info(f"Line is not an asin: {line}")
    return asins_in_file