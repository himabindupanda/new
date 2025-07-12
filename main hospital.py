from datetime import datetime
print("--23--6--25--")

medical_staffs={}
patient= {}


appointment={}
medical_record={}
billing={}

emergency={}

medicine={}
assigned_rooms={}
patient_report={}
discharged_patients={}

hopspital_efficiency=[]
records=[]

def register_patient(patient_id,name,personal_info, medical_history, insurance_info):
    if patient_id in emergency:
        patient[patient_id].update({"name":name,"personal_info":personal_info,"medical_history":medical_history,"insurance_info":insurance_info})
        return
    if patient_id  not in patient:
        patient.update({ patient_id:{"name":name,
                "personal_info":personal_info,
                "medical_history":medical_history,
                "insurance_info":insurance_info}
    })
        print(f"Registration of {patient_id} ID successfull")

    else:
        print("Already Registered")



def add_medical_staff(staff_id, name, specialization, shift_schedule, contact_info):
 if staff_id not in medical_staffs:
   medical_staffs.update({
       staff_id:{"name":name,
            "specialization":specialization,
            "shift_schedule":shift_schedule,
            "contact_info":contact_info}   
   })
   print(f"Medical Staff ('ID'{staff_id}) is added ")
 else:
     print("The Staff already exists")



def schedule_appointment(patient_id, doctor_id, appointment_date, appointment_type):
    appt_datetime = datetime.strptime(appointment_date, "%d-%m-%Y %H:%M")

    if doctor_id not in appointment:
        appointment[doctor_id] = []
    for appt in appointment[doctor_id]:
        existing_time = datetime.strptime(appt["appointment_date"], "%d-%m-%Y %H:%M")
        if existing_time == appt_datetime:
            print("Appointment Conflict")
            return

    if patient_id in patient and doctor_id in medical_staffs:
        appointment[doctor_id].append({
            "patient_id": patient_id,
            "appointment_date": appointment_date,
            "appointment_type": appointment_type
        })
        print(f"""The appointment has been scheduled at {appointment_date}
with {medical_staffs[doctor_id]['name']}""")
        patient[patient_id].update({"doctor":doctor_id})
    else:
        print("Register the patient or doctor first")


def doctors_schedule(doctor_id):
    if doctor_id not in appointment or doctor_id not in medical_staffs:
        print("Doctor not found or has no appointments")
        return

    doctor = medical_staffs[doctor_id]
    print(f"{doctor['name']} - ({doctor['specialization']})")
    today = datetime.today().date()
    print(datetime.strftime(datetime.today(), "%B %d, %Y")) 
    found_today = False
    for appt in appointment[doctor_id]:
        appt_datetime = datetime.strptime(appt["appointment_date"], "%d-%m-%Y %H:%M")
        if appt_datetime.date() == today:
            if not found_today:
                print("Today's Appointments:")
                print("----------------------")
                found_today = True
            print(f"{appt_datetime.strftime('%H:%M')} - Patient ID: {appt['patient_id']} ({appt['appointment_type']})")

    if not found_today:
        print("No appointments today.")





        


def create_medical_record(patient_id, diagnosis, treatment, prescription,doctor_id=101243 ):
 
    for app in appointment[doctor_id]:
        if patient_id == app["patient_id"]:
            medical_record.update({
                patient_id:{"doctor_id":doctor_id, "diagnosis":diagnosis, "treatment":treatment, "prescription":prescription}
            })
            print("Medical record Created")
            break
    else:
        print("Register the patient ")


def manage_emergency_admission(patient_id,admission_date,emergency_type, severity_level):
    emergency.update({
        patient_id:{"emergency_type":emergency_type,"admission_date":admission_date,"severity_level":severity_level}
    })
    patient.update({ patient_id:{"name":None,
                "personal_info":None,
                "medical_history":"Emergency",
                "insurance_info":None}
    })
    
    assigned_rooms.update( {patient_id :{"room_type":"emergency room","admission_date":admission_date,"exp_duaration":None}
                            })
    rooms["emergency room"]["beds"]-=1
    patient[patient_id]["room_type"]="emergency room"
    patient[patient_id["doctor"]]=101243
    
   

