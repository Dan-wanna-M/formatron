# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_infer_mapping 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"mode"\' colon start_mode comma #\'[ \t
]*"title"\' colon start_title comma #\'[ \t
]*"queries"\' colon start_queries comma #\'[ \t
]*"related_queries"\' colon start_related_queries comma #\'[ \t
]*"concepts"\' colon start_concepts comma #\'[ \t
]*"urls"\' colon start_urls object_end;
start_urls ::= array_begin (start_urls_value (comma start_urls_value)*)? array_end;
start_urls_value ::= string;
start_concepts ::= array_begin (start_concepts_value (comma start_concepts_value)*)? array_end;
start_concepts_value ::= string;
start_related_queries ::= array_begin (start_related_queries_value (comma start_related_queries_value)*)? array_end;
start_related_queries_value ::= start_related_queries_value_0 | start_related_queries_value_1;
start_related_queries_value_1 ::= object_begin #'[ \t
]*"foo"\' colon start_related_queries_value_1_foo object_end;
start_related_queries_value_1_foo ::= integer;
start_related_queries_value_0 ::= string;
start_queries ::= array_begin (start_queries_value (comma start_queries_value)*)? array_end;
start_queries_value ::= start_queries_value_0 | start_queries_value_1 | start_queries_value_2;
start_queries_value_2 ::= boolean;
start_queries_value_1 ::= string;
start_queries_value_0 ::= integer;
start_title ::= string;
start_mode ::= string;
'''

snapshots['test_json_schema 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"name"\' colon start_name comma #\'[ \t
]*"price"\' colon start_price comma #\'[ \t
]*"tags"\' colon start_tags comma #\'[ \t
]*"inStock"\' colon start_inStock comma #\'[ \t
]*"category"\' colon start_category comma #\'[ \t
]*"sku"\' colon start_sku object_end;
start_sku ::= #'[ \t
]*"ITEM-001"\';
start_category ::= #'[ \t
]*"electronics"\' | #"[ \t
]*114" | #"[ \t
]*514.1" | null | (array_begin start_category_4_0 comma start_category_4_1 comma start_category_4_2 comma start_category_4_3 array_end) | object_begin start_category_4_0 comma start_category_4_1 comma start_category_4_2 comma start_category_4_3 comma start_category_5_a comma start_category_5_b object_end;
start_category_5_b ::= #"[ \t
]*2.3";
start_category_5_a ::= #"[ \t
]*1";
start_category_4_3 ::= #"[ \t
]*true";
start_category_4_2 ::= #"[ \t
]*514.1";
start_category_4_1 ::= #"[ \t
]*514";
start_category_4_0 ::= #'[ \t
]*"114"\';
start_inStock ::= start_inStock_required?;
start_inStock_required ::= boolean;
start_tags ::= start_tags_required?;
start_tags_required ::= array_begin  comma start_tags_required_item+ array_end;
start_tags_required_item ::= json_value;
start_price ::= #'[ \t
]*0|[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_name ::= start_name_0 | start_name_1;
start_name_1 ::= number;
start_name_0 ::= string;
'''

