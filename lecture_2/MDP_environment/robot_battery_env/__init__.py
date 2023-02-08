from robot_battery_env.robot_battery import RobotBattery
from gym.envs.registration import register

register(
    id="RobotBattery-v",
    entry_point="robot_battery_env.robot_battery:RobotBattery"
)

(RobotBattery,)
