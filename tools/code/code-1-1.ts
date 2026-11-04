// Μάθημα 1.1 – Γνωριμία με το micro:bit
// Πηγή: γράφτηκε από τα βήματα του μαθήματος (tutorials «Flashing Heart» και «Smiley Buttons»). Θέλει δοκιμή σε micro:bit.
// extensions: -
basic.forever(function () {
    basic.showIcon(IconNames.Heart)
    basic.pause(500)
    basic.showIcon(IconNames.SmallHeart)
    basic.pause(500)
})
input.onButtonPressed(Button.A, function () {
    basic.showString("Γεια!")
})
