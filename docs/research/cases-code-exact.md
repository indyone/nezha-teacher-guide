# Nezha Inventor's Kit - exact MakeCode programs (17 cases)

Source: ELECFREAKS wiki case pages, MakeCode share links, `https://makecode.com/api/_ID/text` (main.ts, main.blocks, pxt.json).
Block count = number of `<block>` elements in main.blocks, shadows excluded (counted programmatically in the browser from the XML).
Screenshot host path prefix `P` = `/var/folders/ts/wskdgfmx35bc25gwhyvb1trw0000gp/T/claude-hostloop-plugins/00331c47cabcb001/projects/session/cb774c68-d3ff-4755-af88-742482efbe9c/tool-results/mcp-claude-in-chrome-blob-`
Screenshots: Greek editor UI (`?lang=el`), Blocks view, 1445x840 JPEG. Case 08 was zoomed out once (the map block is wider than the workspace). In cases 02 and 37 the "on start" block partly overlaps the "forever" block, which is how the original author placed them.

## Summary table

| Case | Title | Blocks | Extensions (pxt.json, excluding core/radio/microphone) | Concepts | Ports |
|---|---|---|---|---|---|
| 02 | Flower-watering Prompter | 12 | pxt-PlanetX v0.13.1 | on start, forever, variable, if-else, comparison | J2 soil, J3 red LED, J4 green LED |
| 03 | Automatic Gate | 15 | pxt-PlanetX v1.4.5, pxt-nezha v1.3.6 | on start, forever, variable, if-else, comparison, AND, pause | J1 sonar, S1 servo 360 |
| 04 | Mini Table Lamps | 17 | pxt-PlanetX v0.13.1, pxt-nezha v1.1.5, pxt-TPBot v1.1.1 | on start, forever, 3x if (no else), variable toggle (1 - i), arithmetic, comparison, pause | J1 crash, J2 LED |
| 06 | Temperature-controlled Fan | 8 | pxt-PlanetX v0.13.1, pxt-nezha v1.1.5, pxt-TPBot v1.1.1 | on start, forever, if-else, comparison, built-in temperature | M1 |
| 07 | Smart Lamps | 6 | pxt-PlanetX v0.14.0 | forever, if-else, comparison, built-in light level | J1 LED |
| 08 | Speed Adjustable Fans | 6 | pxt-PlanetX v0.13.1, pxt-nezha v1.1.5, pxt-TPBot v1.1.1 | on start, forever, math map | J1 potentiometer, M1 |
| 09 | Invading Detection Device | 21 | pxt-PlanetX v0.12.0 | on start, forever, variable, 2x if, comparison, AND, music (built-in melody), pause | J1 sonar, J2 red LED, J3 green LED |
| 10 | Speed Adjustable Car | 10 | pxt-PlanetX v0.13.1, pxt-nezha v1.1.5, pxt-TPBot v1.1.1 | on start, forever, variable, math map (0..-100) | J1 potentiometer, M1, M4 |
| 11 | Line-tracking Car | 15 | pxt-nezha v1.1.5, pxt-PlanetX v0.13.1 | on start, forever, 3x if (no else), line-tracking states | J1 tracking, M1, M4 |
| 12 | Obstacles Avoidance Car | 18 | pxt-PlanetX v0.10.6, pxt-nezha v1.1.5, pxt-TPBot v1.1.1 | on start, forever, variable, if, comparison, AND, pause | J1 sonar, M1, M4 |
| 17 | Alarm Device | 13 | pxt-PlanetX v0.13.4, pxt-nezha v1.1.8 | button A event, forever, variable toggle, if-else, arithmetic, music (playTone), pause | J1 LED |
| 27 | The Distance Indicator | 3 | pxt-nezha v1.2.0 | forever, show number (sensor value inline) | J1 sonar |
| 37 | Traffic Lights | 12 | pxt-PlanetX v0.13.1 | on start, forever, sequence, pause | J1 red, J2 yellow, J3 green |
| 50 | A Small Trash Can | 8 | pxt-nezha v1.3.6 | button A event, button B event, pause | M1 |
| 21 | An Oscillating Fan | 27 | pxt-nezha v1.1.8 | on start, 2x forever (parallel), 3x if (one if-else), variables i and j, button polling (is pressed), arithmetic toggle, pause | S1 servo 360, M1 |
| 48 | The Walking Robot | 4 | pxt-nezha v1.3.6 | button A event, button B event | M1 |
| 54 | Happy Seesaw | 14 | pxt-PlanetX v1.3.3, pxt-nezha v1.3.2 | forever, if, comparison, show number, pause | J1 sonar, M1 |

