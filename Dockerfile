FROM python:3.8

COPY setup.py .
COPY RDFGraphStructuredness.py .
COPY readme.MD .

RUN pip install .

ENTRYPOINT ["python", "-m", "RDFGraphStructuredness"]