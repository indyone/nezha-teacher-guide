// Μάθημα 1.2 – Μετρητής απόστασης
// Πηγή: https://makecode.microbit.org/_Vb69KzLR3Dhe (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
basic.forever(function () {
    basic.showNumber(PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm))
})