None of the 17 programs uses radio, even though `radio` and `microphone` are listed as dependencies in every pxt.json (default dependencies).

Exact dependency strings (the `pxt-*` ones), per case, are repeated under each case below.

---

## Case 02: Flower-watering Prompter
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_02
- MakeCode: https://makecode.microbit.org/_gmtM095oj1cd
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.1"` (plus core, radio, microphone)
- Blocks: 12
- Concepts: on start (show icon), forever, variable i, if-else, comparison (<)
- Ports: J2 (soil moisture), J3 (red LED), J4 (green LED)
- screenshot_path: `P`1793439467491-or4x0u.jpg
- Wiki vs code: consistent (wiki: green J4, red J3, soil J2; red lights when dry). The threshold 30 is not stated in the wiki. The XML block is named `readsoilmoisture`, TS shows `PlanetX_Basic.soilHumidity` (value 0-100).

```ts
let i = 0
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    i = PlanetX_Basic.soilHumidity(PlanetX_Basic.AnalogRJPin.J2)
    if (i < 30) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, true)
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J4, false)
    } else {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, false)
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J4, true)
    }
})
```

## Case 03: Automatic Gate
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_03
- MakeCode: https://makecode.microbit.org/_MssY8AXgCbkK
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v1.4.5"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.3.6"`
- Blocks: 15
- Concepts: on start (show icon + servo initial angle), forever, variable i, if-else, comparison (> and <) combined with AND, pause
- Ports: J1 (sonar), S1 (360 degree servo)
- screenshot_path: `P`1793439467492-t8y41w.jpg
- Wiki vs code: the wiki says the gate opens when something is detected and closes when no one is near. In the code the gate opens (angle 240) only when 3 < distance < 20 cm, then waits a blocking 5000 ms before re-reading; otherwise it is set to 180 (closed). Readings of 3 cm or less (and 0, i.e. no echo) count as closed. The wiki result line says "detects any object", which is looser than the 3-20 cm window.

```ts
let i = 0
basic.showIcon(IconNames.Heart)
neZha.setServoAngel(neZha.ServoTypeList._360, neZha.ServoList.S1, 180)
basic.forever(function () {
    i = PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm)
    if (i > 3 && i < 20) {
        neZha.setServoAngel(neZha.ServoTypeList._360, neZha.ServoList.S1, 240)
        basic.pause(5000)
    } else {
        neZha.setServoAngel(neZha.ServoTypeList._360, neZha.ServoList.S1, 180)
    }
})
```

## Case 04: Mini Table Lamps
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_04
- MakeCode: https://makecode.microbit.org/_fewiyT73u19K
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.1"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.5"`, `"pxt-TPBot": "github:elecfreaks/pxt-tpbot#v1.1.1"`
- Blocks: 17
- Concepts: on start (show icon), forever, three separate if blocks (no else), variable i used as a toggle (i = 1 - i), arithmetic, comparison (=), pause (debounce 200 ms)
- Ports: J1 (crash sensor), J2 (yellow LED)
- screenshot_path: `P`1793439467492-8vowo1.jpg
- Wiki vs code: wiki says "the crash sensor controls on/off of the LED"; the code is a latching toggle (each press flips i). TPBot is in the dependencies but not used. Note: `i` starts at 0 so the LED is off at startup.

```ts
let i = 0
basic.showIcon(IconNames.Target)
basic.forever(function () {
    if (PlanetX_Basic.Crash(PlanetX_Basic.DigitalRJPin.J1)) {
        basic.pause(200)
        i = 1 - i
    }
    if (i == 0) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, false)
    }
    if (i == 1) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, true)
    }
})
```

