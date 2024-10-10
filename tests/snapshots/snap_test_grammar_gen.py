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
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"mode"\' colon start_mode comma \'"title"\' colon start_title comma \'"queries"\' colon start_queries comma \'"related_queries"\' colon start_related_queries comma \'"concepts"\' colon start_concepts comma \'"urls"\' colon start_urls object_end;
start_urls ::= array_begin (start_urls_value (comma start_urls_value)*)? array_end;
start_urls_value ::= string;
start_concepts ::= array_begin (start_concepts_value (comma start_concepts_value)*)? array_end;
start_concepts_value ::= string;
start_related_queries ::= array_begin (start_related_queries_value (comma start_related_queries_value)*)? array_end;
start_related_queries_value ::= start_related_queries_value_0 | start_related_queries_value_1;
start_related_queries_value_1 ::= object_begin \'"foo"\' colon start_related_queries_value_1_foo object_end;
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

snapshots['test_json_schema 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"name"\' colon start_name comma \'"price"\' colon start_price comma \'"tags"\' colon start_tags comma \'"inStock"\' colon start_inStock comma \'"category"\' colon start_category comma \'"sku"\' colon start_sku object_end;
start_sku ::= "\\"ITEM-001\\"";
start_category ::= "\\"electronics\\"" | "114" | "514.1" | null | (array_begin start_category_4_0 comma start_category_4_1 comma start_category_4_2 comma start_category_4_3 array_end) | object_begin start_category_4_0 comma start_category_4_1 comma start_category_4_2 comma start_category_4_3 comma start_category_5_a comma start_category_5_b object_end;
start_category_5_b ::= "2.3";
start_category_5_a ::= "1";
start_category_4_3 ::= "true";
start_category_4_2 ::= "514.1";
start_category_4_1 ::= "514";
start_category_4_0 ::= "\\"114\\"";
start_inStock ::= start_inStock_required?;
start_inStock_required ::= boolean;
start_tags ::= start_tags_required?;
start_tags_required ::= array_begin (start_tags_required_value (comma start_tags_required_value)*)? array_end;
start_tags_required_value ::= start_tags_required_value_0 | start_tags_required_value_1;
start_tags_required_value_1 ::= number;
start_tags_required_value_0 ::= string;
start_price ::= number;
start_name ::= start_tags_required_value;
'''

snapshots['test_pydantic_callable 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
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
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
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
start_c ::= "\\"114\\\'"\\"" | "\\"514\\"" | "true" | "\\"1919\\"" | "\\"810\\"";
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
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"value"\' colon start_value comma \'"next"\' colon start_next object_end;
start_next ::= start_next_0 | start_next_1;
start_next_1 ::= null;
start_next_0 ::= start;
start_value ::= integer;
'''

snapshots['test_pydantic_string_constraints 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"min_length_str"\' colon start_min_length_str comma \'"max_length_str"\' colon start_max_length_str comma \'"pattern_str"\' colon start_pattern_str comma \'"combined_str"\' colon start_combined_str object_end;
start_combined_str ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){2,5}"\';
start_pattern_str ::= #\'"^[a-zA-Z0-9]+$"\';
start_max_length_str ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){0,10}"\';
start_min_length_str ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4}){3,}"\';
'''

snapshots['test_recursive_binary_tree_schema 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"value"\' colon start_value comma \'"left"\' colon start_left comma \'"right"\' colon start_right object_end;
start_right ::= start_right_required?;
start_right_required ::= object_begin \'"value"\' colon start_right_required_value comma \'"left"\' colon start_right_required_left comma \'"right"\' colon start_right_required_right object_end;
start_right_required_right ::= start_right_required_right_required?;
start_right_required_right_required ::= start_right_required;
start_right_required_left ::= start_right_required_left_required?;
start_right_required_left_required ::= object_begin \'"value"\' colon start_right_required_left_required_value comma \'"left"\' colon start_right_required_left_required_left comma \'"right"\' colon start_right_required_left_required_right object_end;
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

snapshots['test_recursive_linked_list_schema 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"value"\' colon start_value comma \'"next"\' colon start_next object_end;
start_next ::= start_next_required?;
start_next_required ::= object_begin \'"value"\' colon start_next_required_value comma \'"next"\' colon start_next_required_next object_end;
start_next_required_next ::= start_next_required_next_required?;
start_next_required_next_required ::= start_next_required;
start_next_required_value ::= integer;
start_value ::= integer;
'''

