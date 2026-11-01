# Research: ELECFREAKS Nezha Inventor's Kit (EF08232) for BBC micro:bit

Purpose: support a Greek teacher guide for primary teachers (ages 8-12), zero programming experience.
Research date: 2026-10-31. Language: English.

## 0a. VERIFIED ADDENDUM (read in a real browser, 2026-10-31 — supersedes conflicting items below)

**Packing list (official image on the kit intro page):**
Electronics: 1x Nezha Expansion Board, 1x Trimpot, 1x Soil Moisture Sensor, 1x Green LED, 1x Yellow LED, 1x Red LED, 1x Line Tracking Sensor, 1x Crash Sensor, 1x Sonar:bit, 2x Motors, 1x Servo, 1x USB Cable, 5x RJ11 Cables, **1x Map** (printed line-following track — so Case 11 does NOT need black tape).
Bricks: 400+ Technic-style pieces (beams, axles, gears, wheels x2 large, pins etc.). Exact per-type counts visible in the image; no divider inserts.
micro:bit: NOT included (confirmed).

**Board version:** the kit's specs (900 mAh / 3.3 Wh, 5 V charging, 2 h runtime) match the **original Nezha Expansion Board V1 (EF05043)**, not Nezha Pro. Official specs: charging 5 V, charging time 120 min, battery 3.3 Wh, continuous use ~2 hours, 4 servo + 4 motor + 7 sensor RJ11 ports, motor output 5 V. → MakeCode extension to use is **"nezha"** (not "nezha2"). Board page also confirms the extension-incompatibility warning and gives a motor/servo test program (https://makecode.microbit.org/_8g40hhK9rLvW).

**Safety page (read in full):** titled "Nezha Precautions for Use" but text copy-pasted from Nezha-A: (1) do not use while charging; (2) no water/detergent, clean with alcohol-moistened cloth; (3) no paper/dust/gum in connectors; (4) do not disassemble; (5) keep away from fire; (6) long-term storage in a bag in a clean dry box. 360° servo: adjust angle before building to avoid it getting stuck (debug procedure is an image). PlanetX sensors: same precautions 2–6.

**MakeCode Greek UI:** confirmed available via https://makecode.microbit.org/?lang=el (and the Language menu). Translation is PARTIAL — menu items like "Τα έργα μου", "Νέο έργο", "Μαθήματα", "Έναρξη μαθήματος" are Greek, but tutorial titles and some labels stay English. Block names in the PlanetX/nezha extensions are English only. The guide should show both Greek UI terms and English block names.

## 0. Reliability notes (read first)

- The wiki index page, the kit intro page ("Nezha Inventor Kit"), the `safety_instructions` page and the packing-list image all returned EMPTY or navigation-only content to the fetch tool (JavaScript-rendered / images). Their content could NOT be read directly. Sections 1, 2 and 4 therefore combine: (a) the official shop page text, (b) the "Materials Required" lists on each case page, (c) the Nezha board wiki pages, and (d) web-search summaries. Each item is tagged with its source type. Verify against the physical box and the packing-list image before printing in the guide.
- Working URL pattern for case pages (fetched successfully):
  `https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_NN`
  (NN = 01..76). The pattern `.../case-01` suggested in the task does NOT exist.
- All MakeCode programs on the wiki are screenshots (images). I could not see the blocks. Block counts below are ESTIMATES inferred from the case description and result text, not counted. Build step counts (images) are counted only where the raw markdown source was readable (cases 01, 02, 04, 07, 08, 10, 17).
- Several wiki pages contain copy/paste errors (flagged per case). Case pages 21, 27, 48, 50, 54 are formatted differently from the others (older pages, fewer details).

## 1. Box contents

