// Μάθημα 4.3 – Αυτοκίνητο ακολουθίας γραμμής
// Πηγή: https://makecode.microbit.org/_Uy0eywFah0u1 (project της ELECFREAKS, όπως είναι)
// extensions: pxt-PlanetX=github:elecfreaks/pxt-planetx#v1.6.9, pxt-nezha=github:elecfreaks/pxt-nezha#v1.3.11
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    if (PlanetX_Basic.trackingSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.TrackingStateType.Tracking_State_1)) {
        neZha.setMotorSpeed(neZha.MotorList.M4, -50)
        neZha.setMotorSpeed(neZha.MotorList.M1, 0)
    }
    if (PlanetX_Basic.trackingSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.TrackingStateType.Tracking_State_2)) {
        neZha.setMotorSpeed(neZha.MotorList.M4, 0)
        neZha.setMotorSpeed(neZha.MotorList.M1, -50)
    }
    if (PlanetX_Basic.trackingSensor(PlanetX_Basic.DigitalRJPin.J1, PlanetX_Basic.TrackingStateType.Tracking_State_0)) {
        neZha.setMotorSpeed(neZha.MotorList.M1, -20)
        neZha.setMotorSpeed(neZha.MotorList.M4, -20)
    }
})
