import argparse
import os
import json


"""Given an image and tilesets, create a map json file that can be used by the
game or put into a map editor tool."""


def main(level_path, tilesets, tile_size):
    # Since pygame takes a few seconds to import do so here so that argparser
    # will fail immediately if incorrect args are provided.
    from pygame import image
    level_img = image.load(level_path)

    # Calculate dimensions
    file_dims = level_img.get_size()
    file_dims = [file_dims[0] / int(tile_size[0]),
                 file_dims[1] / int(tile_size[1])]

    # Make sure that dimensions are valid
    for dim in file_dims:
        if not dim.is_integer():
            raise Exception(f'Dimension was not divisible by tilesize: {dim}')

    # Create tileset images and get tileset names
    tileset_names = {}
    tileset_images = []
    for tileset in tilesets:
        img = image.load(tileset)
        tileset_images.append(img)
        tileset_names[img] = os.path.basename(tileset)

    # Map array with tile info
    map_array = []

    # Loop over dimension first checking file 1 then file two
    for y in range(int(file_dims[1])):
        row = []
        for x in range(int(file_dims[0])):
            failed_to_find_match = True
            for tileset in tileset_images:
                response = find_match(level_img, (x, y), tile_size, tileset)
                if response is not False:
                    row.append(
                        {"tileBackground": {
                            "rowNum": response[1],
                            "columnNum": response[0],
                            "tileSetName": tileset_names[tileset]
                        }}
                    )
                    failed_to_find_match = False
                    break

            if failed_to_find_match:
                row.append({"tileBackground": None})

        map_array.append(row)

    # Get map name
    file_name = input("What should this map be called?: ")

    # Format json file
    json_dict = {"mapArray": map_array,
                 "mapInfo": {"rows": int(file_dims[1]),
                             "columns": int(file_dims[1]),
                             "width": tile_size[0],
                             "height": tile_size[1],
                             "name": file_name}}

    with open(f'{file_name}.json', "w") as outfile:
        json.dump(json_dict, outfile)


def find_match(level_img, tile, tile_size, tileset):
    tileset_dims = tileset.get_size()
    tileset_dims = [int(tileset_dims[0]) / int(tile_size[0]),
                    int(tileset_dims[1]) / int(tile_size[1])]

    # Now check each tile from tileset to see if it is a match
    for y in range(int(tileset_dims[1])):
        for x in range(int(tileset_dims[0])):
            response = check_match(level_img, tile, tileset, (x, y), tile_size)
            if response:
                print(f'{tile}, {(x, y)}')
                return (x, y)
    return False


def check_match(level_img, level_tile, tileset, tileset_tile, tile_size):
    for y in range(int(tile_size[1])):
        for x in range(int(tile_size[0])):
            y_loc = y + level_tile[1] * int(tile_size[1])
            x_loc = x + level_tile[0] * int(tile_size[0])

            tile_x_loc = x + tileset_tile[0] * int(tile_size[0])
            tile_y_loc = y + tileset_tile[1] * int(tile_size[1])

            level_pixel = level_img.get_at((x_loc, y_loc))
            tileset_pixel = tileset.get_at((tile_x_loc, tile_y_loc))

            if not level_pixel == tileset_pixel:
                return False
    return True


if __name__ == "__main__":
    # Get arguments
    arg_parser = \
        argparse.ArgumentParser(description="Create a json map file from png")
    arg_parser.add_argument("Level", metavar="Level", type=str)
    arg_parser.add_argument("Tilesets", metavar="Tilesets", type=str,
                            help="Paths to tilesets dileniated via ','")
    arg_parser.add_argument("TileSize", metavar="TileSize", type=str)
    args = arg_parser.parse_args()

    # Run main
    main(args.Level, args.Tilesets.split(','), args.TileSize.split(','))
