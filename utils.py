from constants import *
import re


def get_color(team: str) -> str:
    """Return a color based on the team."""
    return TEAM_COLORS[team]


def unformat(string, pattern):
    regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)
    values = list(re.search(regex, string).groups())
    keys = re.findall(r'{(.+?)}', pattern)
    _dict = dict(zip(keys, values))
    return _dict
