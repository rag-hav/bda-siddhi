from info import streams
threshold = 100
print('''@App:name('AlertsApp')

define stream AlertStream (timestamp long, value double, alertMessage string); 
''')

for name in streams:
    print(f'''define stream {name} (timestamp long, value double); ''')

print('''@sink(type='log')
@info(name='alerts')
from AlertStream
select *
insert into AlertStreamTemp;
''')

for name in streams:
    print(f'''@sink(type='log')
@info(name='query_{name}')
from {name}[value > {threshold}]
select timestamp, value, 'Alert: {name} value is greater than static threshold' as alertMessage
insert into AlertStream;
''')
