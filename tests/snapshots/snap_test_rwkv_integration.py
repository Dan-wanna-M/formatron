# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_rwkv_integration 1'] = '''Hello, RWKV!
'''

snapshots['test_rwkv_integration 2'] = '''Hello, RWKV!
'''