## Case 06: Temperature-controlled Fan
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_06
- MakeCode: https://makecode.microbit.org/_Cii8drJYPar5
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.1"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.5"`, `"pxt-TPBot": "github:elecfreaks/pxt-tpbot#v1.1.1"`
- Blocks: 8
- Concepts: on start (show icon), forever, if-else, comparison (>=), built-in micro:bit temperature input
- Ports: M1 (motor); no J port (temperature is the micro:bit's own sensor)
- screenshot_path: `P`1793439574373-88akwt.jpg
- Wiki vs code: consistent (wiki: motor on M1, fan on/off by temperature). Threshold 28 degrees C is not stated in the wiki text. PlanetX is a declared dependency but no PlanetX block is used.

```ts
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    if (input.temperature() >= 28) {
        neZha.setMotorSpeed(neZha.MotorList.M1, 100)
    } else {
        neZha.stopMotor(neZha.MotorList.M1)
    }
})
```

## Case 07: Smart Lamps
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_07
- MakeCode: https://makecode.microbit.org/_haMDD2EftPLV
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.14.0"`
- Blocks: 6
- Concepts: forever, if-else, comparison (<), built-in micro:bit light level
- Ports: J1 (yellow LED)
- screenshot_path: `P`1793439574373-ufs8zk.jpg
- Wiki vs code: the wiki connection text does not name a port ("connect the yellow LED"); the code uses J1. Threshold 10 (light level 0-255) is not stated in the wiki. No "on start" block in this project.

```ts
basic.forever(function () {
    if (input.lightLevel() < 10) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, true)
    } else {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, false)
    }
})
```

## Case 08: Speed Adjustable Fans
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_08
- MakeCode: https://makecode.microbit.org/_3LAMei8MzHij
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.1"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.5"`, `"pxt-TPBot": "github:elecfreaks/pxt-tpbot#v1.1.1"`
- Blocks: 6
- Concepts: on start (show icon), forever, math map (0-1023 to 0-100), no variable
- Ports: J1 (potentiometer), M1 (motor)
- screenshot_path: `P`1793439679519-9l2aqq.jpg (zoomed out once)
- Wiki vs code: consistent (wiki: potentiometer J1, motor M1).

```ts
basic.showIcon(IconNames.Diamond)
basic.forever(function () {
    neZha.setMotorSpeed(neZha.MotorList.M1, Math.map(PlanetX_Basic.trimpot(PlanetX_Basic.AnalogRJPin.J1), 0, 1023, 0, 100))
})
```

## Case 09: Invading Detection Device
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_09
- MakeCode: https://makecode.microbit.org/_2zrE6AKRHbqW
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.12.0"`
- Blocks: 21
- Concepts: on start (show icon), forever, variable i, two separate if blocks (no else), comparison (>, <=), AND, music (built-in melody "ba ding", once), pause
- Ports: J1 (sonar), J2 (red LED), J3 (green LED)
- screenshot_path: `P`1793439574373-3z94uq.jpg
- Wiki vs code: wiki says red LED lights and the buzzer alarms when the object is detected; the code does that only for 5 < i <= 20 cm. Green LED comes on (red off) only for i > 30. For readings of 0-5 and 21-30 cm nothing changes (LEDs keep their previous state; this is a dead zone). The sound is the built-in melody BaDing via `music.startMelody`, not a PlanetX buzzer. Project name in pxt.json is "Untitled".

```ts
let i = 0
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    i = PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm)
    if (i > 5 && i <= 20) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, true)
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, false)
        music.startMelody(music.builtInMelody(Melodies.BaDing), MelodyOptions.Once)
    }
    if (i > 30) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, false)
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, true)
    }
    basic.pause(500)
})
```

