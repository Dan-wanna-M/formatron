# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_infer_mapping 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
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
start ::= object_begin \'"mode"\' colon start_mode comma \'"title"\' colon start_title comma \'"queries"\' colon start_queries comma \'"related_queries"\' colon start_related_queries comma \'"concepts"\' colon start_concepts comma \'"urls"\' colon start_urls object_end;
start_urls ::= array_begin (start_urls_value (comma start_urls_value)*)? array_end;
start_urls_value ::= string;
start_concepts ::= array_begin (start_concepts_value (comma start_concepts_value)*)? array_end;
start_concepts_value ::= string;
start_related_queries ::= array_begin (start_related_queries_value (comma start_related_queries_value)*)? array_end;
start_related_queries_value ::= start_related_queries_value_0 | start_related_queries_value_1;
start_related_queries_value_1 ::= string;
start_related_queries_value_0 ::= object_begin \'"foo"\' colon start_related_queries_value_0_foo object_end;
start_related_queries_value_0_foo ::= integer;
start_queries ::= array_begin (start_queries_value (comma start_queries_value)*)? array_end;
start_queries_value ::= start_queries_value_0 | start_queries_value_1 | start_queries_value_2;
start_queries_value_2 ::= integer;
start_queries_value_1 ::= boolean;
start_queries_value_0 ::= string;
start_title ::= string;
start_mode ::= string;
'''

snapshots['test_json_schema 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
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
start ::= start_0 | start_1;
start_1 ::= object_begin \'"name"\' colon start_1_name comma \'"price"\' colon start_1_price comma \'"tags"\' colon start_1_tags comma \'"inStock"\' colon start_1_inStock comma \'"category"\' colon start_1_category comma \'"sku"\' colon start_1_sku object_end;
start_1_sku ::= "\'ITEM-001\'";
start_1_category ::= "\'electronics\'" | "114" | "514.1" | null | (array_begin start_1_category_4_0 comma start_1_category_4_1 comma start_1_category_4_2 comma start_1_category_4_3 array_end) | object_begin start_1_category_4_0 comma start_1_category_4_1 comma start_1_category_4_2 comma start_1_category_4_3 comma start_1_category_5_a comma start_1_category_5_b object_end;
start_1_category_5_b ::= "2.3";
start_1_category_5_a ::= "1";
start_1_category_4_3 ::= "true";
start_1_category_4_2 ::= "514.1";
start_1_category_4_1 ::= "514";
start_1_category_4_0 ::= "\'114\'";
start_1_inStock ::= start_1_inStock_required?;
start_1_inStock_required ::= boolean;
start_1_tags ::= start_1_tags_required?;
start_1_tags_required ::= array_begin (start_1_tags_required_value (comma start_1_tags_required_value)*)? array_end;
start_1_tags_required_value ::= start_1_tags_required_value_0 | start_1_tags_required_value_1;
start_1_tags_required_value_1 ::= number;
start_1_tags_required_value_0 ::= string;
start_1_price ::= number;
start_1_name ::= start_1_tags_required_value;
start_0 ::= number;
'''

snapshots['test_pydantic_callable 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
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
start ::= object_begin \'"a"\' colon start_a comma \'"b"\' colon start_b object_end;
start_b ::= start_b_required?;
start_b_required ::= integer;
start_a ::= integer;
'''

snapshots['test_pydantic_class 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
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
start ::= object_begin \'"a"\' colon start_a comma \'"b"\' colon start_b comma \'"c"\' colon start_c comma \'"e"\' colon start_e comma \'"f"\' colon start_f object_end;
start_f ::= start_f_0 | start_f_1 | start_f_2 | start_f_3 | start_f_4;
start_f_4 ::= array_begin (start_f_4_value (comma start_f_4_value)*)? array_end;
start_f_4_value ::= integer;
start_f_3 ::= integer;
start_f_2 ::= json_value;
start_f_1 ::= integer;
start_f_0 ::= boolean;
start_e ::=array_begin start_e_0 comma start_e_1 comma start_e_2 comma start_e_3 comma start_e_4 array_end;
start_e_4 ::= object_begin (string colon start_e_4_value (comma string colon start_e_4_value)*)? object_end;
start_e_4_value ::= start_f_2;
start_e_3 ::= object_begin (string colon start_e_3_value (comma string colon start_e_3_value)*)? object_end;
start_e_3_value ::= start_f_2;
start_e_2 ::= number;
start_e_1 ::= string;
start_e_0 ::= array_begin (start_e_0_value (comma start_e_0_value)*)? array_end;
start_e_0_value ::= number;
start_c ::= "\'114\\\'"\'" | "\'514\'" | "true" | "\'1919\'" | "\'810\'";
start_b ::= start_b_required?;
start_b_required ::= integer;
start_a ::= start_a_required?;
start_a_required ::= string;
'''

snapshots['test_pydantic_class_linked_list 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
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
start ::= object_begin \'"value"\' colon start_value comma \'"next"\' colon start_next object_end;
start_next ::= start_next_0 | start_next_1;
start_next_1 ::= null;
start_next_0 ::= start;
start_value ::= integer;
'''
