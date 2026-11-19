# Stand v3 in extrusion: what it is and why (plain language)

**Move to `docs/learning/` (it replaces the plywood parts of `thrust-stand-v3.md`).**

**The idea.** The motor stands nozzle-up on a load cell. The rocket pushes down, the cell feels the push, and the number goes to the ESP32. Everything else only keeps the motor upright and the stand in place.

**The frame.** Four aluminium bars (2020 means 20 mm square with T-shaped grooves, the "T-slots") stand up like a tower, with a small square frame at the bottom and the top. A nut slides into a groove and a screw into the nut, so anything bolts on anywhere: cameras, a rain cover, the ring. Corners are held with small L-brackets. The tower is 160 mm square and 523 mm tall, tall enough that a 360 mm motor stands fully inside.

**Where the push goes.** Motor, collar, cell, a 3.2 mm aluminium plate, the two bottom bars the plate rests on, then the ground. The brackets and screws never feel the thrust. They hold the frame together and take the pull of the guy ropes.

**Why steel brackets, not printed.** Printed ones are CAD 13 cheaper but plastic slowly stretches under steady pull and softens near heat, and 24 of them is 24 print jobs at the library. The guy ropes pull on the bottom corners, and the top frame sits just above the flame. We picked steel.

**Why an aluminium plate, not plywood.** We checked the worst case, a dip in the ground so only two bars touch the plate. 6 mm plywood would break (safety factor 0.55, you want over 1.5). 3.2 mm aluminium gets 1.9. Aluminium also does not scorch.

**The ring.** A printed ring on two bars catches the motor if it tips. It sits at the motor's mid-height; loosen eight screws and slide the ladder to move it for a short motor. It never carries thrust.

**The cost.** The extrusion tower is CAD 278.55 against 192.35 for plywood (+86). You chose it for durability and presentation; the CAD 120 line cannot be met with it (reduced build 176.47).

**Weak spots to prove, not trust:** the stakes (pull-test each to 300 N), the plate alloy (must be 6061), and the frame's sideways stiffness (no diagonals).
