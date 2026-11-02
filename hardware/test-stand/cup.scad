// Scoudouc 0 thrust stand: motor CUP (OpenSCAD), nozzle-UP layout. Replaces holder.scad.
// The motor stands upright, nozzle up. Its base sits on the thick floor of this cup; the floor sits on the
// load cell (bolted to the cell's platform through the square flange, or just resting flat on a button cell).
// Thrust pushes DOWN, through the floor, into the cell. The walls only keep the motor upright and carry NO load.
//
// Print: PLA, flange down (as modelled), no supports, 4 perimeters, 40% infill, 0.2 mm layers.
// Printer: LIBRARY (Prusa MK3). Estimated 2.5 to 3.2 h on an MK3 (see README for each size). Prints upright; the open top is the last layer.
// HEAT: PLA softens near a hot casing. Line the bore with a cardboard tube (liner_t thick, e.g. rolled kraft
// paper or a spare casing wrap). The cup is a CONSUMABLE: inspect after every burn, bin it if it is soft or warped.

motor_d    = 29;    // motor casing diameter in mm: 24 or 29 (18 also allowed, e.g. for C6)
holder_len = 85;    // depth of the bore above the floor in mm, 70 to 100 (motor sticks out of the top if longer)
clearance  = 0.4;   // extra gap so the lined motor slides in (raise if your printer is tight)
liner_t    = 1.0;   // thickness of the cardboard liner in mm (bore grows by 2 x this)
wall       = 3;     // cup wall thickness in mm
plate_t    = 8;     // thick floor AND flange thickness in mm: the motor's base pushes on the cell through this
bolt_sq    = 40;    // M4 bolt holes sit on a square this wide (match your load cell platform)
bolt_d     = 4.4;   // M4 clearance hole
flange_w   = 56;    // square bottom flange width
lead_slot  = 7;     // width of the side notch at the base for igniter leads (and the opposite vent notch)
lead_h     = 4;     // height of those notches above the floor
groove_w   = 4;     // vertical groove behind the liner that the leads run down
groove_d   = 1.2;   // how deep that groove cuts into the wall
bolt_holes = true;  // false = plain flat bottom for a button cell (no holes)
vent_notch = true;  // opposite-side notch so gas can leave sideways at the base

assert(motor_d == 18 || motor_d == 24 || motor_d == 29, "motor_d must be 18, 24 or 29");
assert(holder_len >= 70 && holder_len <= 100, "holder_len must be between 70 and 100 mm");

bore  = motor_d + 2 * liner_t + clearance;
outer = bore + 2 * wall;
top   = plate_t + holder_len;
$fn = 96;

module cup() {
  difference() {
    union() {
      cylinder(d = outer, h = top);                                   // the cup wall
      translate([-flange_w / 2, -flange_w / 2, 0])
        cube([flange_w, flange_w, plate_t]);                          // flange at the BOTTOM
    }
    translate([0, 0, plate_t]) cylinder(d = bore, h = holder_len + 1);  // bore, open top, floor left solid
    // groove behind the liner for the leads (+X side), top to floor
    translate([bore / 2 - groove_d, -groove_w / 2, plate_t]) cube([groove_d + 1, groove_w, holder_len + 1]);
    // side notch through the wall at the base: igniter leads leave here (+X)
    translate([bore / 2 - groove_d, -lead_slot / 2, plate_t]) cube([outer, lead_slot, lead_h]);
    // opposite-side vent notch (-X)
    if (vent_notch)
      translate([-(bore / 2 - groove_d) - outer, -lead_slot / 2, plate_t]) cube([outer, lead_slot, lead_h]);
    // four M4 mounting holes through the flange
    if (bolt_holes)
      for (x = [-1, 1], y = [-1, 1])
        translate([x * bolt_sq / 2, y * bolt_sq / 2, -1]) cylinder(d = bolt_d, h = plate_t + 2, $fn = 24);
  }
}

cup();
