// Μάθημα 4.2 – Αυτοκίνητο που αποφεύγει εμπόδια
// Πηγή: γράφτηκε από τα βήματα του μαθήματος (το παλιό link _MyUJpP6L9YPo δεν υπάρχει πια)· δημοσιεύτηκε ως https://makecode.microbit.org/_FmXFRx0mjTyR (4/11/2026). Θέλει δοκιμή σε πραγματικό kit.
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9, pxt-nezha=github:elecfreaks/pxt-nezha#v1.3.11
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
let i = 0
basic.showIcon(IconNames.Diamond)
neZha.setMotorSpeed(neZha.MotorList.M1, -40)
neZha.setMotorSpeed(neZha.MotorList.M4, -40)
basic.forever(function () {
    i = PlanetX_Basic.ultrasoundSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.Distance_Unit_List.Distance_Unit_cm)
    if (i >= 4 && i <= 20) {
        neZha.setMotorSpeed(neZha.MotorList.M1, 100)
        neZha.setMotorSpeed(neZha.MotorList.M4, -100)
        basic.pause(500)
        neZha.setMotorSpeed(neZha.MotorList.M1, -40)
        neZha.setMotorSpeed(neZha.MotorList.M4, -40)
    }
})
