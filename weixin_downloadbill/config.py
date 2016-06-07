# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser

SETTINGS_FILENAME = 'settings.ini'


def load():
    config = SafeConfigParser()
    config.read(SETTINGS_FILENAME)

    if config.has_section('main'):
        return {
            'appid': config.get('main', 'appid'),
            'mch_id': config.get('main', 'mch_id'),
            'mch_key': config.get('main', 'mch_key'),
            'sub_mch_id': config.get('main', 'sub_mch_id'),
            'path': config.get('main', 'path'),
        }
        
    return {}

def save(appid, mch_id, mch_key, sub_mch_id, path):
    config = SafeConfigParser()

    config.add_section('main')
    config.set('main', 'appid', appid)
    config.set('main', 'mch_id', mch_id)
    config.set('main', 'mch_key', mch_key)
    config.set('main', 'sub_mch_id', sub_mch_id)
    config.set('main', 'path', path)
    
    with open(SETTINGS_FILENAME, 'w') as f:
        config.write(f)
