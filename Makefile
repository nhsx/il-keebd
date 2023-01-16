.PHONY: test
test:
	python -m pytest test_*

.PHONY: install
install:
	cp keebd.conf /etc/keebd.conf
	cp ./keebd-enable-usb-gadget /usr/local/bin
	cp ./keebd-enable-usb-gadget.service /etc/systemd/system/
	cp ./keebd /usr/local/bin
	cp ./keebd.service /etc/systemd/system
	cp ./keebd-send-keys /usr/local/bin
	systemctl daemon-reload
	systemctl enable keebd-enable-usb-gadget.service
	systemctl enable keebd.service
