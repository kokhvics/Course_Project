import psycopg2

conn = psycopg2.connect(database = 'Smarty', user = 'postgres', host = 'localhost', port = '5432', password = '123')
print("done")