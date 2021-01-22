import numpy as np
import os

import textwrap
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import warnings


attribute_order = ['name', 'type', 'cost', 'rarity', 'text', 'power', 'toughness', 'loyalty', 'flavor_text']


def parse_card_str(card, raise_error, just_first=True):
    cards = card.split('end_of_card')
    if not just_first:
        raise NotImplementedError
    card = cards[0].strip()
    attributes = card.split('|')
    if not len(attributes)==len(attribute_order):
        if raise_error:
            raise ValueError('Got %d pipes, expected %d'%(len(attributes), len(attribute_order)))
        else:
            warnings.warn("This card failed to parse!")
            print(card)
            return card
    attributes = [a.strip () for a in attributes]
    card_dict = {a_k:a_v.replace(' line_break ', '\n') for a_k, a_v in zip(attribute_order, attributes)}
    return card_dict

"""Paramaters for making visualizations"""
# Width/height corresponds to the opposite b/c. Width = 1st axis, height=2nd axis
img_width = 88*4
img_height = 64*4
border_size = 36
color_to_mpl_color = {
    'white' : 'gold',
    'blue' : 'blue',
    'black' : 'black',
    'red': 'red',
    'green' : 'green',
    'artifact' : '#b6bbbe',
    'multi': '#cea84c',
    'land' : '#927a34',
    'colorless': '#bfd8f7'
}
mana_symbol_radius = 12
mana_symbol_spacing = 5
fontsize = 12
mana_symbol_color_mapper = {
    'W' : 'gold',
    'U' : 'blue',
    'B' : 'black',
    'R' : 'red',
    'G' : 'green',
}
# What's x and what's y  and what's width and what's height has thouroughly gotten to me :P
# It works.... dont' worry about it....
mana_symbol_height = img_width - border_size/2 - mana_symbol_spacing
base_mana_symbol_width = img_height - border_size/2 - mana_symbol_spacing
name_wrap_len = 15

type_box_pos_height = img_width*.65
type_box_size_height = img_width*.08
card_type_font_size = 10

card_text_height = img_width*.55
text_wrap_len = 35
card_text_font_size=10

pt_box_size_height = 25
pt_box_size_width = 60
pt_box_loc_height = 25
pt_box_loc_width = img_height*.68




def compute_color(card):
    if 'land' in card['type'].lower():
        card['color'] = 'land'
    if 'artifact' in card['type'].lower():
        card['artifact'] = True
    else:
        card['artifact'] = False
    
    seen = set()
    for c in ['W', 'U', 'B', 'R', 'G']:
        if c in card['cost']:
            seen.add(c)
    if len(seen) > 1:
        card['color'] = 'multi'
    elif len(seen)==0:
        card['color'] = 'colorless'
    else:
        color = list(seen)[0]
        mapper = {'W' : 'white', 'U' : 'blue', 'B' : 'black', 'R': 'red', 'G': 'green'}
        card['color'] = mapper[color]

    return card
    
def get_wrapped_and_len(text, wraplen):
    split = text.split('\n')
    wrapped = [textwrap.wrap(s, width=wraplen) for s in split]
    wrapped = sum(wrapped, [])
    length = len(wrapped)
    return '\n'.join(wrapped), length

def card_str_to_text_display(card):
    lines = card.split('|')
    lines_and_wrapped = [get_wrapped_and_len(a, text_wrap_len) for a in lines]
    n_lines = sum([n[1] for n in lines_and_wrapped])
    wrapped = '\n'.join([n[0].strip().replace(' line_break ', '\n') for n in lines_and_wrapped])
    return wrapped, n_lines

def show_card(card, savename=None):
    # Modifiying it is useful
    card = copy.deepcopy(card)
    fig = plt.figure()
    fig.set_size_inches(8.8,6.3)
    ax = plt.gca()
    ax.axis('off')
