# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_formatter 1'] = '''__regex_0_0 ::= #'[0-9]+';
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
__schema_json_0 ::= object_begin 'a' colon __schema_json_0_a comma 'b' colon __schema_json_0_b comma 'c' colon __schema_json_0_c comma 'e' colon __schema_json_0_e comma 'f' colon __schema_json_0_f object_end;
__schema_json_0_f ::= __schema_json_0_f_0 | __schema_json_0_f_1 | __schema_json_0_f_2 | __schema_json_0_f_3 | __schema_json_0_f_4;
__schema_json_0_f_4 ::= array_begin (__schema_json_0_f_4_value (comma __schema_json_0_f_4_value)*)? array_end;
__schema_json_0_f_4_value ::= integer;
__schema_json_0_f_3 ::= integer;
__schema_json_0_f_2 ::= json_value;
__schema_json_0_f_1 ::= integer;
__schema_json_0_f_0 ::= boolean;
__schema_json_0_e ::=array_begin __schema_json_0_e_0 comma __schema_json_0_e_1 comma __schema_json_0_e_2 comma __schema_json_0_e_3 comma __schema_json_0_e_4 array_end;
__schema_json_0_e_4 ::= object_begin (string colon __schema_json_0_e_4_value (comma string colon __schema_json_0_e_4_value)*)? object_end;
__schema_json_0_e_4_value ::= json_value;
__schema_json_0_e_3 ::= object_begin (string colon __schema_json_0_e_3_value (comma string colon __schema_json_0_e_3_value)*)? object_end;
__schema_json_0_e_3_value ::= json_value;
__schema_json_0_e_2 ::= number;
__schema_json_0_e_1 ::= string;
__schema_json_0_e_0 ::= array_begin (__schema_json_0_e_0_value (comma __schema_json_0_e_0_value)*)? array_end;
__schema_json_0_e_0_value ::= number;
__schema_json_0_c ::= \'114\\\'"\' | \'514\' | \'True\' | \'1919\' | \'810\';
__schema_json_0_b ::= __schema_json_0_b_required?;
__schema_json_0_b_required ::= integer;
__schema_json_0_a ::= __schema_json_0_a_required?;
__schema_json_0_a_required ::= string;

__str_1_0_excepted ::= '.';
__str_1_0 ::= except!(__str_1_0_excepted)('.');
start ::= 'This is a number: ' __regex_0_0 '\\n' 'This is a json: ' __schema_json_0 '\\n' 'Multiple indentations\\nare handled\\n    correctly. This is a random sentence: ' __str_1_0;'''
