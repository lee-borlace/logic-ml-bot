import json
import logging
import os
from typing import Any, List, Text, Optional, Dict, Tuple

from rasa.core.actions.action import ACTION_LISTEN_NAME

import rasa.utils.io

from rasa.core import utils
from rasa.core.domain import Domain
from rasa.core.policies.policy import Policy
from rasa.core.trackers import DialogueStateTracker

logger = logging.getLogger(__name__)

class LogicMlBotPolicy(Policy):

    @staticmethod
    def _standard_featurizer():
        return None

    def __init__(
        self,
        priority: int = 10,
        nlu_threshold: float = 0.3,
        ambiguity_threshold: float = 0.1,
        core_threshold: float = 0.3,
        fallback_action_name: Text = "action_default_fallback",
    ) -> None:
       
        super(LogicMlBotPolicy, self).__init__(priority=priority)

        self.nlu_threshold = nlu_threshold
        self.ambiguity_threshold = ambiguity_threshold
        self.core_threshold = core_threshold
        self.fallback_action_name = fallback_action_name

    def train(
        self,
        training_trackers: List[DialogueStateTracker],
        domain: Domain,
        **kwargs: Any
    ) -> None:
        pass    

    def predict_action_probabilities(
        self, tracker: DialogueStateTracker, domain: Domain
    ) -> List[float]:
        result = [0.0] * domain.num_actions
        idx = domain.index_for_action("action_hello_world")
        result[idx] = 1.0
        return result

    def persist(self, path: Text) -> None:
        """Persists the policy to storage."""

        config_file = os.path.join(path, "logicmlbot_policy.json")
        meta = {
            "priority": self.priority,
            "nlu_threshold": self.nlu_threshold,
            "ambiguity_threshold": self.ambiguity_threshold,
            "core_threshold": self.core_threshold,
            "fallback_action_name": self.fallback_action_name,
        }
        rasa.utils.io.create_directory_for_file(config_file)
        utils.dump_obj_as_json_to_file(config_file, meta)

    @classmethod
    def load(cls, path: Text) -> "CustomPolicy":
        meta = {}
        if os.path.exists(path):
            meta_path = os.path.join(path, "logicmlbot_policy.json")
            if os.path.isfile(meta_path):
                meta = json.loads(rasa.utils.io.read_file(meta_path))

        return cls(**meta)
