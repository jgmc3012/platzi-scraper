from packages.core.utils.singleton import SingletonClass
import yaml


class Config(metaclass=SingletonClass):
    _config_ = dict()

    def config_yaml(self, path):
        if not self._config_.get(path):
            with open(path, "r") as stream:
                config_db = yaml.safe_load(stream)
            self._config_[path] = config_db
        return self._config_[path]
