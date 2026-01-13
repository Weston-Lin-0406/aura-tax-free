import fitz
import requests

from .dao import SevenStore, SevenStoreDao

from bs4 import BeautifulSoup
from fastapi import HTTPException, UploadFile
from pyfk import get_logger
from logging import Logger
from typing import List

class SevenStoreLib:

    log: Logger

    dao: SevenStoreDao

    def __init__(self):
        self.dao = SevenStoreDao()
        self.log = get_logger()

    async def import_store_by_pdf(self, file: UploadFile, current_user: str):
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
            store = SevenStore(code, name, city, address, current_user)
            store_list.append(store)
        
        self.log.info("Delete old stores, %d rows.", self.dao.delete_all_store())

        self.log.info("Insert new stores, %d rows.", len(store_list))
        self.dao.create_batch(store_list)

    async def import_store_by_ibon(self, current_user: str):
        cities = [
            "台北市", "新北市", "基隆市", "宜蘭縣", "桃園市", "新竹市", "新竹縣", "苗栗縣", "台中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣", "花蓮縣", "台東縣", "澎湖縣", "金門縣", "連江縣"
        ]
        self.log.info("All cities: %s", str(cities))

        store_list = []
        for city in cities:
            self.log.info("Get city: %s", city)
            store_tmp = self.get_stores_by_city(city, current_user)
            self.log.info("Get success, store size: %d", len(store_tmp))
            store_list.extend(store_tmp)

        self.log.info("Get all stroes complete, store size: %d", len(store_list))
        self.log.info("Delete old stores, %d rows.", self.dao.delete_all_store())
        self.log.info("Insert new stores.")
        self.dao.create_batch(store_list, False)

    def get_stores_by_city(self, city: str, current_user: str) -> List[SevenStore]:
        url = "https://www.ibon.com.tw/retail_inquiry_ajax.aspx"
        data = {
            "strTargetField": "COUNTY",
            "strKeyWords": city
        }

        response = requests.post(url, data=data)

        if response.status_code != 200:
            raise HTTPException(response.status_code, detail=response.content)
        
        store_list = []

        soup = BeautifulSoup(response.content, "html.parser")
        tr_list = soup.find_all("tr")
        for tr in tr_list[1:]:
            td_list = tr.find_all("td")
            code = td_list[0].find("a").get_text().strip()
            name = td_list[1].get_text().strip()
            address = td_list[2].get_text().strip()
            store_list.append(SevenStore(code, name, city, address, current_user))

        return store_list