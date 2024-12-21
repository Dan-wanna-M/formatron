# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_exllamav2_batched_inference 1'] = [
    '''Hello, cats! Hello, Exllamav2!
''',
    '''Hello, dogs! Hello, Exllamav2!
'''
]

snapshots['test_exllamav2_integration 1'] = '''Hello, cats! Hello, Exllamav2!
'''

snapshots['test_exllamav2_json_schema 1'] = '''Using the given JSON schema, give me an emotion from the following text: 
Ugggghhh, why do you have to be such a jerk!{ "emotion": "angry" }
'''

snapshots['test_exllamav2_utf_8 1'] = '''Hello, cats! 你好，土豆！
'''
