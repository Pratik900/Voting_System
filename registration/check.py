import dbutils.execute as exe

def is_rfid_registered(rfid):
    query = f"SELECT COUNT(*) FROM registration WHERE RFID = '{rfid}';"
    result = exe.execute_select_query(query)
    return result[0][0] > 0