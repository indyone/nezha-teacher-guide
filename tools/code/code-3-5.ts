// Μάθημα 3.5 – Ανιχνευτής εισβολέα
// Πηγή: γράφτηκε από τα βήματα του μαθήματος. Θέλει δοκιμή σε πραγματικό kit.
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
basic.forever(function () {
    if (PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm) < 20) {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, true)
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, false)
        music.startMelody(music.builtInMelody(Melodies.BaDing), MelodyOptions.Once)
    } else {
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J2, false)
        PlanetX_Display.ledBrightness(PlanetX_Display.DigitalRJPin.J3, true)
    }
    basic.pause(500)
})
