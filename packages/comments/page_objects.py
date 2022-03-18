from logging import getLogger

from packages.core.scraper.page_objects import XPathPage

logger = getLogger('log_print')


class CommentsPage(XPathPage):

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
