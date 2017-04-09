import sqlite3
import codecs

def insert_records(records):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    table_name = 'doz'
    try:
        c.execute("CREATE  TABLE  " + table_name + " (  title TEXT, description  TEXT,  url TEXT  );")
    except Exception as e:
        print("already exists? :", e)
    c.execute("SELECT url FROM " + table_name + "")
    all_articles = c.fetchall()
    error_counter = 0
    news_counter = 0
    updates_counter = 0
    errors = {}
    for record in records:
        try:
            print("first try", record['source_url'])
            print((record['source_url'],) not in all_articles)
            print(all_articles)
            if (record['source_url'],) not in all_articles:
                if record['title']:
                    # print('record  ', record)
                    # print('record  ', record['source_url'])

                    executeString = """INSERT INTO """ + table_name + """ VALUES ('{title}','{description}', '{source_url}')""".format(
                        title=record['title'], description=record['description'], source_url=record['source_url'])
                    execute = codecs.escape_decode(bytes(executeString, "utf-8"))[0].decode("utf-8")
                    print(execute)
                    c.execute(execute)
                    news_counter += 1
            else:
                c.execute("UPDATE " + table_name + " SET description='" + record['description'] + "' WHERE url='" +
                          record['source_url'] + "'")
                updates_counter += 1
        except Exception as e:
            error_counter += 1
            print("błąd: ", e)
            # errors[]
            # errors[record['source_url']] = e
    c.execute("SELECT title FROM " + table_name + "")
    print(c.fetchall())
    conn.commit()
    conn.close()
    print("Problemy: ", errors)
    print("Zebrano: ", news_counter)
    print("Zmodyfikowano: ", updates_counter)
    print("Problemów: ", error_counter)
