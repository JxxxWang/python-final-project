import re
f="presentation.slides.html"; s=open(f).read()
s=re.sub(r"width: 960,\s*height: 700,","width: 1400,\n height: 800,\n margin: 0.02,\n minScale: 0.1,\n maxScale: 2.0,",s)
css="""<style>
.reveal{font-size:32px}.reveal .slides section{text-align:left}
.reveal h1{font-size:2em}.reveal h2{font-size:1.4em;margin-bottom:.3em}
.reveal ul,.reveal p{font-size:.9em;margin:.35em 0}
.reveal table{font-size:.7em;margin:0}.reveal table td,.reveal table th{padding:4px 10px}
.reveal pre{font-size:.62em;width:100%;box-shadow:none;white-space:pre-wrap}
.reveal .dataframe,.reveal .jp-RenderedHTMLCommon table{font-size:.85em}
.reveal img{max-height:560px;width:auto;max-width:100%}
</style></head>"""
open(f,"w").write(s.replace("</head>",css,1))