def track_medication_inventory(medication_id, quantity, expiry_date, supplier):
    expiry_date=datetime.strptime(expiry_date,"%d-%m-%Y")
    today=datetime.today()
    if expiry_date>=today:
        print("THE MEDICINE HAS EXPIRED")
    else:
        medicine.update({
            medication_id:{"quantity":quantity,"expiry_date":expiry_date,"supplier":supplier}
        })
        print("The Medicine has been added to the inventory!")
rooms={
        "general room":{"beds":20,
        "price":1500},
        "private room":{"beds":15,
        "price":3000},
        "emergency room":{"beds":10,
        "price":5000}
    }    
def assign_room(patient_id, room_type, admission_date, expected_duration):
   
    room_type=room_type.lower()
    if rooms[room_type]["beds"]>0:
        assigned_rooms.update({patient_id:{"room_type":room_type,"admission_date":admission_date,"exp_duaration":expected_duration}})
        rooms[room_type]["beds"]-=1
        patient[patient_id]["room_type"]=room_type
    else:
        print(f"Currently the {room_type} is unavailable Opt for other rooms")


def manage_discharge_process(patient_id,admission_date, discharge_date, follow_up_instructions):
    if patient_id in assigned_rooms:
        room_ty=patient[patient_id]["room_type"]#genrerl room
        rooms[room_ty]["beds"]+=1
        a=patient[patient_id].pop("room_type")
        print(f"The patient has been Discharged from {a} ")
    discharged_patients.update({patient_id:{"discharge_date":discharge_date,"follow_up_instructions":follow_up_instructions}})
    hopspital_efficiency.append({"patient_id":patient_id,"admission_date":admission_date,"discharge_date":discharge_date})


def process_billing(patient_id, services_list, insurance_coverage):
    billing.update({
        patient_id:{
        "service_list":services_list,
        "insurance_coverage":insurance_coverage}
    })
    
    u=assigned_rooms[patient_id]["admission_date"]
    admi_date=datetime.strptime(u, "%d-%m-%Y")
    v=discharged_patients[patient_id]["discharge_date"]
    disc_date=datetime.strptime(v,"%d-%m-%Y")
   
    
    print(f"""=== BILLING SUMMARY ===
Patient: {patient[patient_id]["name"]}
Admission Date: {admi_date.strftime('%B %d,%Y')}
Discharge Date: {disc_date.strftime('%B %d,%Y')}
Service Charges:""")
    for key,value in services_list.items():
        print(f"{key}:{value}")
        
    sum_of_services=sum(cost for services,cost in services_list.items()) 
    Sum_fo_Serices=sum_of_services
    print(f"Total bill : {Sum_fo_Serices}")
    if billing[patient_id]["insurance_coverage"] :
        after_insurance=(billing[patient_id]["insurance_coverage"])/100*Sum_fo_Serices
        print(f"Insurance ({billing[patient_id]["insurance_coverage"]}) : {after_insurance}")
        print(f"patient responsibility : {Sum_fo_Serices-after_insurance}")
    else:
        print("You have no insurance coverage")
        print(f"Patient Responsibility : {Sum_fo_Serices}")

def calculate_treatment_cost(patient_id, treatment_plan, insurance_details):
    ins=insurance_details
    cost=0
    for plan,price in treatment_plan.items():
        cost+=price
        
    admi_date=datetime.strptime(assigned_rooms[patient_id]["admission_date"], "%d-%m-%Y")
    disc_date=datetime.strptime(discharged_patients[patient_id]["discharge_date"],"%d-%m-%Y")
    print(f"""=== BILLING SUMMARY ===
Patient: {patient[patient_id]["name"]}
Admission Date: {datetime.strftime(admi_date, "%B %d, %Y")}
Discharge Date: {datetime.strftime(disc_date, "%B %d, %Y")}""")
    print(f"The cost of the Treatment : {cost}")
    if ins["coverage"]:
        ins_cost=cost*ins["coverage"]/100
        print(f"The insurance coverage {ins["coverage"]} % : {ins_cost}")
        print(f"Patients responsibility :{cost-ins_cost}")
    else:
        print("You have no insurance coverage")
        print(f"Patients Responsibility : {cost}")