snapshots['test_json_schema_array_min_max_items_constraints 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"min_items_array"\' colon start_min_items_array comma #\'[ \t
]*"max_items_array"\' colon start_max_items_array comma #\'[ \t
]*"min_max_items_array"\' colon start_min_max_items_array object_end;
start_min_max_items_array_min ::= start_min_max_items_array_item;
start_min_max_items_array ::= array_begin start_min_max_items_array_min comma start_min_max_items_array_item array_end;
start_min_max_items_array ::= array_begin start_min_max_items_array_min comma start_min_max_items_array_item comma start_min_max_items_array_item array_end;
start_min_max_items_array ::= array_begin start_min_max_items_array_min comma start_min_max_items_array_item comma start_min_max_items_array_item comma start_min_max_items_array_item array_end;
start_min_max_items_array_item ::= json_value;
start_max_items_array ::= array_begin  array_end;
start_max_items_array ::= array_begin start_max_items_array_item array_end;
start_max_items_array ::= array_begin start_max_items_array_item comma start_max_items_array_item array_end;
start_max_items_array ::= array_begin start_max_items_array_item comma start_max_items_array_item comma start_max_items_array_item array_end;
start_max_items_array_item ::= json_value;
start_min_items_array ::= array_begin start_min_items_array_item comma start_min_items_array_item+ array_end;
start_min_items_array_item ::= json_value;
'''

snapshots['test_json_schema_array_prefix_items 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"2_5_prefix_items"\' colon start_2_5_prefix_items comma #\'[ \t
]*"1_4_prefix_items"\' colon start_1_4_prefix_items comma #\'[ \t
]*"3__prefix_items"\' colon start_3__prefix_items comma #\'[ \t
]*"0_4_prefix_items"\' colon start_0_4_prefix_items comma #\'[ \t
]*"simple_prefix_items"\' colon start_simple_prefix_items object_end;
start_simple_prefix_items ::= array_begin array_end;
start_simple_prefix_items ::= array_begin start_simple_prefix_items_item_0 (comma start_simple_prefix_items_item)* array_end;
start_simple_prefix_items_item ::= json_value;
start_simple_prefix_items_item_0 ::= string;
start_0_4_prefix_items ::= array_begin array_end;
start_0_4_prefix_items ::= array_begin start_0_4_prefix_items_item_0 array_end;
start_0_4_prefix_items_min ::= start_0_4_prefix_items_item_0;
start_0_4_prefix_items ::= array_begin start_0_4_prefix_items_min comma start_0_4_prefix_items_item array_end;
start_0_4_prefix_items ::= array_begin start_0_4_prefix_items_min comma start_0_4_prefix_items_item comma start_0_4_prefix_items_item array_end;
start_0_4_prefix_items ::= array_begin start_0_4_prefix_items_min comma start_0_4_prefix_items_item comma start_0_4_prefix_items_item comma start_0_4_prefix_items_item array_end;
start_0_4_prefix_items_item ::= json_value;
start_0_4_prefix_items_item_0 ::= string;
start_3__prefix_items ::= array_begin start_3__prefix_items_item_0 comma start_3__prefix_items_item_1  comma start_3__prefix_items_item+ array_end;
start_3__prefix_items_item ::= json_value;
start_3__prefix_items_item_1 ::= number;
start_3__prefix_items_item_0 ::= string;
start_1_4_prefix_items ::= array_begin start_1_4_prefix_items_item_0 array_end;
start_1_4_prefix_items ::= array_begin start_1_4_prefix_items_item_0 comma start_1_4_prefix_items_item_1 array_end;
start_1_4_prefix_items_min ::= start_1_4_prefix_items_item_0 comma start_1_4_prefix_items_item_1;
start_1_4_prefix_items ::= array_begin start_1_4_prefix_items_min comma start_1_4_prefix_items_item array_end;
start_1_4_prefix_items ::= array_begin start_1_4_prefix_items_min comma start_1_4_prefix_items_item comma start_1_4_prefix_items_item array_end;
start_1_4_prefix_items_item ::= json_value;
start_1_4_prefix_items_item_1 ::= number;
start_1_4_prefix_items_item_0 ::= string;
start_2_5_prefix_items ::= array_begin start_2_5_prefix_items_item_0 comma start_2_5_prefix_items_item_1 array_end;
start_2_5_prefix_items ::= array_begin start_2_5_prefix_items_item_0 comma start_2_5_prefix_items_item_1 comma start_2_5_prefix_items_item_2 array_end;
start_2_5_prefix_items_min ::= start_2_5_prefix_items_item_0 comma start_2_5_prefix_items_item_1 comma start_2_5_prefix_items_item_2;
start_2_5_prefix_items_item ::= json_value;
start_2_5_prefix_items_item_2 ::= boolean;
start_2_5_prefix_items_item_1 ::= number;
start_2_5_prefix_items_item_0 ::= string;
'''

snapshots['test_json_schema_integer_constraints 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"gt_int"\' colon start_gt_int comma #\'[ \t
]*"ge_int"\' colon start_ge_int comma #\'[ \t
]*"lt_int"\' colon start_lt_int comma #\'[ \t
]*"le_int"\' colon start_le_int object_end;
start_le_int ::= #'[ \t
]*0|-[1-9][0-9]*';
start_lt_int ::= #'[ \t
]*-[1-9][0-9]*';
start_ge_int ::= #'[ \t
]*0|[1-9][0-9]*';
start_gt_int ::= #'[ \t
]*[1-9][0-9]*';
'''

snapshots['test_json_schema_number_constraints 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"gt_number"\' colon start_gt_number comma #\'[ \t
]*"ge_number"\' colon start_ge_number comma #\'[ \t
]*"lt_number"\' colon start_lt_number comma #\'[ \t
]*"le_number"\' colon start_le_number object_end;
start_le_number ::= #'[ \t
]*0|-[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_lt_number ::= #'[ \t
]*-[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_ge_number ::= #'[ \t
]*0|[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_gt_number ::= #'[ \t
]*[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
'''

