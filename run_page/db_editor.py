#!/usr/bin/env python3
"""
Database editor for data.db - allows viewing and deleting activity records.
"""

import sys
from datetime import datetime

from config import SQL_FILE
from generator.db import Activity, init_db


def display_all_activities(session):
    """Display all activities in the database."""
    activities = session.query(Activity).all()

    if not activities:
        print("No activities found in database.")
        return

    print(f"\n{'='*120}")
    print(f"Total activities: {len(activities)}")
    print(f"{'='*120}\n")
    print(
        f"{'ID':<8} {'Name':<30} {'Date':<20} {'Type':<12} {'Distance':<10}"
        f" {'Source':<10}"
    )
    print("-" * 120)

    for activity in activities:
        activity_id = activity.run_id or ""
        name = activity.name[:29] if activity.name else "N/A"
        date = activity.start_date[:19] if activity.start_date else "N/A"
        activity_type = activity.type[:11] if activity.type else "N/A"
        distance = f"{activity.distance:.2f}km" if activity.distance else "N/A"
        source = activity.source[:9] if activity.source else "N/A"

        print(
            f"{activity_id:<8} {name:<30} {date:<20} {activity_type:<12}"
            f" {distance:<10} {source:<10}"
        )

    print(f"\n{'='*120}\n")


def display_activity_by_id(session, run_id):
    """Display a specific activity by ID."""
    activity = session.query(Activity).filter_by(run_id=run_id).first()

    if not activity:
        print(f"No activity found with ID {run_id}")
        return False

    print(f"\n{'='*80}")
    print(f"Activity Details (ID: {run_id})")
    print(f"{'='*80}")
    print(f"Name:                {activity.name}")
    print(f"Date (UTC):          {activity.start_date}")
    print(f"Date (Local):        {activity.start_date_local}")
    print(f"Type:                {activity.type}")
    dist_str = f"{activity.distance} km" if activity.distance else "N/A"
    print(f"Distance:            {dist_str}")
    print(f"Moving Time:         {activity.moving_time}")
    print(f"Elapsed Time:        {activity.elapsed_time}")
    avg_speed_str = f"{activity.average_speed} m/s" if activity.average_speed else "N/A"
    print(f"Average Speed:       {avg_speed_str}")
    avg_hr_str = (
        f"{activity.average_heartrate}" if activity.average_heartrate else "N/A"
    )
    print(f"Average Heart Rate:  {avg_hr_str}")
    elev_str = f"{activity.elevation_gain} m" if activity.elevation_gain else "N/A"
    print(f"Elevation Gain:      {elev_str}")
    print(f"Location Country:    {activity.location_country}")
    print(f"Source:              {activity.source}")
    print(f"{'='*80}\n")

    return True


def display_by_date_range(session, start_date, end_date):
    """Display activities within a date range (YYYY-MM-DD format)."""
    try:
        # Validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD")
        return

    activities = (
        session.query(Activity)
        .filter(
            Activity.start_date >= start_date,
            Activity.start_date <= end_date + " 23:59:59",
        )
        .all()
    )

    if not activities:
        print(f"No activities found between {start_date} and {end_date}")
        return

    print(f"\n{'='*120}")
    print(f"Activities from {start_date} to {end_date}" f" ({len(activities)} found)")
    print(f"{'='*120}\n")
    print(
        f"{'ID':<8} {'Name':<30} {'Date':<20} {'Type':<12} {'Distance':<10}"
        f" {'Source':<10}"
    )
    print("-" * 120)

    for activity in activities:
        activity_id = activity.run_id or ""
        name = activity.name[:29] if activity.name else "N/A"
        date = activity.start_date[:19] if activity.start_date else "N/A"
        activity_type = activity.type[:11] if activity.type else "N/A"
        distance = f"{activity.distance:.2f}km" if activity.distance else "N/A"
        source = activity.source[:9] if activity.source else "N/A"

        print(
            f"{activity_id:<8} {name:<30} {date:<20} {activity_type:<12}"
            f" {distance:<10} {source:<10}"
        )

    print(f"\n{'='*120}\n")


