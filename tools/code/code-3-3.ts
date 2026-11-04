// Μάθημα 3.3 – Αυτόματη πόρτα
// Πηγή: https://makecode.microbit.org/_MssY8AXgCbkK (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9, pxt-nezha=github:elecfreaks/pxt-nezha#v1.3.11
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
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