#     # Border 
    if isinstance(card, str):
        to_print = 'CARD PARSE FAILURE!! :(\n' + card
        wrapped, n_lines = card_str_to_text_display(to_print)
        failure = ax.annotate(wrapped, xy=(border_size-5, img_height*.55 - 2*(n_lines-1)), fontsize=card_text_font_size)
        border = patches.Rectangle((0,0), img_height, img_width, linewidth=border_size, 
                                edgecolor='pink', facecolor='none')
        ax.add_patch(border)
    else:
        card = compute_color(card)
        # if we have 3 numbers, going to write them all lol and do it in flavor text
        if all([not card[attr]=='None' for attr in ['power', 'toughness', 'loyalty']]):
            card['flavor_text'] += '\n(__NOTE__: Power/Toughness/Loyalty)'
        border = patches.Rectangle((0,0), img_height, img_width, linewidth=border_size, 
                                edgecolor=color_to_mpl_color[card['color']], facecolor='none')
        ax.add_patch(border)
        # Mana Symbols
        split_symbols = card['cost'].split('}')
        split_symbols = [s[1:] for s in split_symbols if len(s) > 0][::-1]
        base_offset = border_size + mana_symbol_spacing
        for i, s in enumerate(split_symbols):
            additional_offset = mana_symbol_spacing*i + 2*i*mana_symbol_radius
            x = base_mana_symbol_width-additional_offset
            y = mana_symbol_height
            circle = plt.Circle((x, y), radius=mana_symbol_radius, facecolor='white', edgecolor='black')
            ax.add_patch(circle)
            label = ax.annotate(s, xy=(x,y-5), fontsize=fontsize, ha='center')
            try:
                symbol_color = mana_symbol_color_mapper[s]
            except KeyError:
                symbol_color = '#bfd8f7'
            alpha = .5 if s in ['B', 'U'] else .75
            symbol_color_circle = plt.Circle((x, y), radius=mana_symbol_radius * .75, facecolor=symbol_color, alpha=alpha)
            ax.add_patch(symbol_color_circle)
            
        # Card name
        wrapped_name, n_lines = get_wrapped_and_len(card['name'], name_wrap_len)
        label = ax.annotate(wrapped_name, xy=(border_size-10, mana_symbol_height-8-1.3*fontsize*(n_lines-1),), fontsize=fontsize)
        
        # Card Type
        type_box = patches.Rectangle((10, type_box_pos_height), img_height-20, type_box_size_height, facecolor='none', edgecolor='black', linewidth=2)
        ax.add_patch(type_box)
        wrapped_type, n_lines = get_wrapped_and_len(card['type'], text_wrap_len)
        label = ax.annotate(wrapped_type, xy=(25, type_box_pos_height+15-card_type_font_size*(n_lines-1)), fontsize=card_type_font_size)
        
        # Card Text
        wrapped_text, n_lines = get_wrapped_and_len(card['text'], text_wrap_len)
        if not wrapped_text == 'None':
            text = ax.annotate(wrapped_text, xy=(25, card_text_height+15-1.1*card_text_font_size*(n_lines-1)), fontsize=card_text_font_size)
        
        # Flavor text divider and flavor text
        if not card['flavor_text']=='None':
            divider_height = card_text_height + 15 - card_text_font_size*(n_lines-1) - 20
            divider = ax.annotate('', xy=(img_height*.25, divider_height), xytext=(img_height*.75,divider_height), 
                                arrowprops=dict(arrowstyle='-', connectionstyle='arc3,rad=0.'))
            flavor_text_height = divider_height - 20
            wrapped_text, n_lines = get_wrapped_and_len(card['flavor_text'], text_wrap_len)
            flavor_text = ax.annotate(wrapped_text, xy=(25, flavor_text_height-card_text_font_size*(n_lines-1)), fontsize=card_text_font_size, style='italic')    

        
        # Power/toughness OR loyalty
        # Display the box if p/t is expected (type is creature/planeswalker) OR if we're given one of them
        # If we're given P/T & Loyalty... just print the lo
        if 'planeswalker' in card['type'].lower() or 'creature' in card['type'].lower() or \
            not all([card[attr]=='None' for attr in ['power', 'toughness', 'loyalty']]):
            
            pt_box = patches.Rectangle((pt_box_loc_width, pt_box_loc_height), pt_box_size_width, 
                                    pt_box_size_height, edgecolor='black', facecolor='none', linewidth=2)
            ax.add_patch(pt_box)
            nums_to_show = [card[attr] for attr in ['power', 'toughness', 'loyalty']]
            nums_to_show = [n for n in nums_to_show if not n=='None']
            str_to_show = '/'.join(nums_to_show)
            pt = ax.annotate(str_to_show, xy=(pt_box_loc_width+10, pt_box_loc_height+10),
                            fontsize=card_text_font_size+4)
        
    ax.set_xlim(0, img_height)
    ax.set_ylim(0, img_width)
    ax.set_aspect('equal')
    if savename is not None:
        plt.savefig(savename, bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
        plt.show()


def visualize_card(card, savename=None, raise_error=False):
    if isinstance(card, str):
        card = parse_card_str(card, raise_error=raise_error)
    show_card(card, savename)

def form_table(card_dict, output_name):
    save_dir = './%s/'%output_name
    os.makedirs(save_dir, exist_ok=True)
    img_dir = save_dir + 'images/'
    os.makedirs(img_dir, exist_ok=True)
    
    max_val = 0
    for key, card_list in card_dict.items():
        for i, card in enumerate(card_list):
            visualize_card(card, img_dir+'%s_%d.png'%(key, i))
            max_val = max(max_val, i)

    table = "<table> <tr>" + " ".join(["<th><h1>%s</h1></th>"%key for key, _ in card_dict.items()]) + "</tr>"
    for i in range(max_val):
        this_row = "<tr>"
        for key, _ in card_dict.items():
            target_path = img_dir + '%s_%d.png'%(key, i)
            point_path = './images/' + '%s_%d.png'%(key, i)
            if os.path.exists(target_path):
                this_row += "<td><img src=%s style=\"width:378px;height:528px;\"></td>"%point_path
            else:
                this_row += "<td></td>"
        this_row += "</tr>"
        table += this_row
        # break
    table += "</table>"
    output_name = os.path.join(output_name, '%s.html'%output_name.split('/')[-1])
    with open(output_name, 'w') as f:
        f.write(table)
    os.startfile('./' + output_name, 'open')




