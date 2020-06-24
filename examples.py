import os
import json
import cv2

# Videos were recorded at 30 FPS, but the frame rate might differ because of the Android OS
def getVideoTimestamps(video_path):
    cap = cv2.VideoCapture(video_path)

    # Get first timestamp, convert to nanoseconds
    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC) * 1_000_000]

    # Iterate though all frames
    while (cap.isOpened()):
        valid, _ = cap.read()
        if valid:
            # Log and convert to nanoseconds
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) * 1_000_000)
        else:
            break

    cap.release()
    return timestamps

# Checks if an orientation change should be logged
def isValidOrientationChange(device_data, index):
    # Minimum duration required to be counted as a valid orientation change. It might be that in some cases an orientation
    # change is logged for only a single frame. In that case we want to ignore it since it's possibly a false report
    ORIENTATION_CHANGE_MIN_DURATION_MS = 800
    tmp_index = index + 1

    # Orientation needs to change for at least ORIENTATION_CHANGE_MIN_DURATION ms to be valid
    while tmp_index < len(device_data):
        # Check if threshold was exceeded
        if device_data[tmp_index]['time'] - device_data[index]["time"] >= ORIENTATION_CHANGE_MIN_DURATION_MS * 1_000_000:
            return True

        # Check if we have another orientation change
        if device_data[tmp_index]['event'] == 'ACTION_SCREEN_ORIENTATION_CHANGE':
            return False

        tmp_index += 1

    # End of video recording reached before threshold was exceeded
    return False

# Reports the device orientation for each frame
def analyseOrientation(account_path, recording, session):
    recording_path = os.path.join(account_path, "Recording " + str(recording).zfill(3))
    session_path = os.path.join(recording_path, "Session " + str(session).zfill(4))
    video_path = os.path.join(session_path, "video.mp4")

    assert(os.path.exists(video_path))

    # Contains all device events, like orientation changes
    with open(os.path.join(recording_path, "device_data.txt")) as device_file:
        device_data = json.load(device_file)["device_data"]

        # Contains video recording specific data
        with open(os.path.join(recording_path, "video_data.txt")) as video_file:
            video_data = json.load(video_file)["video_data"]

            assert(session < len(video_data))

            # Get start and end time of recording
            session_data = video_data[session]
            start_time = session_data["startTime"]
            end_time = session_data["stopTime"]

            # Get all timestamps of video
            timestamps = getVideoTimestamps(video_path)

            # Timestamp of video might not be perfectly synchronized with other timestamps!
            video_length = end_time - start_time
            print("Duration of video recording and logs mismatches by", str(round(abs(timestamps[-1] - video_length) / 1_000_000, 1)) + "ms")

            # Init values
            dev_index = 0
            orientation = "UNKNOWN"

            # Iterate though all timestamps of video
            for t in timestamps:
                time = start_time + t

                # Iterate until the most recent event that happened before 'time'
                while dev_index < len(device_data) - 1:
                    if device_data[dev_index+1]["time"] <= time:
                        dev_index += 1

                        # Check if log entry is a orientation change
                        if device_data[dev_index]["event"] == "ACTION_SCREEN_ORIENTATION_CHANGE" and isValidOrientationChange(device_data, dev_index):
                            # Possible values are 'PORTRAIT', 'REVERSE LANDSCAPE', 'REVERSE PORTRAIT', and 'LANDSCAPE'
                            orientation = device_data[dev_index]["val"]
                    else:
                        break

                # Print data for the current frame
                print('Time:', str(round(t / 1_000_000_000, 2)) + "s", ', Orientation:', orientation)