### 1.1 What the shop page says (source: shop.elecfreaks.com product page, EF08232)
- Product name: "ELECFREAKS micro:bit Nezha 48-in-1 Inventor's Kit" (wiki title: "48 IN 1 Nezha Inventor's kit (EF08232)").
- Description: "Based on Planet X sensors... designed for BBC micro:bit. It contains multiple sensors and modules including LED, trumpet [sic, = trimpot], soil moisture sensor, ultrasonic sensor, crash sensor, line-tracking sensor, etc., and also over 400 pieces of building bricks."
- Highlights: 48+ projects; colour recognition system (match port colour to sensor label); "11 Electronic Modules"; MakeCode, Python and C++ (also JavaScript); LEGO and Fischertechnik compatible; storage box with compartments and handle.
- Specs: box 270 x 210 x 74 mm; battery "900mA lithium battery"; input 5V; charging current 1A; communication IIC, UART, SPI.
- Price seen: USD 149 sale / 212 regular (varies by reseller; some resellers call it "36-in-1").
- micro:bit: **NOT included** in the standard SKU. Shop FAQ: "No, the micro:bit board is not included in this kit." A separate bundle "with micro:bit" exists. The wiki URL slug and the shop URL both say "without-micro-bit-board".
- Shop FAQ: "Can multiple students use one kit? Yes ... work together to build, program, and test."
- Shop FAQ: remote-control projects need an additional Joystick:bit V2 Kit and a second micro:bit.
- Shop FAQ: Nezha 48-in-1 kit and "Nezha Inventor's Kit V2" are DIFFERENT products with some different parts. Make sure the school's box is the 48-in-1 (EF08232) and use the 48-in-1 wiki, not the V2 wiki.
- The packing list itself is an image (not readable).

### 1.2 Components named on the case pages (source: "Materials Required" lists; exact wiki names)
Connection type is as stated in the cases' Connection Diagram text.

| Component (wiki name) | What it does | Connection (as used in cases) |
|---|---|---|
| Nezha expansion board / "Nezha Breakout Board" | Main board; micro:bit slots in; power + ports | n/a |
| LED-red, LED-green, LED-yellow | Output lights | J1-J4 via RJ11 |
| Crash sensor | Button-like touch/crash input | J1 (case 04) |
| Soil moisture sensor | Reads soil wetness | J2 (case 02) |
| Potentiometer ("Trimpot") | Knob, analog input | J1 (cases 08, 10) |
| Line-tracking sensor | Detects black line | J1 (case 11) |
| Sonar:bit / "sonar sensor" / "Ultrasonic Sensor" | Distance sensor | J1 (cases 03, 09, 12, 27, 54) |
| Motor (high speed building-blocks motor) | DC motor for fans/wheels | M1 (and M4 for two-motor cars) |
| 360° servo ("geekservo", "360° Gray Block Servo") | Continuous-rotation servo | S1 |
| RJ11 wires (4P4C) | Cables to J ports | 1-3 per case |
| Building bricks ("over 400 pieces", wheels, gears, beams) | Chassis/structures | LEGO-style |
| Storage box | Compartments + handle | n/a |

Other items implied but unverified: USB cable (listings mention one), buzzer/other modules making up the "11 electronic modules". Not named on any case page I read: batteries, USB cable, brick counts per case.

Not in the kit (needed by specific cases): ELECFREAKS Interactive Coding Accessories Pack (Rainbow LED, Segment sensor etc.; cases 69, 76), black electrical tape + white surface (case 11), a plant with soil and water (case 02), a second micro:bit (case 69, remote-control cases in general).

### 1.3 Connection types
- J1-J4 (case pages use J1, J2, J3, J4): sensor ports via RJ11 4P4C. Nezha Pro board page says IO ports have yellow (analog) or red (digital) labels; IIC ports have blue labels; motor connectors have a red round label. Original Nezha page: "four servos connections, four motors connections and seven sensors connections."
- IIC: separate blue-labelled ports on the board (used by I2C sensors; not required by the cases analysed).
- Motors: M1-M4 (cases use M1; two-motor cars use M1 and M4).
- Servos: S1-S4 (cases use S1).

### 1.4 Batteries and power
- No AA/AAA batteries are described anywhere in the sources. The Nezha board has a built-in rechargeable 900 mAh lithium battery (shop spec). It charges at 5V / 1A (shop) via USB. The micro:bit is powered from the board when it is slotted in and the board is switched on.
- Therefore the board must be CHARGED before the lesson (see 2).
- Wiki case pages mention no battery installation steps.

## 2. Nezha breakout board

Caveat: the kit page and case pages call it "Nezha expansion board" / "Nezha Breakout Board". I could not confirm whether the EF08232 box contains the original Nezha (EF05043) or a Nezha Pro/V2 (EF02055 / EF05070). Two shop-page images say "Nezha Pro expansion board" in alt text, but the kit's own spec says 900 mAh / 5V / 1A charging, which differs from Nezha Pro (7.4V, 3A Type-C). VERIFY the board in the physical kit. Extension to use depends on the version (see 3).

