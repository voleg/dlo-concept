IMAGE_NAME							= heljetech_dlo
VERSION 								?= latest


clean:
	@echo cleaning work directory
	@rm -rf .*_cache
	@find . -name '*~' -print -exec rm -rf {} \;
	@find . -name '__pycache__' -print -exec rm -rf {} \;

build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

check:
	@echo run code checks and fixes in feature branch
	@(uv run ruff check . --fix) || true

test:
	uv run pytest

run:
	docker run -p 8000:8000 $(IMAGE_NAME):$(VERSION)
