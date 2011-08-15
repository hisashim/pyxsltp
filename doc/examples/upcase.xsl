<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:e="http://example.org/e">

  <xsl:template match="text()">
    <xsl:choose>
      <xsl:when test="function-available('e:upcase')">
        <xsl:copy-of select="e:upcase(string(.))"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="string(.)"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="@*|node()" name="default">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
      <xsl:apply-imports/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
