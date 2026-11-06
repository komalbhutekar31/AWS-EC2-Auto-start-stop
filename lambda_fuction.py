import boto3
import os
from datetime import datetime
from zoneinfo import ZoneInfo


# --------------------------------------------------
# CREATE EC2 CLIENT
# --------------------------------------------------

ec2 = boto3.client("ec2")


# --------------------------------------------------
# DEVELOPER INSTANCE IDs FROM ENVIRONMENT VARIABLES
# --------------------------------------------------

DEVELOPERS = {

    "dev-1": {
        "instance_id": os.environ["DEV1_INSTANCE_ID"],
        "working_times": [
            (6 * 60, 10 * 60),       # 6:00 AM - 10:00 AM
            (21 * 60, 25 * 60)       # 9:00 PM - 1:00 AM
        ]
    },

    "dev-2": {
        "instance_id": os.environ["DEV2_INSTANCE_ID"],
        "working_times": [
            (17 * 60, 24 * 60)       # 5:00 PM - 12:00 AM
        ]
    },

    "dev-3": {
        "instance_id": os.environ["DEV3_INSTANCE_ID"],
        "working_times": [
            (14 * 60, 18 * 60)       # 2:00 PM - 6:00 PM
        ]
    },

    "dev-4": {
        "instance_id": os.environ["DEV4_INSTANCE_ID"],
        "working_times": [
            (4 * 60, 8 * 60),        # 4:00 AM - 8:00 AM
            (19 * 60, 21 * 60)       # 7:00 PM - 9:00 PM
        ]
    }
}


# --------------------------------------------------
# CHECK WHETHER CURRENT TIME IS WORKING TIME
# --------------------------------------------------

def is_working_time(current_minutes, working_times):

    for start_time, stop_time in working_times:

        if stop_time <= 24 * 60:

            if start_time <= current_minutes < stop_time:
                return True

        else:

            if current_minutes >= start_time:
                return True

            if current_minutes < (stop_time - 24 * 60):
                return True

    return False


# --------------------------------------------------
# LAMBDA HANDLER
# --------------------------------------------------

def lambda_handler(event, context):

    # Current IST time
    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    current_minutes = now.hour * 60 + now.minute

    print("----------------------------------------")
    print(
        "Current IST Time:",
        now.strftime("%Y-%m-%d %I:%M:%S %p")
    )
    print(
        "Current Minutes:",
        current_minutes
    )
    print("----------------------------------------")


    results = {}


    # --------------------------------------------------
    # CHECK EACH DEVELOPER
    # --------------------------------------------------

    for developer, config in DEVELOPERS.items():

        instance_id = config["instance_id"]
        working_times = config["working_times"]

        print("")
        print("========================================")
        print("Developer:", developer)
        print("========================================")


        # --------------------------------------------------
        # GET CURRENT EC2 STATE
        # --------------------------------------------------

        try:

            response = ec2.describe_instances(
                InstanceIds=[instance_id]
            )

            state = response[
                "Reservations"
            ][0][
                "Instances"
            ][0][
                "State"
            ]["Name"]

            print(
                "Current EC2 State:",
                state
            )


        except Exception as e:

            print(
                "ERROR getting EC2 state:",
                str(e)
            )

            results[developer] = {
                "action": "ERROR",
                "error": str(e)
            }

            continue


        # --------------------------------------------------
        # CHECK WORKING TIME
        # --------------------------------------------------

        working = is_working_time(
            current_minutes,
            working_times
        )


        # --------------------------------------------------
        # WORKING TIME
        # EC2 SHOULD BE RUNNING
        # --------------------------------------------------

        if working:

            print(
                "Working time - EC2 should be RUNNING"
            )


            if state == "stopped":

                print(
                    "EC2 is stopped. Starting EC2..."
                )

                try:

                    ec2.start_instances(
                        InstanceIds=[instance_id]
                    )

                    action = "START command sent"

                    print(action)

                except Exception as e:

                    action = "START ERROR"

                    print(
                        "Start error:",
                        str(e)
                    )


            elif state == "running":

                print(
                    "EC2 is already running"
                )

                action = "No action"


            else:

                print(
                    f"EC2 is currently in '{state}' state"
                )

                action = "No action"


        # --------------------------------------------------
        # NON-WORKING TIME
        # EC2 SHOULD BE STOPPED
        # --------------------------------------------------

        else:

            print(
                "Non-working time - EC2 should be STOPPED"
            )


            if state == "running":

                print(
                    "EC2 is running. Stopping EC2..."
                )

                try:

                    ec2.stop_instances(
                        InstanceIds=[instance_id]
                    )

                    action = "STOP command sent"

                    print(action)

                except Exception as e:

                    action = "STOP ERROR"

                    print(
                        "Stop error:",
                        str(e)
                    )


            elif state == "stopped":

                print(
                    "EC2 is already stopped"
                )

                action = "No action"


            else:

                print(
                    f"EC2 is currently in '{state}' state"
                )

                action = "No action"


        # --------------------------------------------------
        # SAVE RESULT
        # --------------------------------------------------

        results[developer] = {
            "state_before_action": state,
            "working_time": working,
            "action": action
        }


    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    print("")
    print("========================================")
    print("FINAL RESULT")
    print("========================================")

    print(results)


    return {
        "statusCode": 200,
        "time_ist": now.strftime(
            "%Y-%m-%d %I:%M:%S %p"
        ),
        "developers": results
    }