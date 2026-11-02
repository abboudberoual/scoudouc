// Scoudouc 0 thrust stand: motor holder (OpenSCAD).
// Motor hangs NOZZLE-DOWN. Thrust pushes the motor UP, so the top of the motor presses on the
// thick top plate, and the plate pushes up on the load cell platform. A lip at the bottom stops
// the motor sliding out under its own weight before ignition. Exhaust leaves through the open bottom.
//
// Change the numbers in this first block, then render (F6) and export STL.
// Print in PETG or ASA (PLA softens near hot motor casings). 4 perimeters, 40% infill, tube upright.

motor_d   = 29;     // motor casing diameter in mm: 24 or 29 (18 also allowed, e.g. for C6)
holder_len = 85;    // tube length in mm, 70 to 100 (F15 is about 98 mm long: use 100)
clearance = 0.4;    // extra gap around the motor so it slides in (raise if your printer is tight)
wall      = 3;      // tube wall thickness in mm
plate_t   = 8;      // top thrust plate thickness in mm
lip_t     = 2.5;    // bottom retaining lip height in mm
lip_inset = 3.5;    // how far the lip reaches in from the casing wall (nozzle must still fit through)
bolt_sq   = 40;     // M4 bolt holes sit on a square this wide (match your load cell platform)
bolt_d    = 4.4;    // M4 clearance hole
flange_w  = 56;     // square top flange width
lead_slot = 7;      // notch in the lip so igniter leads can leave sideways

assert(motor_d == 18 || motor_d == 24 || motor_d == 29, "motor_d must be 18, 24 or 29");
assert(holder_len >= 70 && holder_len <= 100, "holder_len must be between 70 and 100 mm");

bore  = motor_d + clearance;
outer = bore + 2 * wall;
$fn = 96;

module holder() {
  difference() {
    union() {
      // the tube
      translate([0, 0, lip_t]) cylinder(d = outer, h = holder_len);
      // the lip ring at the bottom
      cylinder(d = outer, h = lip_t + 0.01);
      // the square top flange with bolt holes, sitting on top of the tube
      translate([-flange_w / 2, -flange_w / 2, lip_t + holder_len])
        cube([flange_w, flange_w, plate_t]);
    }
    // motor bore (stops short of the thick top plate, so the motor top touches the plate)
    translate([0, 0, lip_t]) cylinder(d = bore, h = holder_len + 0.01);
    // opening through the lip: smaller than the casing, bigger than the nozzle
    translate([0, 0, -1]) cylinder(d = bore - 2 * lip_inset, h = lip_t + 2);
    // notch for igniter leads
    translate([0, 0, -1]) translate([bore / 2 - lip_inset - 1, -lead_slot / 2, 0])
      cube([outer, lead_slot, lip_t + 1]);
    // four M4 mounting holes through the flange
    for (x = [-1, 1], y = [-1, 1])
      translate([x * bolt_sq / 2, y * bolt_sq / 2, lip_t + holder_len - 1])
        cylinder(d = bolt_d, h = plate_t + 2, $fn = 24);
  }
}

holder();
