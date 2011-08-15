<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:h="http://www.w3.org/1999/xhtml"
  xmlns:e="http://example.org/e">

  <xsl:template match="*[name()='p']/text()">
    <xsl:call-template name="example-func">
      <xsl:with-param name="arg1" select="string(.)"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="example-func">
    <xsl:param name="arg1"/>
    <xsl:copy-of select="e:example-func($arg1)"/>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
      <xsl:apply-imports/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