Facts (source: wiki pages for Nezha EF05043 and Nezha Pro EF05070, shop page):
- Slot: micro:bit edge connector; board holds the micro:bit in place.
- Ports: 4 motor, 4 servo (original), 7-8 sensor RJ11 connectors; all RJ11 with anti-misplug (fool-proof) design.
- Power switch: Nezha Pro has a "slide power switch"; shop image of the kit board shows "power switch" and "USB charge".
- Battery indicator LEDs (Nezha Pro): 4 LEDs show 1-25 / 26-50 / 51-75 / 76-100 % when discharging; flashing while charging; all lit = full, then disconnect charger.
- Nezha Pro charging: 5V 3A Type-C, about 50 min; max 45 min continuous run with heavy load. (Kit-board spec 1A, so charging likely slower; check.)
- Nezha Pro: two motor control buttons can spin a motor without the micro:bit.
- Sensor port output 3.3V, max 1.0A; motor output 6.4-8.4V (Pro).
- Case 09 and case 17 say "buzzer on the micro:bit" - this is the micro:bit V2 speaker, not a Nezha board buzzer. I found no buzzer on the Nezha board in the sources.
- Teacher must-knows: charge fully before class; check board switch is ON; micro:bit must be pressed fully into slot; match RJ11 ports exactly to the case diagram (J1 vs J2 mistakes are the most common failure); do not use while charging (from Nezha-A safety page, see 4).

## 3. Software setup

- MakeCode: https://makecode.microbit.org (all cases link to makecode.microbit.org shared projects).
- Procedure (identical wording on every case page): in MakeCode click "Advanced" to open more categories, then "Extensions" at the bottom of the drawer, then search and add:
  - search "PlanetX" for sensors (LED, sonar, potentiometer, soil moisture, crash, line-tracking, rainbow, etc.);
  - search "nezha" for motors/servos on the original Nezha board (cases using M or S ports).
  - Nezha Pro / V2 board: wiki says search "nezha2" instead. (Kit board version unconfirmed.)
- Source repos (confirmed, fetched): github.com/elecfreaks/pxt-PlanetX and github.com/elecfreaks/pxt-nezha. Extension names shown in MakeCode: "PlanetX" and "neZha". Blocks in code samples appear as `neZha.setMotorSpeed(neZha.MotorList.M1, 100)` and `PlanetX.Ultrasoundsensor(PlanetX.DigitalRJPin.J1, ...)`.
- Wiki warning: if MakeCode says some extensions will be removed for incompatibility, continue or create a new project. Practical consequence: add PlanetX first, and use ONE project per case; do not mix with other extensions. Easiest for teachers: open the case's "Reference Link" shared project (makecode.microbit.org/_xxxx) so extensions are preloaded.
- Which extensions each case needs (per page text): PlanetX only: 02, 04, 07, 09, 17, 37. nezha only: 06, 21, 27, 48, 50, 54. Both: 01, 03, 08, 10, 11, 12, 69. 76: PlanetX only (per page).
- NOT from the wiki (general micro:bit knowledge, verify): flashing via USB either by (a) drag-and-drop the downloaded .hex onto the MICROBIT drive (works on Windows, macOS, ChromeOS, Linux), or (b) WebUSB "Connect device / Download" in Chrome or Edge (works on Windows 10/11 and ChromeOS; not Firefox/Safari). Windows 10+ needs no driver for micro:bit V2. WebUSB may be blocked by school policies; drag-and-drop is the fallback. The wiki pages I read do not mention drivers.
- All cases need internet for MakeCode (online editor) unless the offline Windows app is used (PlanetX/nezha extensions load from GitHub, so offline is problematic).
- Checks for a teacher setup day: confirm school network allows makecode.microbit.org and GitHub (extension download), and that USB data cables (not charge-only) work.

## 4. Safety instructions page

