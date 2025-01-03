# experiment for apache
#

import pyarrow as pa
from pathlib import Path
import logging
import os


cwd = Path(__file__).parent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename=os.path.join(cwd, "ARROW.log"), mode="w", encoding="utf-8"),
        # logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


if __name__ == "__main__"