snapshots['test_json_schema_object_without_properties 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object;
'''

snapshots['test_json_schema_substring_constraint 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"substring_str"\' colon start_substring_str object_end;
start_substring_str ::= #'[ \t
]*\' \'"\' #substrs\'Hello, world!\' \'"\';
'''

snapshots['test_pydantic_callable 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"a"\' colon start_a comma #\'[ \t
]*"b"\' colon start_b object_end;
start_b ::= start_b_required?;
start_b_required ::= integer;
start_a ::= integer;
'''

snapshots['test_pydantic_class 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"a"\' colon start_a comma #\'[ \t
]*"b"\' colon start_b comma #\'[ \t
]*"c"\' colon start_c comma #\'[ \t
]*"e"\' colon start_e comma #\'[ \t
]*"f"\' colon start_f object_end;
start_f ::= start_f_0 | start_f_1 | start_f_2 | start_f_3 | start_f_4;
start_f_4 ::= array_begin (start_f_4_value (comma start_f_4_value)*)? array_end;
start_f_4_value ::= integer;
start_f_3 ::= integer;
start_f_2 ::= json_value;
start_f_1 ::= integer;
start_f_0 ::= boolean;
start_e ::=array_begin start_e_0 comma start_e_1 comma start_e_2 comma start_e_3 comma start_e_4 array_end;
start_e_4 ::= object;
start_e_3 ::= object;
start_e_2 ::= number;
start_e_1 ::= string;
start_e_0 ::= array_begin (start_e_0_value (comma start_e_0_value)*)? array_end;
start_e_0_value ::= number;
start_c ::= #'[ \t
]*"114\\\'""\' | #\'[ \t
]*"514"\' | #"[ \t
]*true" | #\'[ \t
]*"1919"\' | #\'[ \t
]*"810"\';
start_b ::= start_b_required?;
start_b_required ::= integer;
start_a ::= start_a_required?;
start_a_required ::= string;
'''

snapshots['test_pydantic_class_linked_list 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"value"\' colon start_value comma #\'[ \t
]*"next"\' colon start_next object_end;
start_next ::= start_next_0 | start_next_1;
start_next_1 ::= null;
start_next_0 ::= start;
start_value ::= integer;
'''

snapshots['test_pydantic_float_constraints 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"gt_float"\' colon start_gt_float comma #\'[ \t
]*"ge_float"\' colon start_ge_float comma #\'[ \t
]*"lt_float"\' colon start_lt_float comma #\'[ \t
]*"le_float"\' colon start_le_float comma #\'[ \t
]*"positive_float"\' colon start_positive_float comma #\'[ \t
]*"negative_float"\' colon start_negative_float comma #\'[ \t
]*"nonnegative_float"\' colon start_nonnegative_float comma #\'[ \t
]*"nonpositive_float"\' colon start_nonpositive_float object_end;
start_nonpositive_float ::= #'[ \t
]*0|-[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_nonnegative_float ::= #'[ \t
]*0|[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_negative_float ::= #'[ \t
]*-[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_positive_float ::= #'[ \t
]*[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_le_float ::= #'[ \t
]*0|-[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_lt_float ::= #'[ \t
]*-[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_ge_float ::= #'[ \t
]*0|[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_gt_float ::= #'[ \t
]*[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
'''

snapshots['test_pydantic_integer_constraints 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"gt_int"\' colon start_gt_int comma #\'[ \t
]*"ge_int"\' colon start_ge_int comma #\'[ \t
]*"lt_int"\' colon start_lt_int comma #\'[ \t
]*"le_int"\' colon start_le_int comma #\'[ \t
]*"positive_int"\' colon start_positive_int comma #\'[ \t
]*"negative_int"\' colon start_negative_int comma #\'[ \t
]*"nonnegative_int"\' colon start_nonnegative_int comma #\'[ \t
]*"nonpositive_int"\' colon start_nonpositive_int object_end;
start_nonpositive_int ::= #'[ \t
]*0|-[1-9][0-9]*';
start_nonnegative_int ::= #'[ \t
]*0|[1-9][0-9]*';
start_negative_int ::= #'[ \t
]*-[1-9][0-9]*';
start_positive_int ::= #'[ \t
]*[1-9][0-9]*';
start_le_int ::= #'[ \t
]*0|-[1-9][0-9]*';
start_lt_int ::= #'[ \t
]*-[1-9][0-9]*';
start_ge_int ::= #'[ \t
]*0|[1-9][0-9]*';
start_gt_int ::= #'[ \t
]*[1-9][0-9]*';
'''

snapshots['test_pydantic_sequence_constraints 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"min_2_list"\' colon start_min_2_list comma #\'[ \t
]*"max_5_list"\' colon start_max_5_list comma #\'[ \t
]*"min_1_max_3_list"\' colon start_min_1_max_3_list comma #\'[ \t
]*"min_2_tuple"\' colon start_min_2_tuple comma #\'[ \t
]*"max_5_tuple"\' colon start_max_5_tuple comma #\'[ \t
]*"min_1_max_3_tuple"\' colon start_min_1_max_3_tuple comma #\'[ \t
]*"empty_list"\' colon start_empty_list object_end;
start_empty_list_item ::= array_begin (start_empty_list_item_value (comma start_empty_list_item_value)*)? array_end;
start_empty_list_item_value ::= json_value;
start_min_1_max_3_tuple_min ::= start_min_1_max_3_tuple_item;
start_min_1_max_3_tuple ::= array_begin start_min_1_max_3_tuple_min comma start_min_1_max_3_tuple_item array_end;
start_min_1_max_3_tuple ::= array_begin start_min_1_max_3_tuple_min comma start_min_1_max_3_tuple_item comma start_min_1_max_3_tuple_item array_end;
start_min_1_max_3_tuple_item ::= number;
start_max_5_tuple ::= array_begin  array_end;
start_max_5_tuple ::= array_begin start_max_5_tuple_item array_end;
start_max_5_tuple ::= array_begin start_max_5_tuple_item comma start_max_5_tuple_item array_end;
start_max_5_tuple ::= array_begin start_max_5_tuple_item comma start_max_5_tuple_item comma start_max_5_tuple_item array_end;
start_max_5_tuple ::= array_begin start_max_5_tuple_item comma start_max_5_tuple_item comma start_max_5_tuple_item comma start_max_5_tuple_item array_end;
start_max_5_tuple ::= array_begin start_max_5_tuple_item comma start_max_5_tuple_item comma start_max_5_tuple_item comma start_max_5_tuple_item comma start_max_5_tuple_item array_end;
start_max_5_tuple_item ::= string;
start_min_2_tuple ::= array_begin start_min_2_tuple_item comma start_min_2_tuple_item+ array_end;
start_min_2_tuple_item ::= integer;
start_min_1_max_3_list_min ::= start_min_1_max_3_list_item;
start_min_1_max_3_list ::= array_begin start_min_1_max_3_list_min comma start_min_1_max_3_list_item array_end;
start_min_1_max_3_list ::= array_begin start_min_1_max_3_list_min comma start_min_1_max_3_list_item comma start_min_1_max_3_list_item array_end;
start_min_1_max_3_list_item ::= number;
start_max_5_list ::= array_begin  array_end;
start_max_5_list ::= array_begin start_max_5_list_item array_end;
start_max_5_list ::= array_begin start_max_5_list_item comma start_max_5_list_item array_end;
start_max_5_list ::= array_begin start_max_5_list_item comma start_max_5_list_item comma start_max_5_list_item array_end;
start_max_5_list ::= array_begin start_max_5_list_item comma start_max_5_list_item comma start_max_5_list_item comma start_max_5_list_item array_end;
start_max_5_list ::= array_begin start_max_5_list_item comma start_max_5_list_item comma start_max_5_list_item comma start_max_5_list_item comma start_max_5_list_item array_end;
start_max_5_list_item ::= string;
start_min_2_list ::= array_begin start_min_2_list_item comma start_min_2_list_item+ array_end;
start_min_2_list_item ::= integer;
'''

