from flask import Flask, request,render_template,session
from registration.create import insert_registration
from registration.retrieve import get_all_registrations,get_name_prn
from registration.check import is_rfid_registered

from voting.create1 import insert_vote
from voting.check1 import has_already_voted 

#from voting.utils import get_prn_by_rfid


from response import create_response

srv = Flask(__name__)


hardware_data = {"RFID": None, "Finger_Print": None}


@srv.route("/")
def home():
    show_flag = 0  # or 0 depending on your backend logic
    return render_template("home.html", show_register_form=show_flag)


@srv.route("/register-form")
def register_form():
    return render_template("register.html")



# ------------------ Registration ------------------
@srv.route("/registration", methods=["GET", "POST", "PUT"])
def registration():
    if request.method == "GET":
        return create_response(get_all_registrations())

    elif request.method == "POST":
        data = request.get_json()
        RFID = data.get("RFID")
        Finger_Print = data.get("Finger_Print")

        # Save hardware data in memory
        hardware_data["RFID"] = RFID
        hardware_data["Finger_Print"] = Finger_Print

        print("Received hardware data:", hardware_data)
        return create_response("Hardware data received, waiting for user input")

    elif request.method == "PUT":
        data = request.get_json()
        PRN_NO = data.get("PRN_NO")
        Name = data.get("Name")

        if not all([PRN_NO, Name]):
            return create_response("Missing PRN_NO, Name", status="fail")

        query = f"""
        UPDATE registration
        SET PRN_NO = '{PRN_NO}', Name = '{Name}'
        WHERE PRN_NO IS NULL AND Name IS NULL;
        """

        import dbutils.execute as exe
        exe.execute_query(query)
        return create_response("Student info updated successfully")

    
# ------------------ Hardware Data Storage ------------------
@srv.route("/check-hardware")
def check_hardware():
    if hardware_data["RFID"] and hardware_data["Finger_Print"]:
        return {"show": 1}
    return {"show": 0}


@srv.route("/cancel-registration", methods=["POST"])
def cancel_registration():
    hardware_data["RFID"] = None
    hardware_data["Finger_Print"] = None
    print("Registration cancelled. Hardware data cleared.")
    return '', 204  # No Content




@srv.route("/submit-form", methods=["POST"])
def submit_form():
    name = request.form.get("name")
    prn = request.form.get("prn")

    RFID = hardware_data.get("RFID")
    Finger_Print = hardware_data.get("Finger_Print")

    if not (RFID and Finger_Print):
        return create_response("Missing hardware data", status="fail")

    if is_rfid_registered(RFID):
        return create_response("RFID already registered", status="fail")

    insert_registration(prn, name, RFID, Finger_Print)

    # Clear stored hardware data
    hardware_data["RFID"] = None
    hardware_data["Finger_Print"] = None

    return render_template("home.html", show_register_form=0)



# @srv.route("/registration", methods=["GET", "POST"])
# def registration():
#     if request.method == "GET":
#         return create_response(get_all_registrations())
    
#     elif request.method == "POST":
#         data = request.get_json()
#         PRN_NO = data.get("PRN_NO")
#         Name = data.get("Name")
#         RFID = data.get("RFID")
#         Finger_Print = data.get("Finger_Print")

#         if is_rfid_registered(RFID):
#             return create_response("RFID already registered", status="fail")
        
#         insert_registration(PRN_NO, Name, RFID, Finger_Print)
#         return create_response("Student registered successfully")

# ------------------ Voting ------------------

@srv.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    RFID = data.get("RFID")
    Selected_Candidate = data.get("Selected_Candidate")

    if has_already_voted(RFID):
        return create_response("Already Voted", status="fail")

    # Optional: fetch PRN from RFID (if needed)
    from voting.utils import get_prn_by_rfid
    PRN_NO = get_prn_by_rfid(RFID)

    insert_vote(PRN_NO, RFID, Selected_Candidate)
    return create_response("Vote submitted successfully")

# ------------------ Check Vote Status ------------------

@srv.route("/vote/status/<rfid>", methods=["GET"])
def check_vote_status(rfid):
    if has_already_voted(rfid):
        return create_response("Already Voted", status="fail")
    return create_response("Not Voted", status="ok")

# ------------------ Run Server ------------------

if __name__ == "__main__":
    srv.run(host="0.0.0.0", port=5000, debug=True)