# Reports foreground application for each frame
def analyseApplication(account_path, recording, session):
    recording_path = os.path.join(account_path, "Recording " + str(recording).zfill(3))
    session_path = os.path.join(recording_path, "Session " + str(session).zfill(4))
    video_path = os.path.join(session_path, "video.mp4")

    assert(os.path.exists(video_path))

    # Contains all application changes
    with open(os.path.join(recording_path, "application_data.txt")) as application_file:
        application_data = json.load(application_file)["application_data"]

        # Contains video recording specific data
        with open(os.path.join(recording_path, "video_data.txt")) as video_file:
            video_data = json.load(video_file)["video_data"]

            assert(session < len(video_data))

            # Get start and end time of recording
            session_data = video_data[session]
            start_time = session_data["startTime"]
            end_time = session_data["stopTime"]

            # Get all timestamps of video
            timestamps = getVideoTimestamps(video_path)

            # Timestamp of video might not be perfectly synchronized with other timestamps!
            video_length = end_time - start_time
            print("Duration of video recording and logs mismatches by", str(round(abs(timestamps[-1] - video_length) / 1_000_000, 1)) + "ms")

            # Init default values
            dummy = {"name": "UNKNOWN", "time": 0}
            application_data.insert(0, dummy)
            app_index = 0

            # Iterate though all timestamps of video
            for t in timestamps:
                time = start_time + t

                # Iterate until the most recent event that happened before 'time'
                while app_index < len(application_data) - 1:
                    if application_data[app_index+1]["time"] <= time:
                        app_index += 1
                    else:
                        break

                # Print data for the current frame
                print('Time:', str(round(t / 1_000_000_000, 2)) + "s", ', App:', application_data[app_index]["name"])


# Reports all logged activities for each frame with high confidence value
def analyseActivity(account_path, recording, session):
    # Minimum required confidence value for a logged activity (ranges from 0 to 100)
    ACTIVITY_CONFIDENCE_THRESHOLD = 50  # in %

    recording_path = os.path.join(account_path, "Recording " + str(recording).zfill(3))
    session_path = os.path.join(recording_path, "Session " + str(session).zfill(4))
    video_path = os.path.join(session_path, "video.mp4")

    assert(os.path.exists(video_path))

    # Contains video recording specific data
    with open(os.path.join(recording_path, "video_data.txt")) as video_file:
        video_data = json.load(video_file)["video_data"]

        assert(session < len(video_data))
        session_data = video_data[session]

        # Contains all logged activities
        with open(os.path.join(session_path, "activity_data.txt")) as activity_file:
            activity_data = json.load(activity_file)["activity_data"]

            # Get start and end time of recording
            start_time = session_data["startTime"]
            end_time = session_data["stopTime"]

            # Get all timestamps of video
            timestamps = getVideoTimestamps(video_path)

            # Timestamp of video might not be perfectly synchronized with other timestamps!
            video_length = end_time - start_time
            print("Duration of video recording and logs mismatches by", str(round(abs(timestamps[-1] - video_length) / 1_000_000, 1)) + "ms")

            # Init values
            activity_index = 0

            # Iterate though all timestamps of video
            for t in timestamps:
                time = start_time + t

                # Iterate until the most recent event that happened before 'time'
                while activity_index < len(activity_data) - 1:
                    if activity_data[activity_index+1]["time"] <= time:
                        activity_index += 1
                    else:
                        break

                # Stores all activities with a high confidence value in this dict.
                # Notice that multiple activities can have high confidence values!
                temp = []

                # Iterate through all reported activities
                for element in activity_data[activity_index]['activities']:
                    if element['conf'] >= ACTIVITY_CONFIDENCE_THRESHOLD:
                        temp.append(element['name'])

                # Print data for the current frame
                print('Time:', str(round(t / 1_000_000_000, 2)) + "s", ', Activities:', temp)

if __name__ == '__main__':
    account = "/media/sander/HDD/ALL_DATA/fd249093-60d2-4d4f-99d0-3e98954f7711"
    recording = 2
    session= 0

    analyseApplication(account, recording, session)
    #analyseActivity(account, recording, session)
    #analyseOrientation(account, recording, session)