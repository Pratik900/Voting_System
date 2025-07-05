import dbutils.execute as exe

def has_already_voted(rfid):
    query = f"SELECT * FROM voting_data WHERE RFID = '{rfid}'"
    data = exe.execute_select_query(query)
    return len(data) > 0