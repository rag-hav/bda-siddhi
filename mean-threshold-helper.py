from info import streams
window = 10 
percent = 10
percentchange = 1.1
print('''@App:name('AlertsApp')

define stream AlertStream (timestamp long, value double, alertMessage string); 
''')

for name in streams:
    print(f'''define stream {name} (timestamp long, attribute double); ''')

print('''@sink(type='log')
@info(name='alerts')
from AlertStream
select *
insert into AlertStreamTemp;
''')


for name in streams:
    print(f'''

from {name}#window.length(10)

select attribute, avg(attribute) as mean
insert into {name}TempStream;

@sink(type='log')
@info(name='query_{name}')

from {name} as i join {name}TempStream as t
on i.attribute > t.mean * 1.1

select timestamp, i.attribute as value, 'Alert: {name} value is greater than {percent}% of last {window} values' as alertMessage
insert into AlertStream;
''')