def generate_patient_report(patient_id, report_type):
 if patient_id in medical_record:
    patient_report.update({patient_id:report_type})
    print()
    print("---PATIENT REPORT---")
    print(f"""Patient Name : {patient[patient_id]["name"]} ('ID'{patient_id})
Age : {patient[patient_id]["personal_info"]["age"]}| Gender :{patient[patient_id]["personal_info"]["gender"]}| Blood Type : {patient[patient_id]["personal_info"]["blood_type"]}
Insurance : {patient[patient_id]["insurance_info"]["company"]} ('ID'{patient[patient_id]["insurance_info"]["policy_no"]})""")
    if patient_id in discharged_patients:
        status = "Discharged"
    elif patient_id in assigned_rooms:
        status = "Inpatient"
    else :
        status = "Outpatient"
    admi_date=datetime.strptime(assigned_rooms[patient_id]["admission_date"], "%d-%m-%Y")
    print(f"Current Status : {status}")
    print(f"Room : {assigned_rooms[patient_id]["room_type"]}")
    print(f"Admitted : {datetime.strftime(admi_date, "%B %d, %Y")}")
    dis=patient[patient_id]["doctor"]
    doc_name=medical_staffs[dis]["name"]

    print(f"Attending Doctor : {doc_name} ")
    today=datetime.today()
    print(f"Recent Vitals ({datetime.strftime(today,"%B %d, %Y - %H:%M %p")}:)")
    for key,value in report_type.items():
        print(f"{key}:{value}")
    print("Active Medications : ")
    for i in medical_record[patient_id]["prescription"]:
        print(f"{i["medicine"]} ({i["dosage"]}) : {i["frequency"]}")
        
 else:
     print("Create the Medical Record of the pateint")





def analyze_hospital_efficiency(metrics_type, time_period):
    Sum=0
    for i in rooms:
        for j in rooms[i]:
            if j!="price":
                Sum+=rooms[i][j]
    TOTAL_BEDS=Sum
    start_date, end_date = time_period
    start_date = datetime.strptime(start_date, "%d-%m-%Y")
    end_date = datetime.strptime(end_date, "%d-%m-%Y")

    total_stay_days = 0
    total_patients = 0
    occupied_bed_days = 0

    for record in hopspital_efficiency:
        admission = datetime.strptime(record["admission_date"], "%d-%m-%Y")
        discharge = datetime.strptime(record["discharge_date"], "%d-%m-%Y")

        if discharge < start_date or admission > end_date:
            continue
        actual_admission = max(admission, start_date)
        actual_discharge = min(discharge, end_date)
        stay_duration = (actual_discharge - actual_admission).days + 1

        total_stay_days += stay_duration
        total_patients += 1
        occupied_bed_days += stay_duration

    if total_patients == 0:
        print("No patient data available for the selected period.")
        return

    if metrics_type == "average_length_of_stay":
        avg_stay = total_stay_days / total_patients
        print(f"Average Length of Stay: {avg_stay:.2f} days")
    elif metrics_type == "bed_occupancy_rate":
        analysis_days = (end_date - start_date).days + 1
        bed_occupancy_rate = (occupied_bed_days / (TOTAL_BEDS * analysis_days)) * 100
        print(f"Bed Occupancy Rate: {bed_occupancy_rate:.2f}%")
    elif metrics_type == "patient_throughput":
        print(f"Patient Throughput: {total_patients} patients")
    else:
        print("Invalid metrics type. Please choose from: 'average_length_of_stay', 'bed_occupancy_rate', or 'patient_throughput'.")



register_patient(123,"Romi",{"age":21,"gender":"Male","blood_type":"O+"},"Diabetes",{"company":"Star Health","policy_no":92394412})
register_patient(183,"Alex",{"age":27,"gender":"Male","blood_type":"A+"},"Fracture",{"company":"TX Health","policy_no":67677676})

