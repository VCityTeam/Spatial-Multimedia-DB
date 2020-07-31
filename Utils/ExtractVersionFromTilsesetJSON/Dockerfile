FROM python:3
LABEL vendor="UD-CPOV project"

COPY requirement.txt ./

RUN pip install --no-cache-dir -r requirement.txt

COPY ./compute_versiondata_from_py3dfiles.py ./compute_versiondata_from_py3dfiles.py

CMD [ "python", "compute_versiondata_from_py3dfiles.py"]
# docker run --mount src=`pwd`,target=/Output,type=bind -it test_python:latest