## Case 10: Speed Adjustable Car
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_10
- MakeCode: https://makecode.microbit.org/_Ysw6uKC3eUwf (this is the link found in the live page's DOM). NOTE: an earlier text fetch of the same wiki page returned a different link, `https://makecode.microbit.org/_cTDgmegXA5ip`; its API also responds and has 10 blocks, but its main.ts was not read. The verbatim code below is from `_Ysw6uKC3eUwf`. Verify which link the wiki currently shows before publishing.
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.1"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.5"`, `"pxt-TPBot": "github:elecfreaks/pxt-tpbot#v1.1.1"`
- Blocks: 10
- Concepts: on start (show icon), forever, variable i, math map with a negative target range (0..-100)
- Ports: J1 (potentiometer), M1 and M4 (motors)
- screenshot_path: `P`1793439574374-tbuicp.jpg
- Wiki vs code: wiki says speed is adjusted by the potentiometer, correct. The map goes 0..-100 (negative speeds), so the car drives in the direction set by the motor wiring; the variable `i` is then used for both M1 and M4 (same sign on both motors). Students will see "-100" in the map block.

```ts
let i = 0
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    i = Math.map(PlanetX_Basic.trimpot(PlanetX_Basic.AnalogRJPin.J1), 0, 1023, 0, -100)
    neZha.setMotorSpeed(neZha.MotorList.M1, i)
    neZha.setMotorSpeed(neZha.MotorList.M4, i)
})
```

## Case 11: Line-tracking Car
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_11
- MakeCode: https://makecode.microbit.org/_Uy0eywFah0u1
- Extensions: `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.5"`, `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.1"`
- Blocks: 15
- Concepts: on start (show icon), forever, three separate if blocks (no else, no else-if chain), line-tracking sensor states
- Ports: J1 (line tracking sensor), M1, M4 (motors)
- screenshot_path: `P`1793439626545-tqaza1.jpg
- Wiki vs code: the wiki connection text (as extracted) names no ports; the code uses J1, M1 and M4. Result text: "drives along the black line". Tracking states: Tracking_State_1 (shown as left dot on / right off) turns with M4 -50, M1 0; State_2 the opposite; State_0 (both dots on, per the Greek-editor icon) drives straight at -20 on both. State 3 (neither) is not handled, so the motors keep their last speed.

```ts
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    if (PlanetX_Basic.trackingSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.TrackingStateType.Tracking_State_1)) {
        neZha.setMotorSpeed(neZha.MotorList.M4, -50)
        neZha.setMotorSpeed(neZha.MotorList.M1, 0)
    }
    if (PlanetX_Basic.trackingSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.TrackingStateType.Tracking_State_2)) {
        neZha.setMotorSpeed(neZha.MotorList.M4, 0)
        neZha.setMotorSpeed(neZha.MotorList.M1, -50)
    }
    if (PlanetX_Basic.trackingSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.TrackingStateType.Tracking_State_0)) {
        neZha.setMotorSpeed(neZha.MotorList.M1, -20)
        neZha.setMotorSpeed(neZha.MotorList.M4, -20)
    }
})
```

## Case 12: Obstacles Avoidance Car
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_12
- MakeCode: https://makecode.microbit.org/_MyUJpP6L9YPo
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.10.6"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.5"`, `"pxt-TPBot": "github:elecfreaks/pxt-tpbot#v1.1.1"`
- Blocks: 18
- Concepts: on start (show icon + start motors), forever, variable i, if (no else), comparison (>=, <=) with AND, pause (500 ms)
- Ports: J1 (sonar), M1, M4 (motors)
- screenshot_path: `P`1793439626545-dzcq12.jpg
- Wiki vs code: consistent with wiki (sonar J1, motors M1&M4). The car starts driving on start (M1 -40, M4 -40), and when 4 <= distance <= 20 cm it turns (M1 100, M4 -100) for 500 ms, then resumes M1 -40, M4 -40. No reverse step. Beyond 20 cm or under 4 cm it just keeps going.

```ts
let i = 0
basic.showIcon(IconNames.Diamond)
neZha.setMotorSpeed(neZha.MotorList.M1, -40)
neZha.setMotorSpeed(neZha.MotorList.M4, -40)
basic.forever(function () {
    i = PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm)
    if (i >= 4 && i <= 20) {
        neZha.setMotorSpeed(neZha.MotorList.M1, 100)
        neZha.setMotorSpeed(neZha.MotorList.M4, -100)
        basic.pause(500)
        neZha.setMotorSpeed(neZha.MotorList.M1, -40)
        neZha.setMotorSpeed(neZha.MotorList.M4, -40)
    }
})
```