def delete_activity_by_id(session, run_id):
    """Delete a specific activity by ID."""
    activity = session.query(Activity).filter_by(run_id=run_id).first()

    if not activity:
        print(f"No activity found with ID {run_id}")
        return False

    print("\nActivity to delete:")
    print(f"  ID: {activity.run_id}")
    print(f"  Name: {activity.name}")
    print(f"  Date: {activity.start_date}")
    print(f"  Distance: {activity.distance} km")

    confirm = (
        input("\nAre you sure you want to delete this activity? (yes/no): ")
        .lower()
        .strip()
    )

    if confirm == "yes":
        session.delete(activity)
        session.commit()
        print("Activity deleted successfully!")
        return True
    else:
        print("Delete cancelled.")
        return False


def delete_activities_by_ids(session, ids):
    """Delete multiple activities by IDs."""
    activities_to_delete = []
    not_found = []

    for run_id in ids:
        activity = session.query(Activity).filter_by(run_id=run_id).first()
        if activity:
            activities_to_delete.append(activity)
        else:
            not_found.append(run_id)

    if not_found:
        print(f"\nWarning: Activity IDs not found: {', '.join(map(str, not_found))}")

    if not activities_to_delete:
        print("No activities found to delete.")
        return False

    print(f"\nFound {len(activities_to_delete)} activities to delete:")
    for activity in activities_to_delete:
        print(f"  - ID {activity.run_id}: {activity.name} ({activity.start_date})")

    confirm = (
        input("\nAre you sure you want to delete these activities? (yes/no): ")
        .lower()
        .strip()
    )

    if confirm == "yes":
        for activity in activities_to_delete:
            session.delete(activity)
        session.commit()
        print(f"{len(activities_to_delete)} activity(ies) deleted successfully!")
        return True
    else:
        print("Delete cancelled.")
        return False


def delete_by_date_range(session, start_date, end_date):
    """Delete all activities within a date range (YYYY-MM-DD format)."""
    try:
        # Validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD")
        return False

    activities = (
        session.query(Activity)
        .filter(
            Activity.start_date >= start_date,
            Activity.start_date <= end_date + " 23:59:59",
        )
        .all()
    )

    if not activities:
        print(f"No activities found between {start_date} and {end_date}")
        return False

    print(f"\nFound {len(activities)} activities to delete:")
    for activity in activities:
        print(f"  - {activity.run_id}: {activity.name} ({activity.start_date})")

    confirm = (
        input("\nAre you sure you want to delete all these activities? (yes/no): ")
        .lower()
        .strip()
    )

    if confirm == "yes":
        for activity in activities:
            session.delete(activity)
        session.commit()
        print(f"{len(activities)} activities deleted successfully!")
        return True
    else:
        print("Delete cancelled.")
        return False


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("DATABASE EDITOR - data.db")
    print("=" * 60)
    print("1. Display all activities")
    print("2. Display activity by ID")
    print("3. Display activities by date range")
    print("4. Delete activity by ID")
    print("5. Delete activities by date range")
    print("6. Exit")
    print("=" * 60)


def main():
    """Main function with interactive menu."""
    try:
        session = init_db(SQL_FILE)
        print("\nDatabase connected successfully!")

        while True:
            show_menu()
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                display_all_activities(session)

            elif choice == "2":
                try:
                    run_id = int(input("Enter activity ID: ").strip())
                    display_activity_by_id(session, run_id)
                except ValueError:
                    print("Invalid ID. Please enter a number.")

            elif choice == "3":
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                display_by_date_range(session, start_date, end_date)

            elif choice == "4":
                try:
                    ids_input = input(
                        "Enter activity ID(s) to delete (comma or space" " separated): "
                    ).strip()
                    if not ids_input:
                        print("No IDs entered.")
                    else:
                        # Parse IDs - support both comma and space separated
                        ids_str = ids_input.replace(",", " ")
                        ids = [
                            int(id_str.strip())
                            for id_str in ids_str.split()
                            if id_str.strip()
                        ]

                        if len(ids) == 1:
                            delete_activity_by_id(session, ids[0])
                        else:
                            delete_activities_by_ids(session, ids)
                except ValueError:
                    print(
                        "Invalid ID(s). Please enter number(s) separated by"
                        " commas or spaces."
                    )

            elif choice == "5":
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                delete_by_date_range(session, start_date, end_date)

            elif choice == "6":
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1-6.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
