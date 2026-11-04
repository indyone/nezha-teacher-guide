// Μάθημα 4.1 – Αυτοκίνητο με ρυθμιστή ταχύτητας
// Πηγή: γράφτηκε από τα βήματα του μαθήματος. Θέλει δοκιμή σε πραγματικό kit.
// Το εικονίδιο εκκίνησης δεν ορίζεται στο μάθημα· μπήκε καρδιά, όπως στα περισσότερα.
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9, pxt-nezha=github:elecfreaks/pxt-nezha#v1.3.11
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
// διάταξη: κάθετα
let i = 0
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    i = Math.map(PlanetX_Basic.trimpot(PlanetX_Basic.AnalogRJPin.J1), 0, 1023, 0, 100)
    neZha.setMotorSpeed(neZha.MotorList.M1, 0 - i)
    neZha.setMotorSpeed(neZha.MotorList.M4, 0 - i)
})
