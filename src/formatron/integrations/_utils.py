import re
import typing


def _multiple_replace(replacements, text):
    # Create a regular expression from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo:replacements.get(mo.group(), ""), text)


def get_original_whitespace_characters(tokenizer, vocab, chars=None) -> typing.Dict[str, int]:
    # Undo the creepy workarounds for BPE algorithms
    old_char_to_new_char = {}
    if chars is None:
        chars = [" ", "\n", "\t", '\r']
    id2tokens = {v: k for k, v in vocab.items()}
    for char in chars:
        char_ids = tokenizer.encode(char)
        if len(char_ids) != 1:
            continue
        char_id = char_ids[0]
        if char_id is not int: # accounts for one dimensional tensor
            char_id = int(char_id)
        char_token = id2tokens[char_id]

        if char_token != char:
            old_char_to_new_char[char_token] = char
    new_vocab = {}
    for k in vocab:
        new_k = _multiple_replace(old_char_to_new_char, k)
        new_vocab[new_k] = vocab[k]
    return new_vocab