snapshots['test_schema_with_anchor_reference 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"mainProperty"\' colon start_mainProperty comma \'"referencedObject"\' colon start_referencedObject comma \'"referencedObject2"\' colon start_referencedObject2 object_end;
start_referencedObject2 ::= object_begin \'"subProperty"\' colon start_referencedObject2_subProperty object_end;
start_referencedObject2_subProperty ::= integer;
start_referencedObject ::= object_begin \'"subProperty"\' colon start_referencedObject_subProperty object_end;
start_referencedObject_subProperty ::= integer;
start_mainProperty ::= string;
'''

snapshots['test_schema_with_anyOf_inside_array 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"items"\' colon start_items object_end;
start_items ::= array_begin (start_items_value (comma start_items_value)*)? array_end;
start_items_value ::= start_items_value_0 | start_items_value_1 | start_items_value_2;
start_items_value_2 ::= boolean;
start_items_value_1 ::= object_begin \'"name"\' colon start_items_value_1_name comma \'"value"\' colon start_items_value_1_value object_end;
start_items_value_1_value ::= number;
start_items_value_1_name ::= string;
start_items_value_0 ::= string;
'''

snapshots['test_schema_with_dynamic_ref 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"data"\' colon start_data comma \'"children"\' colon start_children comma \'"metadata"\' colon start_metadata object_end;
start_metadata ::= start_metadata_required?;
start_metadata_required ::= string;
start_children ::= start_children_required?;
start_children_required ::= array_begin (start_children_required_value (comma start_children_required_value)*)? array_end;
start_children_required_value ::= object_begin \'"data"\' colon start_children_required_value_data comma \'"children"\' colon start_children_required_value_children comma \'"metadata"\' colon start_children_required_value_metadata object_end;
start_children_required_value_metadata ::= start_children_required_value_metadata_required?;
start_children_required_value_metadata_required ::= string;
start_children_required_value_children ::= start_children_required_value_children_required?;
start_children_required_value_children_required ::= array_begin (start_children_required_value_children_required_value (comma start_children_required_value_children_required_value)*)? array_end;
start_children_required_value_children_required_value ::= object_begin \'"data"\' colon start_children_required_value_children_required_value_data comma \'"children"\' colon start_children_required_value_children_required_value_children comma \'"metadata"\' colon start_children_required_value_children_required_value_metadata object_end;
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

snapshots['test_schema_with_embedded_schema 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"referencedEmbedded"\' colon start_referencedEmbedded object_end;
start_referencedEmbedded ::= object_begin \'"embeddedProperty"\' colon start_referencedEmbedded_embeddedProperty object_end;
start_referencedEmbedded_embeddedProperty ::= integer;
'''

snapshots['test_schema_with_reference 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= object_begin \'"name"\' colon start_name comma \'"age"\' colon start_age comma \'"address"\' colon start_address object_end;
start_address ::= object_begin \'"street"\' colon start_address_street comma \'"city"\' colon start_address_city comma \'"country"\' colon start_address_country object_end;
start_address_country ::= string;
start_address_city ::= string;
start_address_street ::= string;
start_age ::= integer;
start_name ::= string;
'''

snapshots['test_schema_with_top_level_anyOf 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= start_0 | start_1 | start_2;
start_2 ::= string;
start_1 ::= array_begin (start_1_value (comma start_1_value)*)? array_end;
start_1_value ::= string;
start_0 ::= object_begin \'"name"\' colon start_0_name comma \'"age"\' colon start_0_age object_end;
start_0_age ::= integer;
start_0_name ::= string;
'''

snapshots['test_schema_with_top_level_array 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= array_begin (start_value (comma start_value)*)? array_end;
start_value ::= object_begin \'"id"\' colon start_value_id comma \'"name"\' colon start_value_name comma \'"active"\' colon start_value_active object_end;
start_value_active ::= start_value_active_required?;
start_value_active_required ::= boolean;
start_value_name ::= string;
start_value_id ::= integer;
'''

snapshots['test_schema_with_union_array_object 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
start ::= start_0 | start_1;
start_1 ::= object_begin \'"name"\' colon start_1_name comma \'"age"\' colon start_1_age object_end;
start_1_age ::= start_1_age_required?;
start_1_age_required ::= integer;
start_1_name ::= string;
start_0 ::= array;
'''
