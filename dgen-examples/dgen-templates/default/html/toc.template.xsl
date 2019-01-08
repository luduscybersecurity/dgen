<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:outline="http://wkhtmltopdf.org/outline"
                xmlns="http://www.w3.org/1999/xhtml">
    <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
              doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
              indent="yes" />
    <xsl:template match="outline:outline">
        <html>
            <head>
                <title>Table of Contents</title>
                <link rel="stylesheet" href="file://%{html_dir}/css/template.css"/>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            </head>
            <body  class="margin">
                <h1>Table of Contents</h1>
                <ul style="list-style: none;-webkit-padding-start: 20px;"><xsl:apply-templates select="outline:item/outline:item"/></ul>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="outline:item">
        <li>
            <xsl:if test="@title!=''">
                <xsl:if test="count(ancestor::*) &lt; 3">
                    <div style="float:left;clear:both;height:1.3em;padding:1px 0.5em;background:#fff">
                        <xsl:if test="@link">
                        <xsl:attribute name="href"><xsl:value-of select="@link"/></xsl:attribute>
                        </xsl:if>
                        <xsl:if test="@backLink">
                        <xsl:attribute name="name"><xsl:value-of select="@backLink"/></xsl:attribute>
                        </xsl:if>
                        <xsl:value-of select="@title" /> 
                    </div>
                    <div style="float:right;height:1.3em;padding:1px 0.5em;background:#fff">
                        <span> <xsl:value-of select="@page" /> </span>
                    </div>
                    <div style="border-bottom: 1px dotted grey;margin-bottom:2px;height:1.3em;">
                    </div>
                </xsl:if>
            </xsl:if>
            <ul style="list-style:none;-webkit-padding-start: 20px;">
                <xsl:comment>added to prevent self-closing tags in QtXmlPatterns</xsl:comment>
                <xsl:apply-templates select="outline:item"/>
            </ul>
        </li>
    </xsl:template>
</xsl:stylesheet>
