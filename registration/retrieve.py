import dbutils.execute as exe

def get_all_registrations():
    query = "SELECT PRN_NO, Name, RFID, Finger_Print FROM registration;"
    return exe.execute_select_query(query)


def get_name_prn():
    name = input("Enter your name: ")

    prn = input("Enter your prn: ")

    return name,prn