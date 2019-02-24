FROM python:2.7-stretch
RUN apt-get update && apt-get install -y pandoc
WORKDIR /tmp
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN mv wkhtmltox/bin/wkhtmlto* /usr/bin/
RUN ln -nfs /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN pip install pyyaml panflute
WORKDIR /app
COPY . .
RUN PATH="/app/:${PATH}"
RUN mkdir -p /project
WORKDIR /project
