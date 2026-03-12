.syntax unified
.cpu cortex-m4
.thumb

.global _start
.type main,%function

.equ P0, 0x50000000
.equ P1, 0x50000300

.equ DIRSET, 0x518
.equ OUTSET, 0x508
.equ OUTCLR, 0x50C
.equ IN, 0x510

/* rows */
.equ ROW1, (1<<21)
.equ ROW2, (1<<22)
.equ ROW3, (1<<15)
.equ ROW4, (1<<24)
.equ ROW5, (1<<19)

/* columns */
.equ COL1, (1<<28)
.equ COL2, (1<<11)
.equ COL3, (1<<31)
.equ COL5, (1<<30)
.equ COL4, (1<<5)

/* button A */
.equ BUTTONA, (1<<14)

_start:

/* configure rows + columns as output */
ldr r0, =P0
ldr r1, =(ROW1|ROW2|ROW3|ROW4|ROW5|COL1|COL2|COL3|COL5)
str r1,[r0,#DIRSET]

ldr r0, =P1
ldr r1, =COL4
str r1,[r0,#DIRSET]

main_loop:

/* read button state */
ldr r0, =P0
ldr r1, [r0,#IN]

/* check if button pressed (active LOW) */
tst r1, #BUTTONA
bne leds_off

/* button pressed → run scan */
bl scan_once
b main_loop


leds_off:
/* ensure LEDs are off */
ldr r0, =P0
ldr r1, =(ROW1|ROW2|ROW3|ROW4|ROW5)
str r1,[r0,#OUTCLR]

ldr r1, =(COL1|COL2|COL3|COL5)
str r1,[r0,#OUTSET]

ldr r0, =P1
ldr r1, =COL4
str r1,[r0,#OUTSET]

b main_loop


scan_once:

ldr r4, =row_table
ldr r5, =col_table
mov r6, #5

scan_loop:

/* clear rows */
ldr r0, =P0
ldr r1, =(ROW1|ROW2|ROW3|ROW4|ROW5)
str r1,[r0,#OUTCLR]

/* clear columns */
ldr r1, =(COL1|COL2|COL3|COL5)
str r1,[r0,#OUTSET]

ldr r0, =P1
ldr r1, =COL4
str r1,[r0,#OUTSET]

/* activate row */
ldr r0, =P0
ldr r1, [r4],#4
str r1,[r0,#OUTSET]

/* activate columns */
ldr r2, [r5],#4

ldr r1, =(COL1|COL2|COL3|COL5)
and r3, r2, r1
str r3,[r0,#OUTCLR]

ldr r0, =P1
and r3, r2, #COL4
str r3,[r0,#OUTCLR]

bl delay

subs r6,#1
bne scan_loop

bx lr


delay:
mov r2,#2000
d1:
subs r2,#1
bne d1
bx lr


.data

row_table:
.word ROW1
.word ROW2
.word ROW3
.word ROW4
.word ROW5

col_table:
.word COL1|COL2|COL3|COL4|COL5
.word COL1|COL5
.word COL1|COL5
.word COL1|COL5
.word COL1|COL2|COL3|COL4|COL5