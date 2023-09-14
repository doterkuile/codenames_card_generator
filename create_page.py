import xml.etree.ElementTree as ET
import copy
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
import cairo

def load_files(page_size):

    # Define the template SVG file and the list of names
    template_file = f"codenames_page_{page_size}.svg"
    names_file = "names.txt"
    # names_file = "names.txt"

    # Read the list of names from the file
    with open(names_file, "r") as names_file:
        names = names_file.readlines()
    names = [name.split('. ')[1].strip() for name in names]

    template_tree = ET.parse(template_file)
    return template_tree, names


def get_font_size(text_element):
    style_properties = text_element.get('style').split(';')

    for property in style_properties:
        if property.startswith("font-size:"):
            # Extract the font size value
            font_size_px = float(property.split(":")[1].split("px")[0].strip())
            font_size = font_size_px / 300 * 25.4
            return float(font_size_px)
    return None

def replace_text(svg_text, new_text):

    if svg_text[0].text == "REPLACE":
        svg_text[0].text = new_text
    else:
        svg_text[0][0].text = new_text
    
    
def replace_position(svg_text, new_x):
    # surface = cairosvg.surface.SVGSurface(io.BytesIO(), width=100, height=100)
    # cairosvg.surface()
    # context = cairosvg.Context(surface)
    # font_size = 20
    # font_name = "Verdana"

    # # # Set font properties
    # # context.set_font_size(font_size)
    # # context.select_font_face(font_family)
    # # c = canvas.Canvas("/dev/null", pagesize=letter)
    
    # # Set the font
    # # c.setFont(font_name, font_size)

    # # Measure the text width
    # text_width = c.stringWidth(text, font_name, font_size)
    # current_style = svg_text[0].get('style')
    is_bottom_text = False
    if svg_text.get('transform') != 'scale(-1)' :
        is_bottom_text = True
    transform = None
    if is_bottom_text:
        transform = svg_text.get('transform')


    # if 'text-anchor' in current_style:
        # svg_text[0].set('style', f"{current_style}text-anchor:middle;")
    svg_text[0].set("x", str(new_x))

    if not is_bottom_text:
        svg_text.set("x", str(new_x))

    if is_bottom_text:
        svg_text.set('transform', "matrix(0.26458333,0,0,0.26458333,-5.9905238,0)")
    return
    # svg_text[0].set("style", "text-anchor: middle;")
    # svg_text[]


def update_position(font_size, new_name, position_element, text_element):


    x_o = float(text_element[0].get("x"))

    surface = cairo.SVGSurface('undefined.svg', 1280, 200)
    cr = cairo.Context(surface)
    # cr.select_font_face('Verdana', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.select_font_face('Verdana', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    font_size = 2.27765
    t_x = 0
    s_x = 1

    is_bottom_text = False
    if text_element.get('transform') != 'scale(-1)' :
        is_bottom_text = True

    # if is_bottom_text:
    #     old_style =  text_element[0][0].get('style')
    #     if 'text-anchor' not in old_style:
    #         text_element[0][0].set('style', f"{old_style};text-anchor:middle;")

    # else:
    #     old_style =  text_element[0].get('style')
    #     if 'text-anchor' not in old_style:
    #         text_element[0].set('style', f"{old_style};text-anchor:middle;")


    if is_bottom_text:
        font_size = 12.1689
        s_x = 0.26458333
        t_x = 5.9905238


    cr.set_font_size(font_size)
    _, _, w_o, _, _, _ = cr.text_extents("REPLACE")
    _, _, w_n, _, _, _ = cr.text_extents(new_name)

    block_width = 15.443726
    if is_bottom_text:
        # block_width = 23.177862 / s_x * 2.1913725
        block_width = 23.177862 / s_x 

    if name == "HEEMSTEDE":
        print(name)
    while w_n > block_width * 0.9:
        font_size = font_size * 0.9
        cr.set_font_size(font_size)
        # _, _, w_o, _, _, _ = cr.text_extents("REPLACE")
        _, _, w_n, _, _, _ = cr.text_extents(new_name)
    

    if not is_bottom_text:
            old_style = text_element.get('style')
            text_element.set('style',f"{old_style};font-size:{font_size}px;")
            old_style = text_element[0].get('style')
            text_element[0].set('style',f"{old_style};font-size:{font_size}px;")
    else:
        text_element.set('style',f"font-size:{font_size}px;")
    # w_o = len("REPLACE")
    # w_n = len(new_name)
    # text_width = font_size * len(new_name)
    new_x = x_o + (w_o - w_n)  / 2 + t_x / s_x
    # new_x = x + (width - text_width) / 2
    return new_x


if __name__ == "__main__":

    page_size = 12

    base_template, names = load_files(page_size)
    template_tree = copy.deepcopy(base_template)
    root = template_tree.getroot()
    root = list(root)
    page_index = 1
    layer_1 = root[2]
    card_groups = list(layer_1.find(".//{http://www.w3.org/2000/svg}g").find(".//{http://www.w3.org/2000/svg}g"))
    i = 0


    # for text in root.iter("text"):
    #     print('test')
    name_iterator = iter(names)  # Create an iterator for names



    cards = []
    stop_iteration = False
    while not stop_iteration:
        for row in root[2].find(".//{http://www.w3.org/2000/svg}g"):
            if stop_iteration:
                break

            for card in row:
                try:
                    name = next(name_iterator).upper()
                except StopIteration as e:
                    stop_iteration = True
                    break

                for card_group in card[0]:
                    
                    if not card_group.find(".//{http://www.w3.org/2000/svg}text"):
                        continue

                    text_card_group = card_group.find(".//{http://www.w3.org/2000/svg}text")
                    replace_text(text_card_group, name.strip())
                    font_size = get_font_size(text_card_group) 

                    position_group = card_group.find(".//{http://www.w3.org/2000/svg}path") if card_group.find(".//{http://www.w3.org/2000/svg}path") else card_group.find(".//{http://www.w3.org/2000/svg}rect")
                    
                    new_x = update_position(font_size, name, position_group, text_card_group)
                    replace_position(text_card_group, new_x)

            
        destination_file = f"generated_templates{page_size}/page{page_index}.svg"
        template_tree.write(destination_file)
        # Save template
        page_index += 1
        reset_template=True
        template_tree = copy.deepcopy(base_template)
        root = list(template_tree.getroot())

            
    destination_file = f"generated_templates{page_size}/page{page_index}.svg"
    template_tree.write(destination_file)
    root = list(template_tree.getroot())

            



        


    pass