## Case 17: Alarm Device
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_17
- MakeCode: https://makecode.microbit.org/_A4CaHvTuJ7br
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.4"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.8"`
- Blocks: 13
- Concepts: event (on button A pressed), forever, variable i as toggle (i = 1 - i), if-else on a variable, arithmetic, music (play tone 262 Hz), pause
- Ports: J1 (red LED)
- screenshot_path: `P`1793439626545-necbec.jpg
- Wiki vs code: consistent with the result text (A starts alarm, A again stops). Details: the alarm sound is `music.playTone(262, whole beat)` (middle C on the micro:bit speaker/pin), not a separate buzzer module. The if tests `i` alone (a number as condition), not a comparison. Because of the 500 ms pauses plus the whole-beat tone, stopping can lag up to about 1.5 s. The wiki lists bricks and mentions only PlanetX in step 1, but pxt.json also contains pxt-nezha (unused).

```ts
let i = 0
input.onButtonPressed(Button.A, function () {
    i = 1 - i
})
basic.forever(function () {
    if (i) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, true)
        music.playTone(262, music.beat(BeatFraction.Whole))
        basic.pause(500)
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, false)
        basic.pause(500)
    } else {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, false)
    }
})
```

## Case 27: The Distance Indicator
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_27
- MakeCode: https://makecode.microbit.org/_Vb69KzLR3Dhe
- Extensions: `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.2.0"` (only)
- Blocks: 3
- Concepts: forever, show number with the sonar value nested inside
- Ports: J1 (sonar)
- screenshot_path: `P`1793439626545-oyt1fg.jpg
- Wiki vs code: consistent. MISMATCH in dependencies: main.ts calls `PlanetX_Basic.ultrasoundSensor`, but pxt.json lists only pxt-nezha, no pxt-PlanetX (the editor still showed the PlanetX_Base category and the block rendered, so the PlanetX code arrives through the pxt-nezha package at v1.2.0). The wiki steps tell students to add PlanetX and nezha only if it applies; check which extensions students must add when starting from scratch. Project name "Untitled".

```ts
basic.forever(function () {
    basic.showNumber(PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm))
})
```

## Case 37: Traffic Lights
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_37
- MakeCode: https://makecode.microbit.org/_YdMCa7KhdVEf
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v0.13.1"`
- Blocks: 12
- Concepts: on start (show icon), forever, sequence of LED on/off with pause. No variables, no conditions.
- Ports: J1 (red), J2 (yellow), J3 (green)
- screenshot_path: `P`1793439626545-n6hjkt.jpg (on start and forever blocks overlap slightly, as authored)
- Wiki vs code: consistent (red 5 s, yellow 2 s, green 5 s). Note green is turned off at the start of each cycle and red on, so after yellow the cycle goes green then red.

```ts
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, true)
    PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, false)
    basic.pause(5000)
    PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, false)
    PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, true)
    basic.pause(2000)
    PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, false)
    PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, true)
    basic.pause(5000)
})
```

## Case 50: A Small Trash Can
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_50
- MakeCode: https://makecode.microbit.org/_VE00w0E5rLL6
- Extensions: `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.3.6"`
- Blocks: 8
- Concepts: two events (button A, button B), pause. No forever, no variables.
- Ports: M1 (motor)
- screenshot_path: `P`1793439679518-x7m6f9.jpg
- Wiki vs code: consistent (A opens, B closes). The lid opens by running M1 at +10 for 1000 ms and closes with -10 for 1000 ms; there is no end-stop sensor, so repeated presses of the same button drift the lid further. The wiki connection text (as extracted) gave no port; code uses M1. Project name "Untitled".

```ts
input.onButtonPressed(Button.A, function () {
    neZha.setMotorSpeed(neZha.MotorList.M1, 10)
    basic.pause(1000)
    neZha.stopMotor(neZha.MotorList.M1)
})
input.onButtonPressed(Button.B, function () {
    neZha.setMotorSpeed(neZha.MotorList.M1, -10)
    basic.pause(1000)
    neZha.stopMotor(neZha.MotorList.M1)
})
```

## Case 21: An Oscillating Fan
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_21
- MakeCode: https://makecode.microbit.org/_fLtdmb8EmHxR
- Extensions: `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.1.8"`
- Blocks: 27
- Concepts: on start (servo to 90), TWO forever loops running in parallel, variables i and j, if-else, three if blocks, button polling with "button A is pressed", toggle (1 - i), arithmetic, pause for debounce
- Ports: S1 (360 degree servo), M1 (motor)
- screenshot_path: `P`1793439679519-3ajive.jpg
- Wiki vs code: MISMATCH with the result text "turn on/off the fan by pressing button A/B". Actual behavior: A toggles the fan motor (M1 100 or 0). B toggles the oscillation of the servo (sweeps 0 to 180 degrees with 1 s pauses), and B only has an effect when the fan is on. Turning the fan off with A also resets j to 0, which stops the oscillation. B does not turn the fan off. Oscillation and fan control live in separate forever blocks (a concurrency example).

