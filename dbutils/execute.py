# import module connecction to create connection
import dbutils.connection as conn


def execute_query(query):
    # get connection of mysql
    connection =  conn.get_connection()

    # get cursor to execute query
    cursor = connection.cursor()

    # execute the query
    cursor.execute(query)

    # commit your changes
    connection.commit()

    # close the cursor
    cursor.close()

    # close the connection
    connection.close()

def execute_select_query(query):
    # get connection of mysql
    connection = conn.get_connection()

    # create a cursor
    cursor = connection.cursor()

    # execute a select query
    cursor.execute(query)

    # fetch data from  cursor
    data = cursor.fetchall()

    # close the cursor
    cursor.close()

    # close the connection
    connection.close()

    # return your data(result)
    return data