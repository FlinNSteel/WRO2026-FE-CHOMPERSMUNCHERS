# Design Overview
Rational behind chassis engineering choices, mechanical adjustments, physical iterations, and potential future improvements.

---
### Why lego?
As an up and coming team, there was bound to be a lot of trial and error with basic concepts which would mean lots of prototyping on parts that seemed "simple" or "basic". Which is why the lego "Spike" kit was ideal for us, with lego providing a solid toolset with all the basic materials needed for the robot along with the proper flexibility to commit any changes needed on the fly, we are planning in the future to pivot towards more professional hardware such as switching out the lego hub for a raspberry or audino, however lego ended up being the best option for the time being since most of the team members had little to no experience with electronics, making this is a perfect opportunity to ensure a decent amount of customizability without overwhelming any of the members with details like learning breadboards or soddering.

### Basic Structure and framing
We aimed to make the robot as lightweight as possible while still not compromising on stability, which would be crucial specially at higher speeds as the challenge went on and more optimizations were added. For this we connected a "main frame" of sorts to the bottom of a hub to act as an anchor for all the other parts of the robot, with side parts like the sensors being placed directly on the sides connected to technic beams as to make sure they did not interfere with any of the drive's business. The structure uses long beams, cross connectors, and double supports to reduce flexing when the robot turns or changes direction. This helps prevent the chassis from deforming under the approximate weight of 1.34 kg.

We were not too worried on trying to make it so that our robot could hit a full 360 on rotations, as there were very little situations during the challenge where we saw that we would need an inmideate turn beyond 90 degrees, instead opting for an ackermann steering (more details below). This mainly happened as our drive motor and steering motor were relatively the same (as they were the type of motors provided by the kit), however with one having the angle repourposed to become a built in encoder of sorts which was especially helpful during segments like parking where maximum precision was needed, although we didn't try too hard to get a full specialized encoder made specifically for that purpose as it was not used enough for that to make too much of a difference.

### Ackermann steering

As our robot has limited power to use with the wheel, ackermann sterring permitted us to be able to invest as much of that power as possible fueling every turn and letting as much of that power be invested in just two of the wheels (resulting in more power by result) instead of having to try to get the motor to feed every single wheel at a time. To further add speed to this setup, we opted for a gear up mechanism, with this being the best way to increase speed as much as possible without compromising on weight or not adding too many things as to not overwhelm the motors.

<img src="https://i.postimg.cc/TwcCTBw1/New-ACCURATE-Ackermann.png">

This ~3:1 reduction between gears cascading downwards towards the motor (from largest to smallest) allowed for a lot less work to be needed from the motor and so a much smoother and quicker robot.

<img src="https://i.postimg.cc/rp4kbcRj/Back-view.png" width="50%" height="50%">
      *Guided back view of the robot, the gears are right behind the "drive motor" area".
 
