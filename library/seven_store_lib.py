import fitz

from fastapi import HTTPException, UploadFile
from .dao import SevenStore, SevenStoreDao
from pyfk import get_logger
from logging import Logger

class SevenStoreLib:

    log: Logger

    dao: SevenStoreDao

    def __init__(self):
        self.dao = SevenStoreDao()
        self.log = get_logger()

    async def import_store_by_pdf(self, file: UploadFile):
        self.log.info("Get file %s, start process.", file.filename)

        if file.content_type != "application/pdf":
            raise HTTPException(status_code=422, detail="File type only accept pdf.")
        
        try:
            content = await file.read()
        finally:
            await file.close()

        self.log.info("Read pdf.")
        chunk_list = []
        with fitz.open(stream=content, filetype="pdf") as pdf:
            for page in pdf:
                chunk_list.extend(list(filter(
                    lambda c: c.strip() not in ["門市", "門市代號", "縣市", "地址", "電話", ""],
                    page.get_text().split("\n")
                )))

        self.log.info("Create store objects.")
        store_list = []
        for i in range(0, len(chunk_list), 5):
            code = chunk_list[i + 1]
            name = chunk_list[i]
            city = chunk_list[i + 2][:3]
            address = chunk_list[i + 2][3:]
            phone_code = chunk_list[i + 3]
            phone_number = chunk_list[i + 4]
            store = SevenStore(code, name, city, address, phone_code, phone_number)
            store_list.append(store)
        
        self.log.info("Delete old stores, %d rows.", self.dao.delete_all_store())

        self.log.info("Insert new stores, %d rows.", len(store_list))
        self.dao.create_batch(store_list)