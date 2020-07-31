FROM python:3
LABEL vendor="UD-SV project"

COPY requirement.txt ./

RUN pip install --no-cache-dir -r requirement.txt

COPY ./compute_versiondata_from_py3dfiles.py ./compute_versiondata_from_py3dfiles.py

CMD [ "python", "compute_versiondata_from_py3dfiles.py"]