import math
import pytest

from scoudouc_sim import (ThrustCurve, builtin_motor, load_csv, VehicleParams, Vehicle, State,
                          MissionConfig, run_mission, PIDGains, HoverslamTrigger, G)

PUBLISHED = {"C6": 8.8, "D12": 16.8, "E12": 28.5, "F15": 49.6}


@pytest.mark.parametrize("name,impulse", PUBLISHED.items())
def test_builtin_impulse_matches_published(name, impulse):
    m = builtin_motor(name)
    assert m.total_impulse == pytest.approx(impulse, rel=0.01)
    assert m.average_thrust * m.burn_time == pytest.approx(impulse, rel=0.01)


def test_scaling_scales_impulse_not_burn_time():
    m = builtin_motor("D12")
    s = m.scaled(1.15)
    assert s.total_impulse == pytest.approx(1.15 * m.total_impulse, rel=1e-9)
    assert s.burn_time == m.burn_time
    assert s.propellant_kg == m.propellant_kg


def test_csv_roundtrip(tmp_path):
    p = tmp_path / "c.csv"
    p.write_text("time_s,thrust_n\n0,0\n0.1,10\n1.0,10\n1.1,0\n")
    m = load_csv(str(p))
    assert m.total_impulse == pytest.approx(0.5 + 9.0 + 0.5, rel=1e-9)
    assert m.thrust(0.5) == pytest.approx(10.0)
    assert m.thrust(2.0) == 0.0


def test_propellant_burns_off_fully():
    m = builtin_motor("E12")
    assert m.mass_burned(0) == 0
    assert m.mass_burned(m.burn_time + 1) == pytest.approx(m.propellant_kg)
    assert 0 < m.mass_burned(1.0) < m.propellant_kg


def test_gimbal_limit_never_exceeded():
    v = Vehicle(VehicleParams(launch_mass_kg=0.35, length_m=0.4))
    d = 0.0
    for _ in range(2000):                       # 2 s of a wildly large command
        d = v.servo_step(d, math.radians(40), 0.001)
        assert abs(d) <= math.radians(6.0) + 1e-12
    assert d == pytest.approx(math.radians(6.0), abs=1e-4)
    d = v.servo_step(d, math.radians(-40), 0.001)
    assert d >= -math.radians(6.0)


def test_servo_is_a_lag_with_rate_limit():
    v = Vehicle(VehicleParams(launch_mass_kg=0.35, length_m=0.4, servo_rate_dps=1e6))
    d = 0.0
    cmd = math.radians(3.0)
    for _ in range(45):                          # one time constant
        d = v.servo_step(d, cmd, 0.001)
    assert d / cmd == pytest.approx(1 - math.exp(-1), abs=0.03)
    slow = Vehicle(VehicleParams(launch_mass_kg=0.35, length_m=0.4, servo_rate_dps=100))
    d = slow.servo_step(0.0, math.radians(6), 0.01)
    assert d <= math.radians(100) * 0.01 + 1e-12


def test_stays_on_pad_when_thrust_below_weight():
    v = Vehicle(VehicleParams(launch_mass_kg=1.0, length_m=0.5))
    s = State()
    for _ in range(100):
        v.step(s, 5.0, 0.0, 1.0, 0.001, airborne=False)
    assert s.z == 0.0 and s.vz == 0.0


def _strong_motor():
    return ThrustCurve([0, 0.05, 4.0, 4.05], [0, 15, 15, 0], name="test15", propellant_kg=0.02)


def test_hoverslam_fires_before_ground_contact():
    veh = VehicleParams(launch_mass_kg=0.6, length_m=0.5, cg_to_nozzle_m=0.2)
    up = ThrustCurve([0, 0.05, 0.5, 0.55], [0, 25, 25, 0], propellant_kg=0.02)
    down = _strong_motor()
    trig = HoverslamTrigger(thrust_est_n=15.0, margin=1.1, ignition_delay_s=0.05)
    cfg = MissionConfig(vehicle=veh, motor_a=up, motor_b=down, gains=PIDGains(1.0, 0, 0.1),
                        trigger=trig)
    summary, log = run_mission(cfg)
    assert summary.landing_burn_fired
    assert summary.touched_down
    assert summary.t_landing_ignite_s < summary.flight_time_s      # lit before touchdown
    # height when the trigger fired must be positive and the stopping distance covers it
    i = min(range(len(log["t_s"])), key=lambda k: abs(log["t_s"][k] - summary.t_landing_ignite_s))
    assert log["z_m"][i] > 0.5
    # and the burn actually helps: slower than the same flight with no landing motor
    cfg0 = MissionConfig(vehicle=veh, motor_a=up, gains=PIDGains(1.0, 0, 0.1))
    s0, _ = run_mission(cfg0)
    assert summary.touchdown_speed_mps < 0.5 * s0.touchdown_speed_mps


def test_trigger_formula():
    trig = HoverslamTrigger(thrust_est_n=20.0, margin=1.0, ignition_delay_s=0.0)
    m, v = 1.0, 10.0
    expected = v ** 2 / (2 * (20.0 / m - G))
    assert trig.stopping_distance(v, m) == pytest.approx(expected)
    assert trig.should_fire(expected * 0.99, -v, m)
    assert not trig.should_fire(expected * 1.01, -v, m)
    assert not trig.should_fire(0.0, +5.0, m)                       # rising: never
    weak = HoverslamTrigger(thrust_est_n=5.0)
    assert weak.stopping_distance(5.0, 1.0) == math.inf              # cannot ever stop


