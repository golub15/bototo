from ..api.fluent_storage import FluentStorageProtocol

import json


class FluentStorageFile(FluentStorageProtocol):
    fluent_file_path: str

    def __init__(self, file_path: str):
        self.fluent_file_path = file_path

    async def load(self):
        with open(self.fluent_file_path, mode='r', encoding="utf-8") as fp:
            self.all_lang_dict = json.load(fp)

    async def save(self):
        with open(self.fluent_file_path, mode='w', encoding="utf-8") as fp:
            json.dump(self.all_lang_dict, fp, ensure_ascii=False)
