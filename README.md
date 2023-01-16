# keebd: A USB-OTG fake keyboard daemon

This is a very small daemon/client pair to make a raspberry pi pretend
to be a USB keyboard to a host computer plugged into the
USB-OTG-capable socket on the pi (which is the USB-micro socket with
the USB logo, not the power logo, on a pi zero or zero 2).

It converts text from the command line to keyboard scancodes, to
simulate keypresses that (we hope) result in that text being "typed"
at the far end.

It only supports a minimal character set at the moment.
`/[A-Za-z0-9\t-']/` is all that will make it through right now,
anything else is silently dropped.

I have tested this on a raspberry pi zero 2 running raspberry pi os
bullseye and nothing else. Other models may work, or may melt into a
glowing heap.  YMMV.

## Installation and usage

Run this on the raspberry pi:

```
$ echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
$ echo "dwc2" | sudo tee -a /etc/modules
$ echo "libcomposite" | sudo tee -a /etc/modules
$ sudo make install
$ sudo reboot
```

When the pi has rebooted, plug a USB cable between the USB-OTG socket
on the pi and a USB socket on the host PC.  Focus a text input area on
the host PC. A Word document would be fine.  Now, run this on the pi:

```
$ keebd-send-keys "My hovercraft is full of eels"
```

All being well, the phrase "My hovercraft is full of eels" will have
appeared in the text input on the PC, as though it had been typed.


## Services

On installation, `make install` will install two systemd services:
`keebd-enable-usb-gadget.service` and `keebd.service`.

### keebd-enable-usb-gadget.service

This creates the configuration for the USB device that the pi will
pretend to be.  See `/usr/local/bin/keebd-enable-usb-gadget` for the
configuration values it uses.

It is responsible for creating the device node which represents the
client end of the USB connection, and which will appear as
`/dev/hidg0` when it's worked.  This device node **must** be created
before the `keebd` daemon itself starts.

### keebd.service

This service runs the `keebd` daemon and keeps it running, restarting
it if it crashes.j

## Config

Both `keebd` and `keebd-send-keys` read the file `/etc/keebd.conf`.
This file is in TOML format, and defines two keys:

- `socket_path`: The filesystem location for the socket to send text
  to `keebd`.  Default is `/var/keebd/keebd.sock`.
- `hidg_device`: The device node provided by
  `keebd-enable-usb-gadget.service`.  Default is `/dev/hidg0`.

## Socket communications

If you don't want to use the `keebd-send-keys` command line tool, you
can open the socket at `/var/keebd/keebd.sock` and write directly to
it.  See `/usr/local/bin/keebd-send-keys` for example code that does
this.

## Contributing

Raise a PR or an issue, then contact the author if I don't get in
touch.

## Author

Alex Young <alex.young12@nhs.net>
