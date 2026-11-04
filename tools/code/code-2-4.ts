// Μάθημα 2.4 – Ανεμιστήρας θερμοκρασίας
// Πηγή: https://makecode.microbit.org/_Cii8drJYPar5 (project της ELECFREAKS, όπως είναι)
// extensions: pxt-nezha=github:elecfreaks/pxt-nezha#v1.3.11
// εκδόσεις extensions: οι τελευταίες (4/11/2026)
basic.showIcon(IconNames.Heart)
basic.forever(function () {
    if (input.temperature() >= 28) {
        neZha.setMotorSpeed(neZha.MotorList.M1, 100)
    } else {
        neZha.stopMotor(neZha.MotorList.M1)
    }
})
