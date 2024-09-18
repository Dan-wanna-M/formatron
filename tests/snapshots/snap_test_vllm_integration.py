# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_vllm_integration 1'] = "Prompt: 'Hello, my name is', Generated text: 'definitely vllm!\\n'"

snapshots['test_vllm_integration 2'] = "Prompt: 'The future of AI is', Generated text: '强大的【VLLM】！！！\\n'"

snapshots['test_vllm_integration_sparse 1'] = "Prompt: 'The first prompt is', Generated text: 'formatted with vllm!\\n'"

snapshots['test_vllm_integration_sparse 2'] = "Prompt: 'The second prompt is', Generated text: ' a list of all the items in the list.\\n\\nThe third prompt is a list of all the items in the list.\\n\\nThe fourth prompt is a list of all the items in the list.\\n\\nThe fifth prompt is a list'"

snapshots['test_vllm_integration_sparse 3'] = "Prompt: 'The third prompt is', Generated text: 'also formatted but is slightly longer!\\n'"

snapshots['test_vllm_integration_sparse 4'] = 'Prompt: \'The fourth prompt is\', Generated text: \' a "I\\\'m sorry" prompt.\\n\\nThe fifth prompt is a "I\\\'m sorry" prompt.\\n\\nThe sixth prompt is a "I\\\'m sorry" prompt.\\n\\nThe seventh prompt is a "I\\\'m sorry" prompt.\''
