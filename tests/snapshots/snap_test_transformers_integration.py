# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_transformers_batched_inference 1'] = [
    '''<|endoftext|><|endoftext|>I am GPT2. Hello, Huggingface!
<|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|>''',
    '''<|endoftext|>I am another GPT2. Hello, Huggingface!
<|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|>''',
    '''I am yet another GPT2. Hello, Huggingface! Hello, Huggingface!
<|endoftext|>'''
]

snapshots['test_transformers_integration 1'] = [
    '''I am GPT2. Hello, Huggingface!
<|endoftext|>'''
]

snapshots['test_transformers_sparse_formatters 1'] = [
    '<|endoftext|><|endoftext|>I am GPT2. \xa0I am GPT3. \xa0I am GPT4. \xa0I am GPT5. \xa0I am GPT6. \xa0I am GPT7. \xa0I am GPT8. \xa0I am GPT9. \xa0I am GPT10. \xa0I am GPT11. \xa0I am GPT12. \xa0I am GPT13. \xa0I am GPT14. \xa0I am G',
    '''<|endoftext|>I am another GPT2. Hello, Huggingface!
<|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|>''',
    'I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. \xa0I am a third GPT2. ',
    '''I am a fourth GPT2. Hello, Huggingface!
<|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|><|endoftext|>''',
    'I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. \xa0I am a fifth GPT2. '
]

snapshots['test_transformers_text_generation_pipeline 1'] = {
    'generated_text': '''I am GPT2. Hello, Huggingface!
'''
}
