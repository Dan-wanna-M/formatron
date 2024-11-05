# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_formatter 1'] = '''__choice_0_0_food ::= 'railroad' | 'orange' | 'banana';
__regex_1_0 ::= #'[0-9]+';
__regex_2_0 ::= #'[a-z]+';
__choice_3_0_ID ::= __regex_1_0 | __regex_2_0;
integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
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
__json_4_0_json ::= object_begin \'"name"\' colon __json_4_0_json_name comma \'"weight"\' colon __json_4_0_json_weight comma \'"color"\' colon __json_4_0_json_color object_end;
__json_4_0_json_color ::= string;
__json_4_0_json_weight ::= number;
__json_4_0_json_name ::= string;

start ::= \'Today, I want to eat \' __choice_0_0_food \'\\n\' "My food\'s ID is " __choice_3_0_ID \'.\\n\' "\\nWhat\'s more, indentations\\nare handled\\nappropriately." \'My weight is 14.4kg and my color is pink. This is my personal info json: \' __json_4_0_json \'\\n\';'''

snapshots['test_formatter 2'] = '''Today, I want to eat orange
My food's ID is orange.

What's more, indentations
are handled
appropriately.My weight is 14.4kg and my color is pink. This is my personal info json: { \t"name": "Van",\t"weight": 1,\t"color": "pink"}
'''

snapshots['test_formatter 3'] = {
    'ID': GenericRepr("<re.Match object; span=(0, 6), match='orange'>"),
    'food': 'orange',
    'json': GenericRepr("Test(name='Van', weight=1.0, color='pink')")
}

snapshots['test_formatter_alternate_accept 1'] = {
    'age': GenericRepr("<re.Match object; span=(0, 2), match='30'>"),
    'name': GenericRepr("<re.Match object; span=(0, 5), match='John,'>")
}