```ts
let j = 0
let i = 0
neZha.setServoAngel(neZha.ServoTypeList._360, neZha.ServoList.S1, 90)
basic.forever(function () {
    if (input.buttonIsPressed(Button.A)) {
        i = 1 - i
        basic.pause(200)
    }
    if (i) {
        neZha.setMotorSpeed(neZha.MotorList.M1, 100)
    } else {
        neZha.setMotorSpeed(neZha.MotorList.M1, 0)
        j = 0
    }
    if (input.buttonIsPressed(Button.B)) {
        j = 1 - j
        basic.pause(200)
    }
})
basic.forever(function () {
    if (j) {
        neZha.setServoAngel(neZha.ServoTypeList._360, neZha.ServoList.S1, 0)
        basic.pause(1000)
        neZha.setServoAngel(neZha.ServoTypeList._360, neZha.ServoList.S1, 180)
        basic.pause(1000)
    }
})
```

## Case 48: The Walking Robot
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_48
- MakeCode: https://makecode.microbit.org/_1ugd2o5xJDae
- Extensions: `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.3.6"`
- Blocks: 4
- Concepts: two events (button A, button B). No forever, no variables, no pause.
- Ports: M1 (motor)
- screenshot_path: `P`1793439679519-2zgddf.jpg
- Wiki vs code: consistent (A moves, B stops). Only one motor (M1) at 100 percent; the walking motion comes from the mechanical build, not the code.

```ts
input.onButtonPressed(Button.A, function () {
    neZha.setMotorSpeed(neZha.MotorList.M1, 100)
})
input.onButtonPressed(Button.B, function () {
    neZha.stopMotor(neZha.MotorList.M1)
})
```

## Case 54: Happy Seesaw
- Wiki: https://wiki.elecfreaks.com/en/microbit/building-blocks/nezha-inventors-kit/Nezha_Inventor_s_kit_for_microbit_case_54
- MakeCode: https://makecode.microbit.org/_2bfKgv7KbVVV
- Extensions: `"pxt-PlanetX": "github:elecfreaks/pxt-planetx#v1.3.3"`, `"pxt-nezha": "github:elecfreaks/pxt-nezha#v1.3.2"`
- Blocks: 14
- Concepts: forever, if (no else), comparison (<), show number (sensor value), pause, stop all motors
- Ports: J1 (sonar, read twice per loop), M1 (motor)
- screenshot_path: `P`1793439679519-y7073u.jpg
- Wiki vs code: wiki result: "when there is an obstruction in front of it, the objects will be pushed down". Code: shows the distance, then if distance < 20 cm the motor runs +10 for 200 ms, stops for 5 s, runs -10 for 200 ms, stops for 5 s. The sonar is read twice (once for display, once for the condition) and there is no variable. The `if` also fires when the reading is 0 (no echo). Project name in pxt.json is Chinese ("chao sheng bo qiao qiao ban" in characters), visible in the editor name box in the screenshot.

```ts
basic.forever(function () {
    basic.showNumber(PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm))
    if (PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm) < 20) {
        neZha.setMotorSpeed(neZha.MotorList.M1, 10)
        basic.pause(200)
        neZha.stopAllMotor()
        basic.pause(5000)
        neZha.setMotorSpeed(neZha.MotorList.M1, -10)
        basic.pause(200)
        neZha.stopAllMotor()
        basic.pause(5000)
    }
})
```

---

## Cross-cutting notes for the teacher guide
- The wiki's "Step 1" text asks students to add PlanetX (and sometimes nezha) but several projects declare other versions: PlanetX appears as v0.10.6, v0.12.0, v0.13.1, v0.13.4, v0.14.0, v1.3.3, v1.4.5; nezha as v1.1.5, v1.1.8, v1.2.0, v1.3.2, v1.3.6. The editor will pick the latest compatible version when students add the extension from scratch, so block names and shapes may differ slightly from these screenshots.
- No program in this set uses an else-if chain; cases that look like else-if (04, 09, 11) are separate sequential `if` blocks.
- No program uses radio or a "math map" other than cases 08 and 10.
- Cases 04, 06, 08, 10, 12 carry the unused TPBot extension in pxt.json.
- Wiki text for cases 11, 48, 50, 54 gave no port list in the extracted text (the wiring is in images only); ports above come from the code.
