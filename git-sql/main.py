#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import codecs
import os
import shutil

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

        def __setattr__(self, name, value):
            self[name] = value


MYSQL_URL = (
    'mysql+pymysql://%(user)s:%(passwd)s@%(host)s:%(port)d/%(db)s?'
    'charset=%(charset)s'
)


def _create_engine(db_config):
    # TODO move to v12_config.MYSQLS
    db_config.setdefault('charset', 'utf8')
    return create_engine(
        MYSQL_URL % db_config,
        echo_pool=True,
        echo=db_config.echo,
        pool_size=db_config.pool_size,
        pool_recycle=600
    )


def main():
    with codecs.open('config.json', 'r', 'utf-8') as f:
        config = json.loads(f.read())
        for db, db_config in config.items():
            db_config = ObjectDict(db_config)
            if not os.path.exists(db):
                # init db sql
                os.mkdir(db + '/init')
                # alter table sql
                os.mkdir(db + '/alter')
                # init data sql
                os.mkdir(db + '/data')
            Session = sessionmaker(bind=_create_engine(db_config))
            print len(Session().execute("select * from area").fetchall())


if __name__ == '__main__':
    main()
