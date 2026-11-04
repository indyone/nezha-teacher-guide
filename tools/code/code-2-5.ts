// Μάθημα 2.5 – Ειδοποίηση ποτίσματος
// Πηγή: https://makecode.microbit.org/_gmtM095oj1cd (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
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
