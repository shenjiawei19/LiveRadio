# -*- coding: utf-8 -*-


class UserManage(object):

    def __init__(self):
        self._permission = None

    @property
    def permission(self):
        return self._permission

    @permission.setter
    def permission(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._permission = value

