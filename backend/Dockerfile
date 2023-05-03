FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5000

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]
