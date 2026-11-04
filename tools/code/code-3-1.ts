// Μάθημα 3.1 – Κάδος που ανοίγει
// Πηγή: https://makecode.microbit.org/_VE00w0E5rLL6 (project της ELECFREAKS, όπως είναι)
// extensions: pxt-nezha=github:elecfreaks/pxt-nezha#v1.3.11
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
input.onButtonPressed(Button.A, function () {
    neZha.setMotorSpeed(neZha.MotorList.M1, 10)
    basic.pause(1000)
    neZha.stopMotor(neZha.MotorList.M1)
})
input.onButtonPressed(Button.B, function () {
    neZha.setMotorSpeed(neZha.MotorList.M1, -10)
    basic.pause(1000)
    neZha.stopMotor(neZha.MotorList.M1)
})
