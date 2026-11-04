// Μάθημα 3.4 – Συναγερμός
// Πηγή: https://makecode.microbit.org/_A4CaHvTuJ7br (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
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
