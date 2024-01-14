import math

# Constants
WHEEL_DIAMETER = 0.1524  # [m]
LX = 0.2105              # [m]
LY = 0.31                # [m]
wheel_circumference = WHEEL_DIAMETER * math.pi
angular_to_rpm = 60 / wheel_circumference

def calculate_wheel_rpms(vx, vy, wz):
    wheel_rpms = {}

    wheel_rpms['rpm_FL'] = (vx + vy + (LX + LY) * wz) * angular_to_rpm
    wheel_rpms['rpm_FR'] = (vx - vy - (LX + LY) * wz) * angular_to_rpm
    wheel_rpms['rpm_BL'] = (vx - vy + (LX + LY) * wz) * angular_to_rpm
    wheel_rpms['rpm_BR'] = (vx + vy - (LX + LY) * wz) * angular_to_rpm

    return wheel_rpms

def forward_kinematic(rpm_FL, rpm_FR, rpm_BL, rpm_BR):
    rpm_to_rad_per_sec = 2 * math.pi / 60

    omega_FL = rpm_FL * rpm_to_rad_per_sec
    omega_FR = rpm_FR * rpm_to_rad_per_sec
    omega_BL = rpm_BL * rpm_to_rad_per_sec
    omega_BR = rpm_BR * rpm_to_rad_per_sec

    vx = (WHEEL_DIAMETER / 2) / 4 * (omega_FL + omega_FR + omega_BL + omega_BR)
    vy = (WHEEL_DIAMETER / 2) / 4 * -(-omega_FL + omega_FR + omega_BL - omega_BR)
    wz = (
        (WHEEL_DIAMETER / 2)
        / (4 * (LX + LY))
        * (omega_FL - omega_FR + omega_BL - omega_BR)
    )

    return vx, vy, wz

# Example usage:
vx = 1.0  # Replace with your desired values
vy = 0
wz = 0

wheel_rpms_result = calculate_wheel_rpms(vx, vy, wz)
print(wheel_rpms_result)

print(forward_kinematic(wheel_rpms_result['rpm_FL'], wheel_rpms_result['rpm_FR'],wheel_rpms_result['rpm_BL'],wheel_rpms_result['rpm_BR']))