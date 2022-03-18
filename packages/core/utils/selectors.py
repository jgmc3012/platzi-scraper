from packages.core.utils.singleton import SingletonClass
import yaml
import os
import inspect


class Selector(metaclass=SingletonClass):
    _config_ = dict()

    def get_selector(self, Class):
        if not self._config_.get(Class):
            path = f'{os.path.dirname(inspect.getfile(Class))}/selectors.yml'
            with open(path, "r") as stream:
                config_db = yaml.safe_load(stream)
            self._config_[path] = config_db
        return self._config_[path]
