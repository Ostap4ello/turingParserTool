all: check run

check:
	if [ ! -f "bin/python3" ]; then \
		python3 -m venv . ; \
		bin/pip install -r requirements.txt ; \
	fi

run:
	bin/python3 project/main.py

clean:
	# fill with tmpremoval
