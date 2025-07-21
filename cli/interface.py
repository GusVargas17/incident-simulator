from core.dispatcher import (
    register_incident,
    get_pending_incident,
    assign_incident,
    start_incident,
    resolve_incident,
    escalate_incident,
    get_resolved_incidents,
    get_escalated_incidents
)
from core.operators import OPERATORS

def handle_register():
    print("\n--- Register Incident ---")
    type_ = input("Incident type (network/software/hardware/ux/security): ")
    priority = input("Priority (low/medium/high): ").strip().lower()
    description = input("Description: ").strip()

    incident = register_incident(type_, priority, description)
    print(f"✅ Incident registered with ID: {incident.id}")

def handle_view_pending():
    print("\n--- Pending Incidents ---")
    pending = get_pending_incident()
    if not pending:
        print("No pending incidents")
    else:
        for i in pending:
            print(f"ID: {i.id} | Type: {i.type} | Priority: {i.priority} | Status: {i.status} | Assigned to: {i.assigned_to}")

def handle_assign():
    print("\n--- Assign Incident ---")
    try:
        incident_id = input("Incident ID to assign: ")
        assign_incident(incident_id)
        print("✅ Incident assigned.")
    except ValueError as m:
        print(f"Error: {m}")

def handle_start():
    print("\n--- Start Incident ---")
    try:
        incident_id = input("Incident ID to start: ")
        operator_name = input("Operator name: ").strip()

        start_incident(incident_id, operator_name)
        print("✅ Incident started.")
    except ValueError as m:
        print(f"Error: {m}")

def handle_resolve():
    print("\n--- Resolve Incident ---")
    try:
        incident_id = input("Incident ID to resolve: ")
        operator_name = input("Operator name: ").strip()

        resolve_incident(incident_id, operator_name)
        print("✅ Incident resolved.")
    except ValueError as m:
        print(f"Error: {m}")

def handle_escalate():
    print("\n--- Escalate Incident ---")
    try:
        incident_id = input("Incident ID to escalate: ").strip()
        reason = input("Reason for escalation: ").strip()

        if not reason:
            print("❌ Escalation reason is required.")
            return

        escalate_incident(incident_id, reason)
        print("✅ Incident escalated.")
    except ValueError as m:
        print(f"Error: {m}")

def handle_view_resolved():
    print("\n--- Resolved Incidents ---")
    resolved = get_resolved_incidents()
    if not resolved:
        print("No resolved incidents.")
    else:
        for i in resolved:
            print(f"ID: {i.id} | Resolved by: {i.assigned_to} | Status: {i.status}")

def handle_view_escalated():
    escalated = get_escalated_incidents()
    print("\n=== ESCALATED INCIDENTS ===")
    if not escalated:
        print("No escalated incidents found.")
    for i in escalated:
        print(f"ID: {i.id}, Type: {i.type}, Priority: {i.priority}, Assigned: {i.assigned_to}, Status: {i.status}")


def pause():
    input("\nPress ENTER to continue..")

def main_menu():
    while True:
        print("\n=== INCIDENT MANAGER ===")
        print("1. Register Incident")
        print("2. View Pending Incidents")
        print("3. Assign Incident")
        print("4. Start Incident")
        print("5. Resolve Incident")
        print("6. Escalate Incident")
        print("7. View Resolved Incidents")
        print("8. View Escalated Incidents")
        print("9. Exit")

        choice = input("Choose an option (1-9): ")

        try:
            if choice == "1":
                handle_register()
                pause()
            elif choice == "2":
                handle_view_pending()
                pause()
            elif choice == "3":
                handle_assign()
                pause()
            elif choice == "4":
                handle_start()
                pause()
            elif choice == "5":
                handle_resolve()
                pause()
            elif choice == "6":
                handle_escalate()
                pause()
            elif choice == "7":
                handle_view_resolved()
                pause()
            elif choice == "8":
                handle_view_escalated()
                pause()
            elif choice == "9":
                print("Exiting...")
                break
            else:
                print("Invalid option. Try again.")
                pause()

        except Exception as e:
            print(f"Error: {e}")