def test_pid_removes_initial_tilt_under_thrust():
    veh = VehicleParams(launch_mass_kg=0.35, length_m=0.4)
    motor = builtin_motor("D12")
    from scoudouc_sim import suggest_gains
    g = suggest_gains(Vehicle(veh).inertia(0.34), veh.cg_to_nozzle_m, motor.average_thrust, 12.0)
    s, log = run_mission(MissionConfig(vehicle=veh, motor_a=motor, gains=g, initial_tilt_deg=5.0,
                                       chute_cda_m2=0.25))
    powered = [tl for tl, th in zip(log["tilt_deg"], log["thrust_n"]) if th > 0]
    assert abs(powered[-1]) < 1.0           # tilt mostly gone by burnout
    assert s.max_tilt_powered_deg <= 5.0 + 1e-6


# --- T-010: .eng loader and integrating landing trigger ---------------------------
from scoudouc_sim import load_eng, IntegratingTrigger  # noqa: E402

ENG = """; sample RASP file
E12 24 70 0-4-6-8 0.0358 0.0573 Estes
0.05 16.0
0.12 32.0
0.30 18.0
0.60 11.0
2.10 9.5
2.30 0.0
"""


def test_load_eng(tmp_path):
    p = tmp_path / "Estes_E12.eng"
    p.write_text(ENG)
    m = load_eng(str(p))
    assert m.name == "E12"
    assert m.propellant_kg == pytest.approx(0.0358)
    assert m.peak_thrust == pytest.approx(32.0)
    assert m.burn_time == pytest.approx(2.30)
    assert m.thrust(0.12) == pytest.approx(32.0)


def _s2(mass_kg, trigger_kind, scale_b=1.0):
    e12 = builtin_motor("E12")
    veh = VehicleParams(launch_mass_kg=mass_kg, length_m=0.6, radius_m=0.033, cg_to_nozzle_m=0.22)
    cda = veh.drag_cd * math.pi * veh.radius_m ** 2
    trig = (IntegratingTrigger(e12, ignition_delay_s=0.1, drag_cda_m2=cda)
            if trigger_kind == "integrating"
            else HoverslamTrigger.from_motor(e12, thrust_trust=0.9, ignition_delay_s=0.1))
    cfg = MissionConfig(vehicle=veh, motor_a=e12, motor_b=e12.scaled(scale_b),
                        gains=PIDGains(kp=1.4, kd=0.16), trigger=trig)
    return run_mission(cfg)[0]


def test_integrating_trigger_never_fires_while_climbing():
    trig = IntegratingTrigger(builtin_motor("E12"))
    assert not trig.should_fire(10.0, 5.0, 0.62)
    assert not trig.should_fire(10.0, 0.0, 0.62)


def test_integrating_trigger_fires_when_waiting_makes_it_worse():
    trig = IntegratingTrigger(builtin_motor("E12"))
    # vz is up-positive. Falling slowly from high up: firing now would stop the rocket high, so wait.
    assert not trig.should_fire(40.0, -2.0, 0.62)
    # Falling fast close to the ground: already late, fire.
    assert trig.should_fire(2.0, -20.0, 0.62)
    # Predicted touchdown grows as the ignition height drops below the best point.
    assert trig.predicted_touchdown(1.0, 20.0, 0.62) > trig.predicted_touchdown(15.0, 20.0, 0.62)


@pytest.mark.parametrize("mass_kg", [0.660, 0.750])
def test_integrating_trigger_lands_nominal_motor(mass_kg):
    s = _s2(mass_kg, "integrating")
    assert s.landing_burn_fired and s.touched_down
    assert s.touchdown_speed_mps < 2.0


def test_integrating_trigger_beats_stopping_distance_rule():
    assert _s2(0.660, "integrating").touchdown_speed_mps < _s2(0.660, "stopping").touchdown_speed_mps


def test_hot_motor_lands_harder_than_nominal():
    """The trigger trusts the nominal curve; a 10 % hot motor stops the rocket high."""
    assert _s2(0.660, "integrating", 1.10).touchdown_speed_mps > 2.0


def test_integrating_trigger_fires_with_a_motor_that_cannot_stop_the_fall():
    """C6 at 660 g has thrust below weight: it must still fire (and touch down fast)."""
    c6, e12 = builtin_motor("C6"), builtin_motor("E12")
    veh = VehicleParams(launch_mass_kg=0.660, length_m=0.6, radius_m=0.033, cg_to_nozzle_m=0.22)
    cfg = MissionConfig(vehicle=veh, motor_a=e12, motor_b=c6, gains=PIDGains(kp=1.4, kd=0.16),
                        trigger=IntegratingTrigger(c6, ignition_delay_s=0.1))
    s = run_mission(cfg)[0]
    assert s.landing_burn_fired and s.touched_down
    assert s.t_landing_ignite_s < s.flight_time_s
