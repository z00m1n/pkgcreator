<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:d="http://docbook.org/ns/docbook"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version="1.0">

<xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/xhtml/onechunk.xsl"/>
<xsl:param name="use.id.as.filename" select="'1'"/>
<xsl:param name="admon.graphics" select="'1'"/>
<xsl:param name="admon.graphics.path"></xsl:param>
<xsl:param name="html.stylesheet" select="'style.css'"/>
  
<!--<xsl:template match="d:section">
  <xsl:variable name="depth" select="count(ancestor::d:section)+1"/>
  <xsl:call-template name="id.warning"/>
  <section>
    <hgroup>
    <xsl:call-template name="section.titlepage"/>
    </hgroup>
    <xsl:variable name="toc.params">
      <xsl:call-template name="find.path.params">
        <xsl:with-param name="table" select="normalize-space($generate.toc)"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="contains($toc.params, 'toc') and $depth &lt;= $generate.section.toc.level">
      <xsl:call-template name="section.toc">
        <xsl:with-param name="toc.title.p" select="contains($toc.params, 'title')"/>
      </xsl:call-template>
      <xsl:call-template name="section.toc.separator"/>
    </xsl:if>
    <xsl:apply-templates/>
    <xsl:call-template name="process.chunk.footnotes"/>
  </section>
</xsl:template>-->
  
<xsl:template match="d:screenshot">
  <xsl:apply-imports/>
  <div class="caption"><xsl:apply-templates select="./d:info/d:title/node()"/></div>
</xsl:template>

</xsl:stylesheet>
