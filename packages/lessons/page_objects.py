from logging import getLogger
from packages.core.scraper.page_objects import BasicPage
from packages.core.utils.datetime import str_to_seg

logger = getLogger('log_print')


class LessonsPage(BasicPage):
    type_page = 'lessons'

    @property
    def titles(self):
        return self._get_property('titles')

    @property
    def paths(self):
        return self._get_property('paths')

    @property
    def durations(self):
        return map(str_to_seg, self._get_property('durations'))


class CommentsPage(BasicPage):
    type_page = 'comments'

    @property
    def as_list(self):
        return map(format, self._state)
    
    def _format(self, comment_as_dict):
        return {
            'author': {
                **comment_as_dict['author'],
                'username': avatar_to_username(comment_as_dict['author']['avatar']),
            },
            'content': html_to_text(comment_as_dict['content']),
            'likes': int(comment_as_dict['likes']),
            'written_at': timestamp_to_datetime(comment_as_dict['written_at']),
            'external_id': comment_as_dict['external_id'],
        }
