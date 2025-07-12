# Sample data stores
patients = {}
staff = {}
appointments = []
medical_records = []
billings = []
emergencies = []
med_inventory = {}
room_assignments = {}
discharges = []
occupied_rooms = set()


def register_patient(patient_id, personal_info, medical_history, insurance_info):
    patients[patient_id] = {
        "personal_info": personal_info,
        "medical_history": medical_history,
        "insurance_info": insurance_info,
        "records": [],
        "appointments": [],
        "vitals": {},
        "medications": []
    }
    print(f"Patient {patient_id} registered successfully.")


def add_medical_staff(staff_id, name, specialization, shift_schedule, contact_info):
    staff[staff_id] = {
        "name": name,
        "specialization": specialization,
        "shift_schedule": shift_schedule,
        "contact_info": contact_info
    }
    print(f"Staff {staff_id} added successfully.")


def schedule_appointment(patient_id, doctor_id, appointment_date, appointment_type):
    if doctor_id not in staff:
        print("Doctor not available.")
        return
    appointments.append({
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "date": appointment_date,
        "type": appointment_type
    })
    patients[patient_id]['appointments'].append(appointment_date)
    print(f"Appointment scheduled for patient {patient_id} with doctor {doctor_id}.")


def create_medical_record(patient_id, doctor_id, diagnosis, treatment, prescription):
    record = {
        "doctor_id": doctor_id,
        "diagnosis": diagnosis,
        "treatment": treatment,
        "prescription": prescription
    }
    patients[patient_id]['records'].append(record)
    patients[patient_id]['medications'] = prescription
    medical_records.append(record)
    print(f"Medical record created for patient {patient_id}.")


def process_billing(patient_id, services_list, insurance_coverage):
    total_cost = sum(service['cost'] for service in services_list)
    coverage_amount = int(total_cost * insurance_coverage)
    patient_due = total_cost - coverage_amount
    bill = {
        "patient_id": patient_id,
        "services": services_list,
        "total_cost": total_cost,
        "insurance_coverage": coverage_amount,
        "amount_due": patient_due
    }
    billings.append(bill)
    print("=== BILLING SUMMARY ===")
    print(f"Patient: {patient_id}")
    print("Service Charges:")
    for service in services_list:
        print(f"{service['name']}: {service['cost']}")
    print(f"\nTotal bill: {total_cost}")
    print(f"Insurance coverage({int(insurance_coverage*100)}%): {coverage_amount}")
    print(f"Patient responsibility: {patient_due}\n")
    return bill


def manage_emergency_admission(patient_id, emergency_type, severity_level):
    if patient_id not in patients:
        print("Unregistered patient. Registering for emergency.")
        register_patient(patient_id, {}, [], {})
    emergencies.append({
        "patient_id": patient_id,
        "type": emergency_type,
        "severity": severity_level
    })
    print(f"Emergency admission recorded for patient {patient_id}.")


def track_medication_inventory(medication_id, quantity, expiry_date, supplier):
    med_inventory[medication_id] = {
        "quantity": quantity,
        "expiry_date": expiry_date,
        "supplier": supplier
    }
    print(f"Medication {medication_id} inventory updated.")


def assign_room(patient_id, room_type, admission_date, expected_duration):
    if room_type in occupied_rooms:
        print("Room occupancy conflict. No available rooms of this type.")
        return
    room_assignments[patient_id] = {
        "room_type": room_type,
        "admission_date": admission_date,
        "expected_duration": expected_duration
    }
    occupied_rooms.add(room_type)
    print(f"Room assigned to patient {patient_id}.")


def calculate_treatment_cost(patient_id, treatment_plan, insurance_details):
    total = sum(item['cost'] for item in treatment_plan)
    covered = int(total * insurance_details.get("coverage_percent", 0))
    due = total - covered
    print(f"Total: {total}, Covered: {covered}, Due: {due}")
    return {
        "total": total,
        "covered": covered,
        "due": due
    }


def generate_patient_report(patient_id, report_type):
    patient = patients.get(patient_id, {})
    room = room_assignments.get(patient_id, {})
    if report_type == "dashboard":
        info = patient.get("personal_info", {})
        print("=== PATIENT DASHBOARD ===")
        print(f"Patient: {info.get('name')} (ID: {patient_id})")
        print(f"Age: {info.get('age')} | Gender: {info.get('gender')} | Blood Type: {info.get('blood_type')}")
        insurance = patient.get("insurance_info", {})
        print(f"Insurance: {insurance.get('provider')} (Policy: {insurance.get('policy_number')})")
        print("Current Status: Inpatient")
        print(f"Room: {room.get('room_type')}\nAdmitted: {room.get('admission_date')}")
        if patient['records']:
            doctor_id = patient['records'][-1]['doctor_id']
            print(f"Attending Doctor: {staff[doctor_id]['name']} ({staff[doctor_id]['specialization']})")
        print("Recent Vitals:")
        for k, v in patient['vitals'].items():
            print(f"{k}: {v}")
        print("Active Medications:")
        for med in patient['medications']:
            print(f"- {med}")


def analyze_hospital_efficiency(metrics_type, time_period):
    if metrics_type == "appointments":
        count = len([appt for appt in appointments if appt['date'] in time_period])
        print(f"Appointments in period: {count}")
        return count
    elif metrics_type == "admissions":
        count = len([room for room in room_assignments.values() if room['admission_date'] in time_period])
        print(f"Admissions in period: {count}")
        return count
    return 0


def manage_discharge_process(patient_id, discharge_date, follow_up_instructions):
    discharge = {
        "patient_id": patient_id,
        "discharge_date": discharge_date,
        "follow_up": follow_up_instructions
    }
    discharges.append(discharge)
    room_type = room_assignments[patient_id]['room_type']
    if room_type in occupied_rooms:
        occupied_rooms.remove(room_type)
    print(f"Patient {patient_id} discharged successfully.")


# Step 1: Register patient
register_patient("P12345", {
    "name": "Prasanna kumar",
    "age": 45,
    "gender": "Male",
    "blood_type": "B+"
}, [], {
    "provider": "Star Health",
    "policy_number": "SH789456",
    "coverage_percent": 0.80
})

# Step 2: Add doctor
add_medical_staff("D100", "Dr. Sanjana satapathy ", "Cardiology", "Day", "1234567890")

# Step 3: Assign room
assign_room("P12345", "204-A (General Ward)", "March 15, 2025", 3)

# Step 4: Create medical record
create_medical_record("P12345", "D100", "Hypertension", "Routine monitoring", [
    "Metoprolol 50mg - Twice daily",
    "Aspirin 75mg - Once daily",
    "Atorvastatin 20mg - Bedtime"
])

# Step 5: Record vitals manually
patients["P12345"]["vitals"] = {
    "Blood Pressure": "130/85 mmHg",
    "Heart Rate": "78 BPM",
    "Temperature": "98.6°F",
    "Oxygen Saturation": "97%"
}

# Step 6: Generate patient dashboard
generate_patient_report("P12345", "dashboard")

# Step 7: Process billing
process_billing("P12345", [
    {"name": "Room Charges (3 days)", "cost": 4500},
    {"name": "Doctor Consultation", "cost": 2000},
    {"name": "ECG test", "cost": 800},
    {"name": "Blood tests", "cost": 1200},
    {"name": "Medication", "cost": 1800},
    {"name": "Nursing care", "cost": 2400}
], 0.80)

# Step 8: Discharge
manage_discharge_process("P12345", "March 18, 2025", "Follow up in 2 weeks")


