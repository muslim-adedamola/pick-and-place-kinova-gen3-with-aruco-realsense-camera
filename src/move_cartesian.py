#this code is adapted and modified from the kinova kortex api link below
#https://github.com/Kinovarobotics/Kinova-kortex2_Gen3_G3L/blob/master/api_python/examples/110-Waypoints/02-send_cartesian_waypoint_trajectory.py

import sys
import os
import threading
import numpy as np

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.messages import Base_pb2


TIMEOUT_DURATION = 20


def check_for_end_or_abort(e):
    def check(notification):
        print("EVENT:",
              Base_pb2.ActionEvent.Name(notification.action_event))
        if notification.action_event in (
            Base_pb2.ACTION_END,
            Base_pb2.ACTION_ABORT
        ):
            e.set()
    return check


def move_to_cartesian_pose(base: BaseClient, T_base_target):

    # extract position
    x = float(T_base_target[0, 3])
    y = float(T_base_target[1, 3])
    z = float(T_base_target[2, 3])

    # choose orientation and extract from T_base_target (tune later)
    # theta_x = 90.0
    # theta_y = 0.0
    # theta_z = 90.0
    feedback = base.GetMeasuredCartesianPose()

    theta_x = feedback.theta_x
    theta_y = feedback.theta_y
    theta_z = feedback.theta_z


    # build waypoint
    waypoint = Base_pb2.CartesianWaypoint()
    waypoint.pose.x = x
    waypoint.pose.y = y
    waypoint.pose.z = z
    waypoint.pose.theta_x = theta_x
    waypoint.pose.theta_y = theta_y
    waypoint.pose.theta_z = theta_z

    waypoint.reference_frame = Base_pb2.CARTESIAN_REFERENCE_FRAME_BASE
    waypoint.blending_radius = 0.0

    # --- waypoint list ---
    waypoints = Base_pb2.WaypointList()
    waypoints.duration = 0.0
    waypoints.use_optimal_blending = False

    wp = waypoints.waypoints.add()
    wp.name = "target_pose"
    wp.cartesian_waypoint.CopyFrom(waypoint)

    # validate waypoint (IMPORTANT)
    result = base.ValidateWaypointList(waypoints)
    if len(result.trajectory_error_report.trajectory_error_elements) != 0:
        print("[ERROR] Waypoint validation failed")
        print(result.trajectory_error_report)

        return False

    # execute
    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    print("[INFO] Executing Cartesian waypoint")
    base.ExecuteWaypointTrajectory(waypoints)

    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if not finished:
        print("[ERROR] Motion timed out")
        return False

    print("[INFO] Cartesian motion completed")
    return True

