# Set up for microbit on linux systems

Important link to do something [fun](https://makecode.microbit.org/#editor).

## Set up folders

Make a new folder 
```bash
mkdir <folder_name>
cd <folder_name>
```

Clone the following repos:

```bash
git clone https://github.com/code-help-tutor/COMP2300-6300-ENGN2219-Computer-Organisation-and-Program-Execution.git
```

```bash
git clone https://github.com/cpmpercussion/comp2300-toolchain
```

## Vscode extensions

Download the following vscode extensions

```bash
COMP2300 Extension (anu-extensions.comp2300-extension)
QuAC Companion Extension (anu-extensions.quac-companion)
```

### Installing toolchain

On vscode's command palatte run the following command:

```
COMP2300: Install Toolchain
```

It will install the toolchain in a specific directory. Make sure you keep track of that directory.

Incase this doesn't work refer to the next section

### If vscode command fails

We'll try to install this manually. Navigate to your home directory and run the following command:

```bash
git clone https://github.com/cpmpercussion/comp2300-toolchain.git .comp2300
```

`cd` into this repository and run the following commands:

```bash
make toolchain-linux.zip
```

This will download the ARM GCC toolchain, OpenOCD, and DiscoServer for Linux. 
<!-- Extract and organize them in a linux folder. Zip the folder into `toolchain-linux.zip`. -->

Then run this command:

```bash
unzip toolchain-linux.zip -d ~/.comp2300/linux
```

Add the Toolchain to PATH: (we're using vim here, you can use any editor to edit `.bashrc`)

```bash
vim ~/.bashrc
```

Add this line:

```
export PATH="~/.comp2300/linux/arm-none-eabi/bin:$PATH"
```

Then finally run:

```bash
source ~/.bashrc
```

## Verify Installation

Run: `arm-none-eabi-as --version`

# Running programs

Install `openocd`, this will help us look at the register values in the microbit.

```bash
sudo apt install -y openocd
```

Note: depending on linux distro this command may vary.

Verify the installation:

```bash
openocd --version
```

Next we need to install `udev` which will help us recognize the USB device.

```bash
sudo apt install -y udev
```

Run the following commands:

```bash
sudo nano /etc/udev/rules.d/99-cmsis-dap.rules
```

Note: Here we are using nano to edit the file, you can use any other editor but make sure you have sudo privileges.

Paste exactly this:

```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="0d28", ATTR{idProduct}=="0204", MODE="0666"
```

OR

```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="0d28", ATTR{idProduct}=="0204", MODE="0666", TAG+="uaccess"
```

Save and exit.

Then reload the rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Confirm that linux sees the debugger

Run:

```bash
lsusb
```

You should see something like:

```
ARM CMSIS-DAP
```

## Start OpenOCD for micro:bit

Run:

```bash
openocd \
  -f interface/cmsis-dap.cfg \
  -f target/nrf52.cfg
```

If the above fails try:

```bash
sudo openocd -f interface/cmsis-dap.cfg -f target/nrf52.cfg
```

If this fails too then udev rules must be wrong.

Expected Output:

```bash
Info : CMSIS-DAP: SWD supported
Info : nrf52.cpu: hardware has 6 breakpoints, 4 watchpoints
Info : Listening on port 3333 for gdb connections
```

Leave this terminal open!

In another terminal do the following steps.

## Building the program

Navigate to the project directory.

Run this:

```bash
make clean
make
```

Now we should have a `program.elf`.

Start GDB (the debugger):

```bash
arm-none-eabi-gdb program.elf
```

Inside this run the following:

```bash
target extended-remote localhost:3333
monitor reset halt
load
```

## Commands:

Inspect registers

```bash
info registers
```

Inspect GPIO memory

```bash
x/16wx 0x50000000
```

Break at main

```bash
break main
continue
```

Step instruction-by-instruction

```bash
stepi
```

Watch PC and registers

```bash
display $pc
display $r0
```