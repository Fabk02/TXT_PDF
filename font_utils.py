from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def register_fonts(font_toml):
    for font_family, styles in font_toml.items():
        for style, info in styles.items():
            pdfmetrics.registerFont(TTFont(info['name'], info['path']))
        if styles.get('italic') == None:
            if styles.get('bold') == None:
                if styles.get('boldItalic') == None:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'])
                else:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'], 
                                                boldItalic=styles['boldItalic']['name'])
            else:
                if styles.get('boldItalic') == None:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'], 
                                                bold=styles['bold']['name'])
                else:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'], 
                                                bold=styles['bold']['name'], 
                                                boldItalic=styles['boldItalic']['name'])
        else:
            if styles.get('bold') == None:
                if styles.get('boldItalic') == None:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'],
                                                italic=styles['italic']['name'])
                else:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'],
                                                italic=styles['italic']['name'], 
                                                boldItalic=styles['boldItalic']['name'])
            else:
                if styles.get('boldItalic') == None:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'], 
                                                italic=styles['italic']['name'],
                                                bold=styles['bold']['name'])
                else:
                    pdfmetrics.registerFontFamily(font_family, 
                                                normal=styles['default']['name'], 
                                                italic=styles['italic']['name'],
                                                bold=styles['bold']['name'], 
                                                boldItalic=styles['boldItalic']['name'])