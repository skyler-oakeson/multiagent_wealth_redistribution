VENV = .venv

ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE = @$(VENV)\Scripts\activate
else
    VENV_ACTIVATE = @. $(VENV)/bin/activate
endif

init:
	python -m venv $(VENV)
	$(VENV_ACTIVATE) && pip install -r requirements.txt

test:
	$(VENV_ACTIVATE) && python -m pytest tests/

run: 
	$(VENV_ACTIVATE) && python src/main.py

lint:
	$(VENV_ACTIVATE) && python -m ruff check --fix $$(git ls-files '*.py')

check:
	$(VENV_ACTIVATE) && python -m pyright $$(git ls-files '*.py')

clean:
	rm -rf $(VENV)
