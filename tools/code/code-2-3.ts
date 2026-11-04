// Μάθημα 2.3 – Έξυπνη λάμπα
// Πηγή: https://makecode.microbit.org/_haMDD2EftPLV (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
basic.forever(function () {
    if (input.lightLevel() < 10) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, true)
    } else {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J1, false)
    }
})
