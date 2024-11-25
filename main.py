import xml.etree.ElementTree as ET
import toml
import re
from font_utils import register_fonts
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas


# Function to extract text, including those outside of tags
def extract_text_with_tags(element):
    parts = []
    parts_styles = []
    if element.text:
        parts.append(element.text.strip())
        parts_styles.append(element.tag)
    for subelement in element:
        parts.append(f"{subelement.text.strip()}")
        parts_styles.append(subelement.tag)
        if subelement.tail:
            parts.append(subelement.tail.strip())
            parts_styles.append(element.tag)
    return parts,parts_styles


def make_styles_settings_dicts(styles_toml):
    styles_dict = {}
    settings_dict = {}
    for style_name in styles_toml:
        styles_dict[style_name] = ParagraphStyle(**styles_toml[style_name]["style"]) 
        settings_dict[style_name] = styles_toml[style_name]["settings"]
    return styles_dict,settings_dict

def make_pdf(parts, parts_styles, styles_dict, settings_dict, regex_dict): 
    doc_struct = [] 
    for part,style in zip(parts,parts_styles):
        
        for regex in regex_dict['regex']:
            part = re.sub(regex['find'],regex['replace'], part, flags=re.DOTALL)

        if (settings_dict[style]["newParagraphOnEndline"]):
            splitted_part = part.split('\n')
        else:
            splitted_part = part.split('\n\n')

        if (settings_dict[style]["newPageBefore"]):
            if len(doc_struct) != 1:
                doc_struct.append(PageBreak())
        
        if (settings_dict[style]["blockSpaceBefore"]) != 0:
            doc_struct.append(Spacer(1,settings_dict[style]["blockSpaceBefore"]))
        
        for split in splitted_part:
            doc_struct.append(Paragraph(split, styles_dict[style]))

        if (settings_dict[style]["blockSpaceAfter"]) != 0:
            doc_struct.append(Spacer(1,settings_dict[style]["blockSpaceAfter"]))

        if (settings_dict[style]["newPageAfter"]):
            doc_struct.append(PageBreak())
    return doc_struct

def add_page_number(canvas, doc, doc_size):
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(doc_size[0]/2, (1/0.035)/2, str(page_num))

margin = 15*mm
pdf = SimpleDocTemplate(
    "2_output.pdf", 
    pagesize=A4,
    leftMargin=margin,
    rightMargin=margin,
    topMargin=margin,
    bottomMargin=margin
    )


#register fonts in order to use them with reportlab library
font_toml = toml.load("cfg/fonts.toml")
register_fonts(font_toml)

#split settings and styles in dictionaries
styles_toml = toml.load("cfg/styles.toml")
styles,settings = make_styles_settings_dicts(styles_toml)
#styles = make_styles_dict(styles_toml)
#settings = make_settings_dict(styles_toml)

regex_toml = toml.load("cfg/regex.toml")
# Sample input
file_path='files/around_the_world_in_80_days.xml'

#extract structure from xml source
tree = ET.parse(file_path) 
root = tree.getroot()

# Extract text with tags
result,result_styles = extract_text_with_tags(root)

pdf.build(make_pdf(result, result_styles, styles, settings, regex_toml),
          onFirstPage=lambda canvas, doc: add_page_number(canvas,doc,pdf.pagesize),
          onLaterPages=lambda canvas, doc: add_page_number(canvas,doc,pdf.pagesize))