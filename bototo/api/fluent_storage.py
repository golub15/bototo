from abc import abstractmethod, ABC


class FluentStorageProtocol(ABC):
    all_lang_dict: dict

    @abstractmethod
    async def load(self):
        raise NotImplementedError

    @abstractmethod
    async def save(self):
        raise NotImplementedError

    def get_dict_for_lang(self, lang_code: str) -> dict:
        return self.all_lang_dict.get(lang_code, {})

    async def edit_key_and_save(self, lang_code: str, key: str, new_value: str):
        self.all_lang_dict[lang_code][key] = new_value
        await self.save()