The page returned no content to the fetch tool. Summary below is from search-result excerpts of the sibling Nezha-A (Arduino) page, so only partially applicable. The wiki index lists sections: "Nezha-A Precautions for Use", "360° Gray Block Servo Precautions for Use", "Notes on the use of PlanetX series sensors".
- Do not use the control box while it is charging.
- Do not clean with detergent or water; wipe with alcohol on a cloth.
- Keep paper, dust and gum out of connectors.
- Do not disassemble; keep away from fire; store dry and clean.
- 360° servo: adjust/zero its angle before building so it does not get stuck (details not retrieved).
- PlanetX sensors: same precautions as the control box.
- Nezha Pro/V2 power guidance: disconnect power and store safely when not used for long periods; keep power connector away from humidity and dust.
- General for classrooms (other ELECFREAKS safety page): keep fingers away from moving parts (pinching), dry hands before touching boards, adult supervision for younger users.
- Lithium battery in board: charge under supervision, do not charge unattended or overnight in a bag.
ACTION: have someone open the real safety page in a browser and confirm before the guide quotes it.

## 5. Case analysis

Scale: Teacher difficulty (TD) and Student difficulty (SD) 1-5 (5 = hardest), for primary teachers with zero experience and ages 8-12 working in groups of 2-3. Block counts and times are estimates. Time = build + code for a first-time class group, in minutes. Build complexity inferred from number of assembly images where known (L = under 8 steps, M = 8-15, H = more than 15), otherwise from the model type.

Common to all cases: needs micro:bit (V2 recommended), Nezha board charged and on, PlanetX and/or nezha extension added, correct RJ11 port. Common failure points: wrong J port; RJ11 not clicked in; extension not added (blocks missing); board switched off or battery flat; micro:bit not fully inserted; micro:bit program not flashed (still old program).

### Case 01 - The Mechanical Shrimp (skim)
- Source: wiki case 01 (raw page read).
- Components: Ultrasonic Sensor (J1), geekservo (S1), two motors (M1, M4), Nezha Breakout Board.
- NOT "motor only": it uses sonar for obstacle detection, so it is an if-then project.
- Build: HIGH, 33 assembly images. Code: if-then on distance, ~10-20 blocks (estimate). Concepts: forever loop, if/else, sensor threshold, motor/servo blocks.
- Time: 60-90 min. Failure: long build, servo orientation, both extensions needed. TD 3, SD 4. Justification: long mechanical build and a sensor-driven turn decision; not a first lesson.

### Case 02 - Flower-watering Prompter
- Source: wiki case 02 (raw page read). Components: LED-red (J3), LED-green (J4), Soil moisture sensor (J2), 3 RJ11. Extension: PlanetX only.
- Build: M-L, 8 assembly images. Concepts: forever loop, if/else, sensor threshold on moisture. ~8-12 blocks (est.). Time 40-50 min.
- Failure points: threshold wrong for the actual soil (needs calibration, needs real plant/soil/water in a computer-lab setting); wrong LED port; sensor probe not in soil.
- TD 2, SD 2. Justification: one sensor, two LEDs, one if/else; real-world and relatable. Good first sensor case but needs soil/water.

### Case 03 - Automatic Gate
- Source: wiki case 03 (read). Components: 360° servo (S1), Sonar:bit (J1), 1 RJ11. Extensions: PlanetX and nezha. Page has an assembly video.
- Build: M (images not counted). Concepts: forever loop, if/else on distance threshold, servo angle/rotation blocks. ~10-15 blocks (est.). Time 50-60 min.
- Failure: 360° servo needs correct start position (safety page: set angles before building); gate opens/closes too far or keeps spinning (360° servo is continuous, so timing matters); distance threshold; two extensions at once.
- TD 3, SD 3. Justification: continuous servo behaviour is non-obvious; otherwise if/else.

### Case 04 - Mini Table Lamps
- Source: wiki case 04 (raw read). Components: Crash sensor (J1), LED-yellow (J2), 2 RJ11. Extension: PlanetX only.
- Build: L-M, 9 assembly images. Concepts: event (on pressed/if sensor pressed), toggle/if-then, maybe a variable. ~5-8 blocks (est.). Time 30-40 min.
- Failure: sensor logic (is it "pressed" or "released"); LED stays on; port mix-up.
- TD 1-2, SD 1-2. Justification: one input, one output; best first project.

