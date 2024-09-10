# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_vllm_integration 1'] = "Prompt: 'Hello, my name is', Generated text: 'definitely vllm!\\n'"

snapshots['test_vllm_integration 2'] = "Prompt: 'The future of AI is', Generated text: '强大的【VLLM】！！！\\n'"
