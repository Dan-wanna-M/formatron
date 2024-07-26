# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_formatter 1'] = '''__choice_food_0 ::= 'railroad' | 'orange' | 'banana';
__regex_0_0 ::= #'[0-9]+';
__regex_1_0 ::= #'[a-z]+';
__choice_ID_0 ::= __regex_0_0 | __regex_1_0;
integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*,(\\u0020|\\u000A|\\u000D|\\u0009)*";
colon ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*:(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_begin ::= #"\\\\{(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\}";
array_begin ::= #"\\\\[(\\u0020|\\u000A|\\u000D|\\u0009)*";
array_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\]";
__schema_json_0 ::= object_begin 'name' colon __schema_json_0_name comma 'weight' colon __schema_json_0_weight comma 'color' colon __schema_json_0_color object_end;
__schema_json_0_color ::= string;
__schema_json_0_weight ::= number;
__schema_json_0_name ::= string;

start ::= \'Today, I want to eat \' __choice_food_0 \'\\n\' "My food\'s ID is " __choice_ID_0 \'.\\n\' "\\nWhat\'s more, indentations\\nare handled\\nappropriately." \'Let me give you a random json: \' __schema_json_0 \'\\n\';'''

snapshots['test_formatter 2'] = '''Today, I want to eat orange
My food's ID is orange.

What's more, indentations
are handled
appropriately.Let me give you a random json: { name : "Van" , weight : 100 , color : "red" }'''

snapshots['test_formatter 3'] = {
    'ID': GenericRepr("<re.Match object; span=(0, 6), match='orange'>"),
    'food': 'orange',
    'json': '{ name : "Van" , weight : 100 , color : "red" }'
}
