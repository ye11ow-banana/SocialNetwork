from typing import NamedTuple

import yaml


class Config(NamedTuple):
    number_of_users: int
    max_posts_per_user: int
    max_likes_per_user: int


def read_config(config_path: str) -> Config:
    with open(config_path) as file:
        try:
            return Config(**yaml.safe_load(file))
        except yaml.YAMLError:
            raise yaml.YAMLError('Error while opening config')
