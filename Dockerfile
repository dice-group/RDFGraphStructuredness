FROM python:3.8.2-alpine3.11

COPY setup.py .
COPY RDFGraphStructuredness.py .
COPY readme.MD .

RUN pip install .

ENTRYPOINT ["python", "-m", "RDFGraphStructuredness"]