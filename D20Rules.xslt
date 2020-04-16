<?xml version="1.0" encoding="UTF-8"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<body style="">
<style>
li {
	list-style-type: none;
}

body {
	font-family:Arial;font-size:12pt;
	background-color:#ddcebc;
	margin:1% 5% 1% 5%
}

.box {
	min-height:265px;
	border:outset 3px;
	padding:18px;
  page-break-inside: avoid;  
  -webkit-column-break-inside: avoid;  
  break-inside: avoid;  
}
</style>
<div>
<xsl:if test="D20Rules/RulesElement[@type = 'Class']" >
<h1>Class Updates</h1>
</xsl:if>
<xsl:for-each select="D20Rules/RulesElement[@type = 'Class']" >
<xsl:sort select="@name"/>
  <h2><xsl:value-of select="@name" /></h2>
<ul>
<p><xsl:value-of select="Flavor" /></p>
  <xsl:for-each select="specific">
   <xsl:if test="@name != 'type'">
      <xsl:if test="not(starts-with(@name,'_'))">
		<xsl:if test=". != ''">
			<li> <span style="font-weight:bold"><xsl:value-of select="@name" /> : </span><xsl:value-of select="." /> </li> 
		</xsl:if>
	  </xsl:if>
	</xsl:if>
</xsl:for-each>
<xsl:copy-of select="text()[normalize-space()][1]"/>
</ul>
</xsl:for-each>

<xsl:if test="D20Rules/RulesElement[@type = 'Class Feature']" >
<h1>Class Feature Updates</h1>
</xsl:if>
<xsl:for-each select="D20Rules/RulesElement[@type = 'Class Feature']" >
<xsl:sort select="@name"/>
  <h2><xsl:value-of select="@name" /></h2>
<ul>
<p><xsl:value-of select="Flavor" /></p>
  <xsl:for-each select="specific">
   <xsl:if test="@name != 'type'">
      <xsl:if test="not(starts-with(@name,'_'))">
		<xsl:if test=". != ''">
			<li> <span style="font-weight:bold"><xsl:value-of select="@name" /> : </span><xsl:value-of select="." /> </li> 
		</xsl:if>
	  </xsl:if>
	</xsl:if>
</xsl:for-each>
<xsl:copy-of select="text()[normalize-space()][1]"/>
</ul>
</xsl:for-each>

<xsl:if test="D20Rules/RulesElement[@type = 'Paragon Path']" >
<h1>Paragon Paths</h1>
</xsl:if>
<xsl:for-each select="D20Rules/RulesElement[@type = 'Paragon Path']" >
<xsl:sort select="@name"/>
  <h2><xsl:value-of select="@name" /></h2>
<ul>
<p><xsl:value-of select="Flavor" /></p>
  <xsl:for-each select="specific"> 
   <xsl:if test="@name != 'type'">
      <xsl:if test="not(starts-with(@name,'_'))">
		 <xsl:if test=". != ''">
			<li> <span style="font-weight:bold"><xsl:value-of select="@name" /> : </span><xsl:value-of select="." /> </li> 
		</xsl:if>
	</xsl:if>
  </xsl:if>
</xsl:for-each>
<xsl:copy-of select="text()[normalize-space()][1]"/>
</ul>
</xsl:for-each>
</div>
<div>
<xsl:if test="D20Rules/RulesElement[@type = 'Ritual']" >
<h1>Martial Practices / Practical Arts</h1>
<div style="column-count:3;margin:18px">
<xsl:for-each select="D20Rules/RulesElement[@type = 'Ritual']" >
<xsl:sort select="@name"/>
	<a>
	 <xsl:attribute name="href">#<xsl:value-of select="@name"/></xsl:attribute><xsl:value-of select="@name" />
	</a>
	<br />
</xsl:for-each>
</div>
</xsl:if>
<div style="column-count:2">
<xsl:for-each select="D20Rules/RulesElement[@type = 'Ritual']" >
<xsl:sort select="@name"/>
<div class="box" >
<a><xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
	</a>
  <h2><xsl:value-of select="@name" /></h2>
<ul>
<p><xsl:value-of select="Flavor" /></p>
  
  <xsl:for-each select="specific">
  <xsl:if test="@name != 'type'"> 
       <xsl:if test="not(starts-with(@name,'_'))">
		 <xsl:if test=". != ''">
			<li> <span style="font-weight:bold"><xsl:value-of select="@name" /> : </span><xsl:value-of select="." /> </li> 
		</xsl:if>
	  </xsl:if>
	</xsl:if> 
</xsl:for-each>
<xsl:copy-of select="text()[normalize-space()][1]"/>
</ul>
</div>
</xsl:for-each>
</div>
<xsl:if test="D20Rules/RulesElement[@type = 'Feat']" >
<h1>Feats</h1>
</xsl:if>
<xsl:for-each select="D20Rules/RulesElement[@type = 'Feat']" >
<xsl:sort select="@name"/>
  <h2><xsl:value-of select="@name" /></h2>
  <p><xsl:value-of select="Flavor" /></p>
<ul>
  <xsl:for-each select="specific">
 <xsl:if test="@name != 'type'"> 
       <xsl:if test="not(starts-with(@name,'_'))">
		 <xsl:if test=". != ''">
			<li> <span style="font-weight:bold"><xsl:value-of select="@name" /> : </span><xsl:value-of select="." /> </li> 
		</xsl:if>
	  </xsl:if> 
  </xsl:if>
</xsl:for-each>
<xsl:copy-of select="text()[normalize-space()][1]"/>
</ul>
</xsl:for-each>
</div> 
<div >
<xsl:if test="D20Rules/RulesElement[@type = 'Weapon']" >
<h1>Focused Techniques</h1>
</xsl:if>
<xsl:for-each select="D20Rules/RulesElement[@type = 'Weapon']" >
<xsl:sort select="@name"/>
  <h2><xsl:value-of select="@name" /></h2>
  <p><xsl:value-of select="Flavor" /></p>
<ul>
  <xsl:for-each select="specific">
  <xsl:if test="@name != 'type'">
      <xsl:if test="not(starts-with(@name,'_'))"> 
		 <xsl:if test=". != ''">
			<li> <span style="font-weight:bold"><xsl:value-of select="@name" /> : </span><xsl:value-of select="." /> </li> 
		</xsl:if> 
	</xsl:if>
  </xsl:if>
</xsl:for-each>
 <xsl:copy-of select="text()[normalize-space()][1]"/>
</ul>
</xsl:for-each>
<xsl:if test="D20Rules/RulesElement[@type = 'Power']" >
<h1>Power</h1>
</xsl:if>
<xsl:for-each select="D20Rules/RulesElement[@type = 'Power']" >
<xsl:sort select="@name"/>
  <h2><xsl:value-of select="@name" /></h2>
  <p><xsl:value-of select="Flavor" /></p>
<ul>
  <xsl:for-each select="specific">
  <xsl:if test="@name != 'Class'"> 
     <xsl:if test="not(starts-with(@name,'_'))" >
		 <xsl:if test=". != ''">
			<li> <span style="font-weight:bold"><xsl:value-of select="@name" /> : </span><xsl:value-of select="." /> </li> 
		  </xsl:if>
	</xsl:if> 
	</xsl:if>  
</xsl:for-each>
 <xsl:copy-of select="text()[normalize-space()][1]"/>
</ul>
</xsl:for-each>
<xsl:if test="PartIndex/Part">
<h1>Part Files</h1>
</xsl:if>
<xsl:for-each select="PartIndex/Part" >
<h2><xsl:value-of select="Filename" /></h2>
</xsl:for-each>
</div>
</body>
</html>