### Case 06 - Temperature-controlled Fan
- Source: wiki case 06 (read). Components: Motor (M1). NO extra sensor: uses the micro:bit's own temperature reading. Extension: nezha only.
- Build: L-M (steps not counted). Concepts: if/else with a threshold on temperature, motor speed. ~6-10 blocks (est.). Time 30-40 min.
- Failure: classroom temperature may never reach the threshold (kids must warm the micro:bit by hand or change the threshold); micro:bit temperature is the chip's, sluggish; motor direction/fan blades.
- TD 2, SD 2. Justification: simple if/else but the testing needs a threshold tweak.

### Case 07 - Smart Lamps
- Source: wiki case 07 (raw read). Components: LED-yellow (port in image only), 1 RJ11. Uses the micro:bit's built-in light level (LED matrix). Extension: PlanetX only.
- Build: L, 7 images. Concepts: if/else on light level threshold, forever. ~6-9 blocks (est.). Time 30-40 min.
- Failure: light threshold depends on classroom lighting (must test by covering the micro:bit with a hand); micro:bit light sensing is rough.
- TD 2, SD 2. Justification: single threshold; very visible result.

### Case 08 - Speed Adjustable Fans
- Source: wiki case 08 (raw read). Components: Potentiometer (J1), Motor (M1), 1 RJ11. Extensions: PlanetX and nezha.
- Build: M, 13 images. Concepts: forever loop, reading an analog value and mapping it to motor speed (maybe a variable and "map" block). ~5-8 blocks (est.). Time 45-55 min.
- Failure: 0-1023 value must be mapped to speed 0-100 (new idea for kids); motor stalls at low speed; two extensions.
- TD 3, SD 3. Justification: analog-to-speed mapping is the first "variable-like" idea.

### Case 09 - Invading Detection Device
- Source: wiki case 09 (read). Components: Sonar:bit (J1), LED-red (J2), LED-green (J3), 3 RJ11. Uses the micro:bit's buzzer. Extension: PlanetX only (page text).
- Build: M. Concepts: forever loop, if/else on distance threshold, LED on/off, play sound/tone. ~10-15 blocks (est.). Time 45-60 min.
- Failure: buzzer requires micro:bit V2 (V1 has no speaker); noise in a 6-7 kit classroom (all alarms at once); distance threshold; classmates keep triggering it.
- TD 2-3, SD 3. Justification: if/else with sensor and two outputs; sound adds classroom-management cost.

### Case 10 - Speed Adjustable Car
- Source: wiki case 10 (raw read). Components: Potentiometer (J1), Motors x2 (M1, M4), 1 RJ11. Extensions: PlanetX and nezha.
- Build: HIGH, 19 images. Concepts: analog value to speed for two motors (same as case 08), forever. ~6-10 blocks (est.). Time 60-75 min.
- Failure: motors mirrored so car goes backwards or spins (one motor needs reverse); wheel/axle bricks; car runs off the table while testing.
- TD 3, SD 3. Justification: long build; code is simple but the motor direction trap is common.

### Case 11 - Line-tracking Car
- Source: wiki case 11 (read). Components: Line-tracking sensor (J1), Motors x2 (M1, M4), 1 RJ11. Extensions: PlanetX and nezha. Needs black electrical tape on a white surface (NOT in kit). No assembly video listed on this page.
- Build: HIGH. Concepts: forever loop, if/else if/else with sensor states (nested conditions), motor speed per side. ~15-25 blocks (est.). Time 75-90 min.
- Failure: sensor height above floor; track too tight; speeds too high; ambient light/ floor colour; wrong turning direction logic; tape needed.
- TD 4, SD 4. Justification: multi-branch sensor logic and tuning.

### Case 12 - Obstacles Avoidance Car
- Source: wiki case 12 (read). Components: Sonar:bit (J1), Motors x2 (M1, M4), 1 RJ11. Extensions: PlanetX and nezha.
- Build: HIGH. Concepts: forever loop, if/else on distance, turn sequence (pause/timing), motor speeds. ~12-20 blocks (est.). Time 75-90 min.
- Failure: car turns too little/too much; falls off table; sonar blind to soft/angled objects; multiple cars interfering with each other's ultrasonic in the same room.
- TD 4, SD 4. Justification: autonomous car with tuning; ultrasonic cross-talk in a lab.

