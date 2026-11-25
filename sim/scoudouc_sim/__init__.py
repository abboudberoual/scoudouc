"""Scoudouc flight simulator: 2D (x, z, tilt) rocket with a gimballed motor."""
from .thrust import ThrustCurve, load_csv, load_eng, builtin_motor, BUILTIN_MOTORS
from .vehicle import Vehicle, VehicleParams, State, G
from .control import PID, PIDGains, HoverslamTrigger, IntegratingTrigger, suggest_gains
from .sim import MissionConfig, Summary, run_mission

__all__ = [
    "ThrustCurve", "load_csv", "load_eng", "builtin_motor", "BUILTIN_MOTORS",
    "Vehicle", "VehicleParams", "State", "G",
    "PID", "PIDGains", "HoverslamTrigger", "IntegratingTrigger", "suggest_gains",
    "MissionConfig", "Summary", "run_mission",
]
