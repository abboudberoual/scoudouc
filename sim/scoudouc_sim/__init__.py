"""Scoudouc flight simulator: 2D (x, z, tilt) rocket with a gimballed motor."""
from .thrust import ThrustCurve, load_csv, builtin_motor, BUILTIN_MOTORS
from .vehicle import Vehicle, VehicleParams, State, G
from .control import PID, PIDGains, HoverslamTrigger, suggest_gains
from .sim import MissionConfig, Summary, run_mission

__all__ = [
    "ThrustCurve", "load_csv", "builtin_motor", "BUILTIN_MOTORS",
    "Vehicle", "VehicleParams", "State", "G",
    "PID", "PIDGains", "HoverslamTrigger", "suggest_gains",
    "MissionConfig", "Summary", "run_mission",
]
