import argparse
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import uvicorn
from fastapi import FastAPI, UploadFile, File, status,  Response

import receipt_processor
import exceptions

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-p", "--port", default="8000", type=int,
                             help="Port to listen for receipt processing requests on")
args = argument_parser.parse_args()

app = FastAPI()


@app.post("/process-receipt", status_code=status.HTTP_200_OK)
def handle_process_receipt(response: Response, image_buffer: UploadFile = File(...)) -> Optional[str]:
    """
    Process a receipt image and return a json representing the data in it
    """
    with NamedTemporaryFile(mode="rw") as temp_image_file:
        temp_image_file.write(image_buffer.file.read())
        try:
            receipt = receipt_processor.process_receipt(Path(temp_image_file.name))
            return receipt.encode()
        except (exceptions.NotAReceiptError, exceptions.BadQualityError) as e:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return f"{type(e)}"


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=args.port)