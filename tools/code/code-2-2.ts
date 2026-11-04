// Μάθημα 2.2 – Μίνι λάμπα με διακόπτη
// Πηγή: https://makecode.microbit.org/_fewiyT73u19K (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
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
