<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
      <xsl:apply-imports/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="comment()|processing-instruction()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
      <xsl:apply-imports/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