snapshots['test_pydantic_string_constraints 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"min_length_str"\' colon start_min_length_str comma #\'[ \t
]*"max_length_str"\' colon start_max_length_str comma #\'[ \t
]*"pattern_str"\' colon start_pattern_str comma #\'[ \t
]*"combined_str"\' colon start_combined_str object_end;
start_combined_str ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){2,5}"\';
start_pattern_str ::= #'[ \t
]*"[a-zA-Z0-9]+"\';
start_max_length_str ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){0,10}"\';
start_min_length_str ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){3,}"\';
'''

snapshots['test_pydantic_substring_constraint 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"substring_str"\' colon start_substring_str object_end;
start_substring_str ::= string;
'''

snapshots['test_recursive_binary_tree_schema 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"value"\' colon start_value comma #\'[ \t
]*"left"\' colon start_left comma #\'[ \t
]*"right"\' colon start_right object_end;
start_right ::= start_right_required?;
start_right_required ::= object_begin #'[ \t
]*"value"\' colon start_right_required_value comma #\'[ \t
]*"left"\' colon start_right_required_left comma #\'[ \t
]*"right"\' colon start_right_required_right object_end;
start_right_required_right ::= start_right_required_right_required?;
start_right_required_right_required ::= start_right_required;
start_right_required_left ::= start_right_required_left_required?;
start_right_required_left_required ::= object_begin #'[ \t
]*"value"\' colon start_right_required_left_required_value comma #\'[ \t
]*"left"\' colon start_right_required_left_required_left comma #\'[ \t
]*"right"\' colon start_right_required_left_required_right object_end;
start_right_required_left_required_right ::= start_right_required_left_required_right_required?;
start_right_required_left_required_right_required ::= start_right_required;
start_right_required_left_required_left ::= start_right_required_left_required_left_required?;
start_right_required_left_required_left_required ::= start_right_required_left_required;
start_right_required_left_required_value ::= number;
start_right_required_value ::= number;
start_left ::= start_left_required?;
start_left_required ::= start_right_required_left_required;
start_value ::= number;
'''

snapshots['test_recursive_linked_list_schema 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"value"\' colon start_value comma #\'[ \t
]*"next"\' colon start_next object_end;
start_next ::= start_next_required?;
start_next_required ::= object_begin #'[ \t
]*"value"\' colon start_next_required_value comma #\'[ \t
]*"next"\' colon start_next_required_next object_end;
start_next_required_next ::= start_next_required_next_required?;
start_next_required_next_required ::= start_next_required;
start_next_required_value ::= integer;
start_value ::= integer;
'''

