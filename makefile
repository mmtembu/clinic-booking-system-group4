PYTHON = python3

test:
		${PYTHON} -m tests

run:
		${PYTHON} clinix-api-start.py

clean:
		rm -r __pycache__