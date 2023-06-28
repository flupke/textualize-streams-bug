.PHONY: bug
bug:
	- pkill -f mix
	poetry run phoenix_gui

.PHONY: install
install:
	asdf plugin add python || true
	asdf plugin add elixir || true
	asdf plugin add erlang || true
	asdf install
	mix local.hex --force
	poetry install