add_medical_staff(101123,"Dr.Subhash Rao","General Doctor",[
    {"day": "Monday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "OPD"},
    {"day": "Tuesday", "shift": "Evening", "start": "14:00", "end": "20:00", "location": "OPD"},
    {"day": "Wednesday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "Wards"},
    {"day": "Thursday", "shift": "Evening", "start": "14:00", "end": "20:00", "location": "Emergency"},
    {"day": "Friday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "OPD"},
    {"day": "Saturday", "shift": "Full Day", "start": "08:00", "end": "20:00", "location": "OPD/Wards"},
    {"day": "Sunday", "shift": "Off", "start": "-", "end": "-", "location": "-"}] , 9929929292)
add_medical_staff(101243,"Dr.Jay Kumar","emergency doctor",[
    {"day": "Monday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "Cardiology OPD"},
    {"day": "Tuesday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "Cardiology Ward"},
    {"day": "Wednesday", "shift": "Evening", "start": "14:00", "end": "20:00", "location": "ICU"},
    {"day": "Thursday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "Cath Lab"},
    {"day": "Friday", "shift": "Full Day", "start": "08:00", "end": "20:00", "location": "OPD & Ward"},
    {"day": "Saturday", "shift": "On Call", "start": "-", "end": "-", "location": "-"},
    {"day": "Sunday", "shift": "Off", "start": "-", "end": "-", "location": "-"}
], 8800978213)
add_medical_staff(101143,"Dr.Santosh","Ortho Surgeon",[
    {"day": "Monday", "shift": "Evening", "start": "14:00", "end": "20:00", "location": "Neuro OPD"},
    {"day": "Tuesday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "Neuro Ward"},
    {"day": "Wednesday", "shift": "Full Day", "start": "08:00", "end": "20:00", "location": "Neurology & ICU"},
    {"day": "Thursday", "shift": "Off", "start": "-", "end": "-", "location": "-"},
    {"day": "Friday", "shift": "Evening", "start": "14:00", "end": "20:00", "location": "Neuro OPD"},
    {"day": "Saturday", "shift": "Morning", "start": "08:00", "end": "14:00", "location": "Neuro Ward"},
    {"day": "Sunday", "shift": "Off", "start": "-", "end": "-", "location": "-"}
], 7800978543)

# schedule_appointment(123, 101123, '1-7-2025 8:00', "Consultation")
# schedule_appointment(123, 101123, '1-7-2025 9:00', "Consultation")
schedule_appointment(183, 101143, '1-7-2025 9:00', "Follow Up")

# doctors_schedule(101123)
doctors_schedule(101143)

# create_medical_record(123, "Type 2 Diabetes Mellitus", "Lifestyle changes, blood sugar monitoring, and oral medications", [
#     {"medicine": "Metformin", "dosage": "500mg", "frequency": "Twice a day"},
#     {"medicine": "Glimepiride", "dosage": "2mg", "frequency": "Once a day"},
# ], 101123)
create_medical_record(183, "hairline tratment in radius bone", "Immobilization,physiotherapy",[
    {"medicine": "Ibuprofen", "dosage": "500mg", "frequency": "Twice a day"},
    {"medicine": "Shelcal", "dosage": "500mg", "frequency": "Once a day"},
] ,101143)

# assign_room(123,"general room","1-7-2025",4)
assign_room(183,"private room","2-7-2025",5)

# manage_discharge_process(123,"1-7-2025","4-7-2025","Eat oil free food")
manage_discharge_process(183,"2-7-2025","7-7-2025","Bed rest and physiotherapy")

# process_billing(123, {
#     "Room Charges(3 days)":4500,
#     "Doctor Charges":2000,
#     "Consultation": 1500,
#     "X-Ray": 800,
#     "Blood Test": 500
# }, 70)
process_billing(183, {
    "Room Charges(5 days)":15000,
    "Doctor Charges":2000,
    "X-Ray": 800,
    "Blood Test": 500,
    "Fracture Plaster (POP)":2500
}, 80)

# generate_patient_report(123,{
#     "blood_test": "Blood Test",
#     "urine_test": "Urine Test",
#     "xray": "X-Ray",
#     "mri": "MRI Scan",
#     "ct_scan": "CT Scan",
#     "ultrasound": "Ultrasound",
#     "ecg": "ECG",
#     "pathology": "Pathology Report",
#     "surgery_summary": "Surgery Summary"
# })
generate_patient_report(183,{
    "blood_test": "Blood Test",
    "xray": "X-Ray",
    "mri": "MRI Scan",
    "ct_scan": "CT Scan",
    "ultrasound": "Ultrasound",
    "ecg": "ECG",
    "surgery_summary": "Surgery Summary"
})

analyze_hospital_efficiency("bed_occupancy_rate",('1-7-2025','7-7-2025'))
import datetime

patients = {}
doctors = {}
appointments = []
medical_staff = {}

def register_patient(patient_id, name, personal_info, medical_history, insurance_info):
    patients[patient_id] = {
        "name": name,
        "personal_info": personal_info,
        "medical_history": medical_history,
        "insurance_info": insurance_info,
        "admitted": True,
        "admission_date": datetime.datetime.now(),
    }
    print(f"Patient {name} registered successfully.")

def discharge_patient(patient_id):
    if patient_id in patients:
        patients[patient_id]["admitted"] = False
        patients[patient_id]["discharge_date"] = datetime.datetime.now()
        print(f"Patient {patients[patient_id]['name']} has been discharged.")
    else:
        print("Patient ID not found.")

def schedule_appointment(patient_id, doctor_id, appointment_date, appointment_type):
    if patient_id not in patients:
        print("Patient not found.")
        return
    if doctor_id not in doctors:
        print("Doctor not found.")
        return
    appointment = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "date": appointment_date,
        "type": appointment_type,
    }
    appointments.append(appointment)
    print(f"Appointment scheduled on {appointment_date} for patient {patient_id} with doctor {doctor_id}.")

def add_medical_staff(staff_id, name, role, department, schedule):
    medical_staff[staff_id] = {
        "name": name,
        "role": role,
        "department": department,
        "schedule": schedule,
    }
    if role.lower() == "doctor":
        doctors[staff_id] = {
            "name": name,
            "specialty": department,
        }
    print(f"{role.title()} {name} added to the system.")

# ------------------ INPUT WRAPPERS ------------------

def input_register_patient():
    patient_id = int(input("Enter patient ID: "))
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    blood_type = input("Enter blood type: ")
    medical_history = input("Enter medical history: ")
    insurance_company = input("Enter insurance company: ")
    policy_no = int(input("Enter insurance policy number: "))

    personal_info = {"age": age, "gender": gender, "blood_type": blood_type}
    insurance_info = {"company": insurance_company, "policy_no": policy_no}

    register_patient(patient_id, name, personal_info, medical_history, insurance_info)

def input_discharge_patient():
    patient_id = int(input("Enter patient ID to discharge: "))
    discharge_patient(patient_id)

def input_schedule_appointment():
    patient_id = int(input("Enter patient ID: "))
    doctor_id = int(input("Enter doctor ID: "))
    appointment_date = input("Enter appointment date (DD-MM-YYYY HH:MM): ")
    appointment_type = input("Enter appointment type: ")
    schedule_appointment(patient_id, doctor_id, appointment_date, appointment_type)

def input_add_medical_staff():
    staff_id = int(input("Enter staff ID: "))
    name = input("Enter staff name: ")
    role = input("Enter role (Doctor/Nurse/etc.): ")
    department = input("Enter department/specialty: ")
    schedule = input("Enter work schedule: ")
    add_medical_staff(staff_id, name, role, department, schedule)

def display_all_patients():
    if not patients:
        print("No patients found.")
    for pid, info in patients.items():
        print(f"\nPatient ID: {pid}")
        print(f"Name: {info['name']}")
        print(f"Admitted: {info['admitted']}")
        print(f"Medical History: {info['medical_history']}")

def display_all_staff():
    if not medical_staff:
        print("No staff records found.")
    for sid, info in medical_staff.items():
        print(f"\nStaff ID: {sid}")
        print(f"Name: {info['name']}")
        print(f"Role: {info['role']}")
        print(f"Department: {info['department']}")

def display_all_appointments():
    if not appointments:
        print("No appointments scheduled.")
    for appt in appointments:
        print(f"\nAppointment - Patient ID: {appt['patient_id']}, Doctor ID: {appt['doctor_id']}")
        print(f"Date: {appt['date']}, Type: {appt['type']}")

# ------------------ MAIN MENU LOOP ------------------

def main():
    while True:
        print("\n=== Hospital Management System ===")
        print("1. Register Patient")
        print("2. Discharge Patient")
        print("3. Schedule Appointment")
        print("4. Add Medical Staff")
        print("5. View All Patients")
        print("6. View All Staff")
        print("7. View All Appointments")
        print("8. Exit")

        choice = input("Select an option (1-8): ")

        if choice == '1':
            input_register_patient()
        elif choice == '2':
            input_discharge_patient()
        elif choice == '3':
            input_schedule_appointment()
        elif choice == '4':
            input_add_medical_staff()
        elif choice == '5':
            display_all_patients()
        elif choice == '6':
            display_all_staff()
        elif choice == '7':
            display_all_appointments()
        elif choice == '8':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid input. Please select a valid option.")