snapshots['test_schema_with_anchor_reference 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"mainProperty"\' colon start_mainProperty comma #\'[ \t
]*"referencedObject"\' colon start_referencedObject comma #\'[ \t
]*"referencedObject2"\' colon start_referencedObject2 object_end;
start_referencedObject2 ::= object_begin #'[ \t
]*"subProperty"\' colon start_referencedObject2_subProperty object_end;
start_referencedObject2_subProperty ::= integer;
start_referencedObject ::= object_begin #'[ \t
]*"subProperty"\' colon start_referencedObject_subProperty object_end;
start_referencedObject_subProperty ::= integer;
start_mainProperty ::= string;
'''

snapshots['test_schema_with_anyOf_inside_array 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"items"\' colon start_items object_end;
start_items ::= array_begin (start_items_value (comma start_items_value)*)? array_end;
start_items_value ::= start_items_value_0 | start_items_value_1 | start_items_value_2;
start_items_value_2 ::= boolean;
start_items_value_1 ::= object_begin #'[ \t
]*"name"\' colon start_items_value_1_name comma #\'[ \t
]*"value"\' colon start_items_value_1_value object_end;
start_items_value_1_value ::= number;
start_items_value_1_name ::= string;
start_items_value_0 ::= string;
'''

snapshots['test_schema_with_dynamic_ref 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"data"\' colon start_data comma #\'[ \t
]*"children"\' colon start_children comma #\'[ \t
]*"metadata"\' colon start_metadata object_end;
start_metadata ::= start_metadata_required?;
start_metadata_required ::= string;
start_children ::= start_children_required?;
start_children_required ::= array_begin (start_children_required_value (comma start_children_required_value)*)? array_end;
start_children_required_value ::= object_begin #'[ \t
]*"data"\' colon start_children_required_value_data comma #\'[ \t
]*"children"\' colon start_children_required_value_children comma #\'[ \t
]*"metadata"\' colon start_children_required_value_metadata object_end;
start_children_required_value_metadata ::= start_children_required_value_metadata_required?;
start_children_required_value_metadata_required ::= string;
start_children_required_value_children ::= start_children_required_value_children_required?;
start_children_required_value_children_required ::= array_begin (start_children_required_value_children_required_value (comma start_children_required_value_children_required_value)*)? array_end;
start_children_required_value_children_required_value ::= object_begin #'[ \t
]*"data"\' colon start_children_required_value_children_required_value_data comma #\'[ \t
]*"children"\' colon start_children_required_value_children_required_value_children comma #\'[ \t
]*"metadata"\' colon start_children_required_value_children_required_value_metadata object_end;
start_children_required_value_children_required_value_metadata ::= start_children_required_value_children_required_value_metadata_required?;
start_children_required_value_children_required_value_metadata_required ::= string;
start_children_required_value_children_required_value_children ::= start_children_required_value_children_required_value_children_required?;
start_children_required_value_children_required_value_children_required ::= array_begin (start_children_required_value_children_required_value_children_required_value (comma start_children_required_value_children_required_value_children_required_value)*)? array_end;
start_children_required_value_children_required_value_children_required_value ::= start_children_required_value_children_required_value;
start_children_required_value_children_required_value_data ::= start_children_required_value_children_required_value_data_required?;
start_children_required_value_children_required_value_data_required ::= string;
start_children_required_value_data ::= start_children_required_value_data_required?;
start_children_required_value_data_required ::= string;
start_data ::= start_data_required?;
start_data_required ::= string;
'''

snapshots['test_schema_with_embedded_schema 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"referencedEmbedded"\' colon start_referencedEmbedded object_end;
start_referencedEmbedded ::= object_begin #'[ \t
]*"embeddedProperty"\' colon start_referencedEmbedded_embeddedProperty object_end;
start_referencedEmbedded_embeddedProperty ::= integer;
'''

