#import psycopg2


conn = psycopg2.connect("dbname=POS user=postgres password=Leong73292H")


# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test2 (Account_Name text PRIMARY KEY, Password text);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
    #(100, "abc'def"))

# Query the database and obtain data as Python objects
def record_test():
    cur.execute("SELECT * FROM test2")

    record = cur.fetchall()
    print(record)
    print((record[1])[1])
    for row in record:
        print("Account Name =", row[0],)
        print("Account Level =", row[2], "\n")
def update_test():
    cur.execute("UPDATE test2 SET account_level = 3 WHERE account_name = 'test'")

#record_test()

update_test()




# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

'''
UPDATE test2
SET account_level = 1
WHERE account_name = 'test'
'''