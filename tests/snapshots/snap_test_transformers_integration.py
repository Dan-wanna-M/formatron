# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_transformers_batched_inference 1'] = [
    '''<|endoftext|>I am GPT2. Hello, Huggingface!
<|endoftext|>''',
    '''I am another GPT2. Hello, Huggingface!
<|endoftext|>'''
]

snapshots['test_transformers_integration 1'] = [
    '''I am GPT2. Hello, Huggingface!
<|endoftext|>'''
]

snapshots['test_transformers_text_generation_pipeline 1'] = {
    'generated_text': '''I am GPT2. Hello, Huggingface!
'''
}
