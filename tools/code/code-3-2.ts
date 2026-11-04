// Μάθημα 3.2 – Ανεμιστήρας με ρυθμιστή
// Πηγή: https://makecode.microbit.org/_3LAMei8MzHij (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9, pxt-nezha=github:elecfreaks/pxt-nezha#v1.3.11
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
// διάταξη: κάθετα
basic.showIcon(IconNames.Diamond)
basic.forever(function () {
    neZha.setMotorSpeed(neZha.MotorList.M1, Math.map(PlanetX_Basic.trimpot(PlanetX_Basic.AnalogRJPin.J1), 0, 1023, 0, 100))
})
