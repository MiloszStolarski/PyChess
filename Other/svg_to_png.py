import cairosvg


names = ['bishop_black',
         'bishop_white',
         'king_black',
         'king_white',
         'knight_black',
         'knight_white',
         'pawn_black',
         'pawn_white',
         'queen_black',
         'queen_white',
         'rook_black',
         'rook_white',
         ]



# Wymiary obrazu PNG wyjściowego
output_png_width = output_png_height = 110

for name in names:
    cairosvg.svg2png(url=f'images/images_svg/{name}.svg', write_to=f'images_{output_png_width}px/{name}.png', output_width=output_png_width, output_height=output_png_height)

print('DONE')
