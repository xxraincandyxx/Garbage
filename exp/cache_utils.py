import copy
import logging
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple


logger = logging.getLogger(__name__)


@dataclass
class Cache:
    fct_name: str
    fct_content: str
    type_name: str
    fct_args: Dict[str, str]


class FunctionStateCache:
    def __init__(self):
        """Base Cache to store the state of the function

        fct_namme (str): function name
        fct_content (str): function content
        type_name (str): type of the function
        fct_args (Dict[str, Tuple[int, str]]): arguments of the function
            containing (arg_name, (arg_value, arg_type))
        conditions (List[List, List]): conditions needed to trigger the function
        """

        self.caches: Dict[str, Cache] = {}

    def __len__(self) -> int:
        return len(self.cache)

    def __getitem__(self, key: str) -> Cache:
        return self.caches[key] if key in self.caches else None

    def __iter__(self):
        return iter(self.caches.values())

    def update(
        self,
        fct_name: str,
        fct_content: Optional[str] = None,
        type_name: Optional[str] = None,
        fct_args: Optional[Dict[str, str]] = None,
    ) -> None:
        if fct_name in self.caches:
            cache: Cache = self.caches[fct_name]
            cache.fct_content = fct_content if fct_content is not None else cache.fct_content
            cache.type_name = type_name if type_name is not None else cache.type_name
            if fct_args is not None:
                cache.fct_args.update(fct_args)
        else:
            self.caches.update(
                {
                    fct_name: Cache(
                        fct_name,
                        fct_content,
                        type_name,
                        fct_args,
                    )
                }
            )

    def _output_(self) -> None:
        for cache in self.caches.values():
            print(f"Function Name: {getattr(cache, 'fct_name', None)}")
            print(f"Return Type: {getattr(cache, 'type_name', None)}")
            print(f"Arguments: {getattr(cache, 'fct_args', None)}")
            print(f"Conditions: {getattr(cache, 'conditions', None)}")
            print(f"Content: {getattr(cache, 'fct_content', None)}")
            print()
