# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the shared state for the abci skill of Mech."""
from typing import Any, Optional, Dict, Callable, List

from aea.exceptions import enforce
from aea.protocols.dialogue.base import Dialogue
from aea.skills.base import Model


class Params(Model):
    """A model to represent params for multiple abci apps."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the parameters object."""
        self.use_polling = kwargs.get("use_polling", False)
        self.agent_mech_contract_address = kwargs.get("agent_mech_contract_address", None)
        enforce(self.agent_mech_contract_address is not None, "agent_mech_contract_address must be set!")

        self.in_flight_req: bool = False
        self.from_block: int = 0
        self.req_to_callback: Dict[str, Callable] = {}
        self.api_keys: Dict = self._nested_list_todict_workaround(kwargs, "api_keys_json")
        self.file_hash_to_tools: Dict[
            str, List[str]
        ] = self._nested_list_todict_workaround(
            kwargs, "file_hash_to_tools_json",
        )
        self.task_deadline = kwargs.get("task_deadline", 240)
        super().__init__(*args, **kwargs)


    def _nested_list_todict_workaround(
        self, kwargs: Dict, key: str,
    ) -> Dict:
        """Get a nested list from the kwargs and convert it to a dictionary."""
        values = kwargs.get(key)
        if len(values) == 0:
            raise ValueError(f"No {key} specified!")
        return {value[0]: value[1] for value in values}

