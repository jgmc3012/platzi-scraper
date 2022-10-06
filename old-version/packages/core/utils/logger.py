import logging
import sys
import os
import argparse
import yaml
from logging.config import dictConfig
from packages.core.utils.singleton import SingletonClass


class Logger(metaclass=SingletonClass):
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logging.getLogger('log_print').error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    def __init__(self):
        directory = './log/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--verbose', action='count', default=0)
        args, _ = parser.parse_known_args()
        levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]  # [not_possible ,-v, -vv, -vvv]
        try:
            level = levels[args.verbose or 1]
        except IndexError:
            logging.getLogger(__package__).error(f"Invalid verbosity level. Max level is -vvv")
            exit(1)

        yaml_path = './packages/core/utils/log.yaml'
        default_level = logging.DEBUG

        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f.read())
            dictConfig(config)
        else:
            logging.basicConfig(filemode='w', level=default_level)

        logging.getLogger('log_print').setLevel(level)
        logging.getLogger('log_print_full').setLevel(level)
        logging.getLogger('log').setLevel(level)

        logging.getLogger('log_print').warn(f'logging setted : {logging.getLevelName(level)}')
        sys.excepthook = self.handle_exception