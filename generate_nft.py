from PIL import Image, ImageDraw, ImageChops
import random
import colorsys


def random_color():
    h = random.random()
    s = 1
    v = 1
    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x*255) for x in float_rgb]
    return tuple(rgb)


def interpolate(start_color, end_color, factor: float):
    recip = 1-factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )


def generate(path: str):

    print("gernarting art!")
    target_size_pxl = 256
    scale_factor = 2
    image_size_pxl = target_size_pxl * scale_factor
    padding_pxl = 16*scale_factor
    start_color = random_color()
    end_color = random_color()
    image_background_color = (0, 0, 0)
    image = Image.new("RGB", size=(image_size_pxl, image_size_pxl),
                      color=(image_background_color))
    draw = ImageDraw.Draw(image)

    points = []

    # Generate the points
    for _ in range(10):
        random_point = (
            random.randint(padding_pxl, image_size_pxl-padding_pxl),
            random.randint(padding_pxl, image_size_pxl-padding_pxl)
        )
        points.append(random_point)

    # draw the boundary box
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    # center the image
    delta_x = min_x-(image_size_pxl-max_x)
    delta_y = min_y-(image_size_pxl-max_y)

    # Center the image
    for i, point in enumerate(points):
        points[i] = (point[0]-delta_x//2, point[1]-delta_y//2)

    # Draw the points
    thickness = 0
    n_points = len(points)-1
    for i, point in enumerate(points):

        # overlay image
        overlay_image = Image.new("RGB", size=(image_size_pxl, image_size_pxl),
                                  color=(image_background_color))
        overlay_draw = ImageDraw.Draw(overlay_image)
        p1 = point
        if i == len(points)-1:
            p2 = points[0]
        else:
            p2 = points[i+1]

        line_xy = (p1, p2)
        color_factor = i/n_points
        line_color = interpolate(start_color, end_color, color_factor)
        thickness += scale_factor
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((target_size_pxl, target_size_pxl),
                         resample=Image.ANTIALIAS)

    image.save(path)


if __name__ == "__main__":
    for i in range(15):
        generate(f"test_image{i}.png")
