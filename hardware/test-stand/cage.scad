// Scoudouc 0 thrust stand: anti-tip CAGE (OpenSCAD), for the nozzle-UP cup.
// A ring with a few mm of free gap around the top of the cup, held by three posts that screw to the PLYWOOD
// BASE (not to the cup, not to the load cell). It only stops the cup tipping over if thrust is a few degrees
// off-axis. The gap means the ring never touches the cup in normal use, so it can never carry vertical load
// (if it did, it would take force away from the cell and the reading would be too low).
//
// Modelled in USE orientation (z = 0 is the plywood). Set print_flip = true (default) to export ring-down,
// which prints with no supports. PLA, 4 perimeters, 30% infill, 0.2 mm layers. Printer: LIBRARY (MK3), est. 4 h
// for the 29 mm cage (under the 6 h limit); the footprint is about 128 x 111 mm.
// HEAT: the ring is outside the cup wall, with a gap and the cardboard liner between it and the casing.
// Keep the ring below the cup rim (ring_drop) and replace it if it softens.

motor_d    = 29;    // must match the cup
holder_len = 85;    // must match the cup
clearance  = 0.4;   // same as cup.scad
liner_t    = 1.0;   // same as cup.scad
wall       = 3;     // same as cup.scad
plate_t    = 8;     // same as cup.scad
stand_h    = 25;    // MEASURE THIS: height of the cup's underside above the plywood (cell + riser + platform)
cage_gap   = 3;     // free gap between cup wall and ring, each side (mm). 2 to 4 is fine
ring_h     = 10;    // ring height
ring_w     = 5;     // ring radial thickness
ring_drop  = 5;     // ring top sits this far below the cup rim
post_R     = 52;    // post centre distance from the cup axis (clears the 56 mm flange corner at 39.6 mm)
post_r     = 10;    // post size, radial
post_t     = 16;    // post size, sideways
arm_w      = 10;    // arm joining ring to post
foot_ext   = 12;    // foot tab sticks out this far beyond the post
tab_t      = 5;     // foot tab thickness
screw_d    = 4.5;   // wood-screw hole
post_angle0 = 90;   // rotate the whole cage so no post sits on the load cell bar or its riser
print_flip = true;

bore  = motor_d + 2 * liner_t + clearance;
outer = bore + 2 * wall;
cup_top = stand_h + plate_t + holder_len;
ring_top = cup_top - ring_drop;
ring_z = ring_top - ring_h;
ring_id = outer + 2 * cage_gap;
ring_od = ring_id + 2 * ring_w;
$fn = 96;

module post() {
  px0 = post_R - post_r / 2;
  px1 = post_R + post_r / 2;
  difference() {
    union() {
      translate([px0, -post_t / 2, 0]) cube([post_r, post_t, ring_top]);                     // post
      translate([ring_od / 2 - 1, -arm_w / 2, ring_z]) cube([px0 - ring_od / 2 + 2, arm_w, ring_h]); // arm
      translate([px0, -post_t / 2, 0]) cube([post_r + foot_ext, post_t, tab_t]);             // foot tab
      for (s = [-1, 1])                                                                      // 45 degree ribs
        hull() {
          translate([px0, s * (post_t / 2 - 1.5) - 1.5, 0]) cube([post_r + foot_ext, 3, tab_t]);
          translate([px0, s * (post_t / 2 - 1.5) - 1.5, tab_t + foot_ext - 0.01]) cube([post_r, 3, 0.01]);
        }
    }
    translate([px1 + foot_ext / 2, 0, -1]) cylinder(d = screw_d, h = tab_t + foot_ext + 2, $fn = 24);
  }
}

module cage() {
  difference() {
    translate([0, 0, ring_z]) cylinder(d = ring_od, h = ring_h);
    translate([0, 0, ring_z - 1]) cylinder(d = ring_id, h = ring_h + 2);
  }
  for (k = [0 : 2]) rotate([0, 0, post_angle0 + 120 * k]) post();
}

if (print_flip) translate([0, 0, ring_top]) rotate([180, 0, 0]) cage();
else cage();
