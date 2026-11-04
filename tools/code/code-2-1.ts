// Μάθημα 2.1 – Φανάρι
// Πηγή: https://makecode.microbit.org/_YdMCa7KhdVEf (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
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
