from relational import relation, parser, rtypes
from relational import maintenance
ui = maintenance.UserInterface()

relation_input = '''
Employees (EID, Name, Age) = {
E1, John, 32
E2, Alice, 28
E3, Bob, 29
}
Poop (EID, Name, Age) = {
E1, John, 32
E2, Alice, 28
E3, Bob, 29
}
'''

query_input = 'select Age>30(Employees)'
input = relation_input.split('\n')[1:-1]
placeholder = -1

def divide_chunks(l, n):  
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def replacements(query: str) -> str:
    '''This function replaces ascii easy operators with the correct ones'''
    rules = (
        ('join', parser.JOIN),
        ('left_join', parser.JOIN_LEFT),
        ('right_join', parser.JOIN_RIGHT),
        ('full_join', parser.JOIN_FULL),
        ('project', parser.PROJECTION),
        ('select', parser.SELECTION),
        ('rename', parser.RENAME),
    )
    for asciiop, op in rules:
        query = query.replace(asciiop, op)
    return query

for i in range(0, len(input)):
     if input[i]=='}':
          title = input[placeholder+1]
          name = title[0:title.index(' ')]
          attributes = title[title.index('(')+1:title.index(')')]
          attributes = attributes.split(', ')
          temp_relation = ", ".join(input[placeholder+2:i])
          temp_relation = temp_relation.split(', ')
          temp_relation = list(divide_chunks(temp_relation, len(attributes)))
          placeholder = i
          ui.set_relation(name, relation.Relation.create_from(attributes, temp_relation))
query_input = replacements(query_input)
print(query_input)
pyquery = parser.parse(query_input)
print(ui.relations)
result = pyquery(ui.relations)
print(result.pretty_string(tty=True))