FROM python:3.7.9-stretch
WORKDIR /tmp
RUN apt-get update && apt-get install -y libssl1.0-dev=1.0.2u-1~deb9u3 fonts-liberation=1:1.07.4-2 fonts-crosextra-carlito=20130920-1 fonts-crosextra-caladea=20130214-1
RUN wget https://github.com/jgm/pandoc/releases/download/2.11.3.2/pandoc-2.11.3.2-1-amd64.deb && dpkg -i pandoc-2.11.3.2-1-amd64.deb
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN mv wkhtmltox/bin/wkhtmlto* /usr/bin/
RUN ln -nfs /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN pip install pyyaml==5.3.1 panflute==2.0.5 gitpython==3.1.12 requests==2.25.1
WORKDIR /app
COPY . .
RUN PATH="/app/:${PATH}"
RUN mkdir -p /project
WORKDIR /project