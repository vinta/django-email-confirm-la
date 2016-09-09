.PHONY: build
build:
	docker build -t email_confirm_la .

.PHONY: test
test:
	docker run --rm=true -v `pwd`:/app email_confirm_la