### Case 17 - Alarm Device
- Source: wiki case 17 (raw read). Components: LED-red (J1), 1 RJ11, "Bricks x n". Uses the micro:bit's buzzer and button A. Extension: PlanetX only.
- Build: L, 5 images. Concepts: event (button A), toggle with a variable (alarm on/off), forever loop with LED flashing and sound. ~10-15 blocks (est.). Time 35-45 min.
- Failure: micro:bit V2 required for sound; toggle logic (press again to cancel) is the first real variable/state concept; flashing LED loop vs button check; noise.
- TD 3, SD 3. Justification: needs state memory (a variable) which beginners find hard.

### Case 21 - An Oscillating Fan
- Source: wiki case 21 (read; older page format). Components: 360° servo (S1), Motor (M1), "Bricks x n". Uses buttons A and B. Extension: nezha only. Video link exists; no step images text.
- Build: MED-HIGH (motor + servo swing mechanism). Concepts: button events (A on, B off), forever loop sweeping servo left/right, pauses. ~10-15 blocks (est.). Time 60-75 min.
- Failure: 360° servo swing needs timed rotation (not an angle); mechanism binds; swing too wide.
- TD 3, SD 3. Justification: events only but mechanical timing; good showpiece.

### Case 27 - The Distance Indicator
- Source: wiki case 27 (read; older format). Components: Sonar:bit (J1), micro:bit V2 explicitly ("micro:bit V2 x 1"), "Bricks x n". Extension: nezha (page says search "nezha"; the sonar blocks come from PlanetX so likely also needs PlanetX; page text inconsistent).
- Build: L-M (small wearable holder). Concepts: forever loop, read sensor into a number, show number on the LED display (possibly a variable). ~4-6 blocks (est.). Time 25-35 min.
- Failure: wiki inconsistency about extensions; number scrolls too fast to read; sonar reads 0 when nothing in range.
- TD 1-2, SD 2. Justification: smallest code in the set; great for introducing "variable shown on screen". Easy start. Note the wiki theme is "social distance / epidemic" - consider re-theming for kids.

### Case 37 - Traffic Lights
- Source: wiki case 37 (read). Components: LED-red (J1), LED-yellow (J2), LED-green (J3), 3 RJ11. Extension: PlanetX only.
- Build: L-M. Concepts: sequence, forever loop, pause (wait) timings 5 s / 2 s / 5 s. ~8-12 blocks (est.). Time 35-45 min.
- Failure: wiring colour order; LED port reversal (LED polarity is handled by the module); timing not as expected.
- TD 1-2, SD 1-2. Justification: pure sequence and loop, easiest to explain, familiar real-life theme. Strong first project, no sensors.

### Case 48 - The Walking Robot (skim)
- Source: wiki case 48 (read; minimal page). Components: "Nezha Inventor's Kit", motor(s) on M1 (page says "motors ... to M1"). Extension: nezha only. Buttons: A moves forward, B stops.
- Pure mechanical + motor. Build HIGH (walking linkage; page has component list/steps as images not readable). Concepts: events only (A start, B stop). ~4-6 blocks (est.). Time 60-90 min (build dominated).
- Failure: linkage alignment, motor speed; page text is sparse.
- TD 2, SD 3. Justification: trivial code, difficult mechanics.

### Case 50 - A Small Trash Can
- Source: wiki case 50 (read; older page, mentions "Nezha-A Master Box" = copy error). Components: Motor on M1. Extension: nezha only. A opens lid, B closes it.
- Build: MED. Concepts: events only; motor run for a time (pause) or motor speed. ~6-10 blocks (est.). Time 45-60 min.
- Failure: motor runs too long and jams the lid (timing needs tuning); lid mechanism; "Materials" section is blank on the page.
- TD 2, SD 2. Justification: button events + timing; simple.

### Case 54 - Happy Seesaw
- Source: wiki case 54 (read; older page). Components: Sonar:bit (J1), Motors on M1 (page also mentions programming "the servo" - inconsistent). Extension: nezha only (page); sonar blocks need PlanetX in practice (page text omits it).
- Build: MED-HIGH. Concepts: forever, if/else on distance, motor/servo movement. ~8-14 blocks (est.). Time 60-75 min.
- Failure: wiki inconsistency (servo vs motor, missing PlanetX); seesaw mechanical stops; objects pushed off.
- TD 3, SD 3. Justification: sensor + motion; unclear wiki text increases teacher prep.

