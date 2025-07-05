import dbutils.execute as exe

def get_prn_by_rfid(rfid):
    query = f"SELECT PRN_NO FROM registration WHERE RFID = '{rfid}'"
    data = exe.execute_select_query(query)
    if data:
        return data[0][0]
    return None