snapshots['test_formatter_callable_schema 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
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
__json_0_0_json ::= object_begin \'"a"\' colon __json_0_0_json_a comma \'"b"\' colon __json_0_0_json_b comma \'"c"\' colon __json_0_0_json_c object_end;
__json_0_0_json_c ::= integer;
__json_0_0_json_b ::= integer;
__json_0_0_json_a ::= integer;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_callable_schema 2'] = '''{"a":1,"b":2,"c":3}
'''

snapshots['test_formatter_callable_schema 3'] = {
    'json': 6
}

snapshots['test_formatter_dict_inference 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
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
__json_0_0_json ::= object_begin \'"name"\' colon __json_0_0_json_name comma \'"gender"\' colon __json_0_0_json_gender object_end;
__json_0_0_json_gender ::= string;
__json_0_0_json_name ::= string;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_dict_inference 2'] = '{"name":"这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字这是一个json: 我的名字'

snapshots['test_formatter_dict_inference 3'] = {
}

snapshots['test_formatter_json_no_properties 1'] = {
    'data': {
        'key': 'value',
        'number': 42
    }
}

snapshots['test_formatter_json_schema 1'] = '''{"name":"calibur","age":120}
'''

snapshots['test_formatter_json_schema 2'] = {
    'json': {
        'age': 120,
        'name': 'calibur'
    }
}

snapshots['test_formatter_json_schema 3'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
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
__json_0_0_json ::= object_begin \'"name"\' colon __json_0_0_json_name comma \'"age"\' colon __json_0_0_json_age object_end;
__json_0_0_json_age ::= integer;
__json_0_0_json_name ::= string;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_regex_complement 1'] = '''__regex_complement_0_0_non_numeric ::= #ex'[0-9]';
__regex_1_0_numeric ::= #'[0-9]+';
start ::= 'Text: ' __regex_complement_0_0_non_numeric 'Number: ' __regex_1_0_numeric '\\n';'''

snapshots['test_formatter_regex_complement 2'] = '''Text: THERE IS A BIG SCREEN OF THE LIFE AND DEATH OF JEAN GILLETTE

Assistant: There is a big screen of the life and death of Jean Gillette.
Jean Gillette was a French actor, director, and producer who died at the age of eighty-one. He was best known for his role as Louis XIV in the musical comedy The Life and Death of Jeanne D'Arc. Gillette was born on June\xa0I,\xa0in\xa0Paris, France. He started his career as a stage actor in the late nineteenth century, but his popularity skyrocketed when he appeared in films such as The Life and Death of Jack the Ripper and The Life and Death of Count Dracula. Gillette's performances were praised by critics and audiences alike, and he became a household name.
The life and death of Jean Gillette is a tragic tale that has inspired countless films, plays, and novels over the years. The story follows the life of Jean Gillette, a French actor who was famous for his role as Louis XIV in the musical comedy The Life and Death of Jack the Ripper. The story revolves around a young woman named Jeanne D'Arc, who is accused of murder'''

snapshots['test_formatter_regex_complement 3'] = {
    'non_numeric': 'Hello, world! Number: ',
    'numeric': GenericRepr("<re.Match object; span=(0, 2), match='42'>")
}

snapshots['test_formatter_regex_complement 4'] = {
    'non_numeric': 'Hello, world! Number: ',
    'numeric': GenericRepr("<re.Match object; span=(0, 2), match='42'>")
}

snapshots['test_formatter_str 1'] = '''__str_0_0 ::= #'.*?(?:\\\\.)';
start ::= __str_0_0 '\\n';'''

snapshots['test_formatter_str 2'] = '\uf06eI\'m the prince of ice. I was once a king, but my father was killed by my brother. I\'m the son of the Frost King, who took me from my mother and forced me to marry his daughter. I\'m now a prince, but my mother was murdered by my father. I\'m the king\'s son, but I\'m a prince too. I want to be the best at everything. I want to be a king. But I don\'t know how to fight. I don\'t know how to kill people. I don\'t know how to speak the language of ice." Van said. He looked at each of them with his eyes filled with pain and fear. He was scared, but he also knew that he had to be brave. "Van, you can do this," Prince Hal said. "I\'ll help you," Van said, and he stood up and walked towards Hal and the others. "Hal, you\'re going to be my best friend," Van said as he smiled. Hal smiled back and hugged Van. "You\'ll be my best friend too," Hal said. "And I\'m not just talking about your magic," Van added. "I know that you\'re not just talking about magic," Hal said, and'

snapshots['test_formatter_str 3'] = {
}

snapshots['test_formatter_substr 1'] = '''__substr_0_0_substr ::= #substrs'Name: Umbrella; Price: 114.514 dollars;';
start ::= __substr_0_0_substr '<eos>';'''

snapshots['test_formatter_substr 2'] = ' 114.514 dollars;<eos>'

snapshots['test_formatter_substr 3'] = {
    'substr': ' 114.514 dollars;'
}

snapshots['test_formatter_top_level_array_json_schema 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
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
__json_0_0_json_min ::= __json_0_0_json_item;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item array_end;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item comma __json_0_0_json_item array_end;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item comma __json_0_0_json_item comma __json_0_0_json_item array_end;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item comma __json_0_0_json_item comma __json_0_0_json_item comma __json_0_0_json_item array_end;
__json_0_0_json_item ::= json_value;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_top_level_array_json_schema 2'] = '''[{"name": "John", "age": 30}, {"name": "Jane", "age": 30}, {"name": "Mary", "age": 40}]
'''

snapshots['test_formatter_top_level_array_json_schema 3'] = {
    'json': [
        {
            'age': 30,
            'name': 'John'
        },
        {
            'age': 30,
            'name': 'Jane'
        },
        {
            'age': 40,
            'name': 'Mary'
        }
    ]
}

snapshots['test_grammar_literal 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
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
__json_0_0_json ::= object_begin \'"a"\' colon __json_0_0_json_a object_end;
__json_0_0_json_a ::= "\\"114\\"" | "\\"514\\"";

start ::= __json_0_0_json '\\n';'''

snapshots['test_grammar_literal 2'] = '''{"a":"114"}
'''

snapshots['test_grammar_literal 3'] = {
    'json': GenericRepr("A(a='114')")
}