### Case 69 - The Trimpot Remote Control Car
- Source: wiki case 69 (read). Components: "ELECFREAKS micro:bit Nezha 48 IN 1 Inventor's Kit" + "ELECFREAKS Interactive Coding Accessories Pack" (sold separately). Remote handle: 2 Potentiometers (J1, J2) + Rainbow LED (J3). Car: two motors (page says "two Potentiometers to M1 and M2" - typo for motors). Two programs (car, handle) -> TWO micro:bits, TWO Nezha boards (or one board plus another power source), radio link. Extensions: PlanetX and Nezha.
- Build: VERY HIGH (two structures). Concepts: radio send/receive, variables, mapping, comparison of two values, LED ring display. ~20-35 blocks total (est.). Time 120+ min (likely two sessions).
- Failure: radio group mismatch between micro:bits; interference from other kits in the same room (all groups must use different radio groups); needs second micro:bit and second board.
- TD 5, SD 5. Justification: two devices + radio + variables; unsuitable for target audience and kit count (see 6).

### Case 76 - The Tomato Clock
- Source: wiki case 76 (read). Components per page: "ELECFREAKS micro:bit Nezha 48 IN 1 Inventor's Kit", "ELECFREAKS PlanetX Segment Sensor", "ELECFREAKS PlanetX Rainbow LED" (accessory pack, not in the 48-in-1 kit list). Connection text mentions "Dust Sensor to J1 and Motor Fan to J2" - clearly a copy error, so the real wiring is unknown. Extension: PlanetX only. Result text: "Countdown to 25 seconds" (demo; real Pomodoro = 25 minutes).
- Build: MED. Concepts: variables (countdown), loop, display of number on segment display, music/lights at end, probably a start event. ~15-25 blocks (est.). Time 60-75 min.
- Failure: missing parts (Segment Sensor, Rainbow LED); wiring text wrong; countdown timing; music needs V2 speaker.
- TD 4, SD 4. Justification: depends on parts not in the kit, unclear wiring, variable-based countdown.

### Summary ranking (easiest to hardest, for guide sequencing)
1. 37 Traffic Lights (TD1-2 / SD1-2): sequence only, no sensor.
2. 27 Distance Indicator (1-2 / 2): sensor to screen.
3. 04 Mini Table Lamps (1-2 / 1-2): one sensor, one LED.
4. 07 Smart Lamps (2 / 2) and 06 Temperature-controlled Fan (2 / 2): single thresholds, built-in sensors.
5. 02 Flower-watering Prompter (2 / 2), 50 Small Trash Can (2 / 2), 48 Walking Robot (2 / 3).
6. 09 Invading Detection Device, 17 Alarm Device, 03 Automatic Gate, 08 Speed Adjustable Fans, 10 Speed Adjustable Car, 21 Oscillating Fan, 54 Happy Seesaw (3).
7. 11 Line-tracking Car, 12 Obstacles Avoidance Car, 01 Mechanical Shrimp (3-4).
8. 76 Tomato Clock (4), 69 Trimpot Remote Control Car (5).

## 6. Flags against "6-7 kits, groups of 2-3 kids, school computer lab"

