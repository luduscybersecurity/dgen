FROM python:2.7-stretch
WORKDIR /tmp
RUN apt-get update && apt-get install -y libssl1.0-dev
RUN wget https://github.com/jgm/pandoc/releases/download/2.7/pandoc-2.7-1-amd64.deb && dpkg -i pandoc-2.7-1-amd64.deb
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN mv wkhtmltox/bin/wkhtmlto* /usr/bin/
RUN ln -nfs /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN pip install pyyaml panflute gitpython requests
WORKDIR /app
COPY . .
RUN PATH="/app/:${PATH}"
RUN mkdir -p /project
WORKDIR /project