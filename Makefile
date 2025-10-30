VENV = .venv

ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE = $(VENV)\Scripts\activate
else
    VENV_ACTIVATE = . $(VENV)/bin/activate
endif

init:
	python -m venv $(VENV)
	$(VENV_ACTIVATE) && pip install -r requirements.txt

test:
	$(VENV_ACTIVATE) && python -m pytest tests/

clean:
	rm -rf $(VENV)