1. micro:bits are NOT included. Schools need 6-7 micro:bits, preferably V2 (cases 09, 17, 27, and any music/alert feature need the V2 speaker; case 27 states "micro:bit V2"). V1 will not play the buzzer.
2. Case 69 needs 2 micro:bits and 2 boards (remote + car) and the accessories pack. With 6-7 kits this means two kits per group or a teacher demo only.
3. Cases 69 and 76 need the separately sold "Interactive Coding Accessories Pack" (Rainbow LED, Segment Sensor). Not in the 48-in-1 kit. Case 69 also requires radio groups per team.
4. Case 11 needs black electrical tape and a white surface; case 02 needs a plant, soil and water; cars need floor space (cases 10, 11, 12) - lab desks are small; risk of cars driving off tables.
5. Radio and ultrasonic cross-talk: 6-7 groups running sonar (cases 03, 09, 12, 27, 54) at the same time can interfere; space groups apart. Radio cases (69) require unique group numbers per team.
6. Battery: board has a built-in 900 mAh lithium battery with USB charging (shop spec). 6-7 boards need to be charged before class, and charge time and runtime (45 min max on Nezha Pro under heavy load) limit longer builds and cars. Plan a charging station and spare time. No AA batteries described.
7. Build time: cars and mechanical cases (01, 10, 11, 12, 48, 69) take 60-120 min; for ages 8-12 one 45-min lesson is not enough. Budget two sessions or pre-build.
8. Computer lab: MakeCode needs internet and access to GitHub-hosted extensions; WebUSB works in Chrome/Edge only (general knowledge); school filters may block it. Test beforehand. Lab computers must supply a USB port for each micro:bit (USB data cable).
9. Wiki quality: cases 21, 27, 48, 50, 54, 69, 76 have sparse, inconsistent or copy-pasted text (wrong board names like "Nezha-A Master Box", wrong parts "Dust Sensor"/"Motor Fan", servo vs motor, missing extension). The guide cannot rely on the wiki text alone for those; check against the physical build.
10. The kit's component list in the box could not be confirmed: kit intro page and packing-list image were unreadable. Verify the physical contents against the case materials lists.
11. Kit versions: the 48-in-1 (EF08232) vs Nezha Inventor's Kit V2 vs 36-in-1 (reseller naming) are different. Nezha board version (original vs Pro/V2) changes the extension ("nezha" vs "nezha2") and charging details.
12. Safety: lithium battery inside board; supervise charging; moving motors/servos (pinch); small bricks for younger children.
13. Cases 02, 06, 07 depend on environmental values (soil, room temperature, light) so thresholds need calibration; plan 5 minutes for it.

## 7. Sources (URLs actually fetched)

Fetched with readable content:
- https://www.elecfreaks.com/learn-en/_sources/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha_Inventor_s_kit_for_microbit_case_01.md.txt
- https://www.elecfreaks.com/learn-en/_sources/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha_Inventor_s_kit_for_microbit_case_02.md.txt
- https://www.elecfreaks.com/learn-en/_sources/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha_Inventor_s_kit_for_microbit_case_04.md.txt
- https://www.elecfreaks.com/learn-en/_sources/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha_Inventor_s_kit_for_microbit_case_07.md.txt
- https://www.elecfreaks.com/learn-en/_sources/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha_Inventor_s_kit_for_microbit_case_08.md.txt
- https://www.elecfreaks.com/learn-en/_sources/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha_Inventor_s_kit_for_microbit_case_10.md.txt
- https://www.elecfreaks.com/learn-en/_sources/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha_Inventor_s_kit_for_microbit_case_17.md.txt
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_03
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_06
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_09
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_11
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_12
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_21
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_27
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_37
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_48
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_50
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_54
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_69
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_76
- https://shop.elecfreaks.com/products/elecfreaks-micro-bit-nezha-48-in-1-inventors-kit-without-micro-bit-board
- https://wiki.elecfreaks.com/en/microbit/expansion-board/nezha
- https://wiki.elecfreaks.com/en/microbit/expansion-board/nezha-v2
- https://github.com/elecfreaks/pxt-nezha
- https://github.com/elecfreaks/pxt-PlanetX
- https://learn-en.readthedocs.io/en/latest/microbitKit/Nezha_Inventor_s_kit_for_microbit/index.html (navigation only; gave the full list of the 76 case titles and the section names; kit content not shown)

Fetched but returned empty or navigation-only (no usable content):
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/ (index, kit intro) - empty
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha-Inventor-s-kit-for-microbit - empty
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/safety_instructions - empty
- https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/case-02 (suggested pattern; does not exist) - empty
- https://www.elecfreaks.com/learn-en/microbitKit/Nezha_Inventor_s_kit_for_microbit/Nezha-Inventor-s-kit-for-microbit.html - empty
- https://www.elecfreaks.com/learn-en/microbitKit/Nezha_Inventor_s_kit_for_microbit/safety_instructions.html - navigation only
- several .md.txt variants for cases 03, 06, 09, 11, 12, 21, 27, 37, 48, 50, 54, 69, 76 and the intro/safety pages - empty (replaced by the wiki.elecfreaks.com URLs above)
- learn-en.readthedocs.io case 03, 06, 09, 11 pages - navigation only

Web searches used (for context, not primary): searches on the kit, the case 02 page, and the Nezha safety/battery pages; their results cited: core-electronics.com.au, rs-online.com listings (kit naming, 400+ bricks, 900 mAh battery), wiki.elecfreaks.com Nezha-A safety page (Arduino sibling).