snapshots['test_schema_with_reference 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"name"\' colon start_name comma #\'[ \t
]*"age"\' colon start_age comma #\'[ \t
]*"address"\' colon start_address object_end;
start_address ::= object_begin #'[ \t
]*"street"\' colon start_address_street comma #\'[ \t
]*"city"\' colon start_address_city comma #\'[ \t
]*"country"\' colon start_address_country object_end;
start_address_country ::= string;
start_address_city ::= string;
start_address_street ::= string;
start_age ::= integer;
start_name ::= string;
'''

snapshots['test_schema_with_reference_to_number 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"mainProperty"\' colon start_mainProperty comma #\'[ \t
]*"numberReference"\' colon start_numberReference object_end;
start_numberReference ::= #'[ \t
]*0|[1-9][0-9]*(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?';
start_mainProperty ::= string;
'''

snapshots['test_schema_with_string_metadata 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= object_begin #'[ \t
]*"username"\' colon start_username comma #\'[ \t
]*"email"\' colon start_email comma #\'[ \t
]*"description"\' colon start_description comma #\'[ \t
]*"password"\' colon start_password object_end;
start_password ::= #'[ \t
]*".*[A-Za-z].*"\';
start_description ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){0,200}"\';
start_email ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){3,}"\';
start_username ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){3,20}"\';
'''

snapshots['test_schema_with_top_level_anyOf 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= start_0 | start_1 | start_2;
start_2 ::= string;
start_1 ::= array_begin (start_1_value (comma start_1_value)*)? array_end;
start_1_value ::= string;
start_0 ::= object_begin #'[ \t
]*"name"\' colon start_0_name comma #\'[ \t
]*"age"\' colon start_0_age object_end;
start_0_age ::= integer;
start_0_name ::= string;
'''

snapshots['test_schema_with_top_level_array 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= array_begin  comma start_item+ array_end;
start_item ::= json_value;
'''

snapshots['test_schema_with_union_array_object 1'] = '''integer ::= #"[ \t
]*-?(0|[1-9][0-9]*)";
number ::= #"[ \t
]*-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #'[ \t
]*"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= #"[ \t
]*(true|false)";
null ::= #"[ \t
]*null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
]*,";
colon ::= #"[ \t
]*:";
object_begin ::= #"[ \t
]*\\\\{";
object_end ::= #"[ \t
]*\\\\}";
array_begin ::= #"[ \t
]*\\\\[";
array_end ::= #"[ \t
]*\\\\]";
start ::= start_0 | start_1;
start_1 ::= object_begin #'[ \t
]*"name"\' colon start_1_name comma #\'[ \t
]*"age"\' colon start_1_age object_end;
start_1_age ::= start_1_age_required?;
start_1_age_required ::= integer;
start_1_name ::= string;
start_0 ::= array_begin (start_0_value (comma start_0_value)*)? array_end;
start_0_value ::= string;
'''
