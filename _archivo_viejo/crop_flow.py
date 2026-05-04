from PIL import Image

def crop_image(input_path, output_path, left, top, right, bottom):
    try:
        img = Image.open(input_path)
        cropped = img.crop((left, top, right, bottom))
        cropped.save(output_path, "PNG")
        print(f"Éxito: {output_path} guardado.")
    except Exception as e:
        print(f"Error procesando {input_path}: {e}")

# Post 23
crop_image(
    r"C:\Users\Awinda\.gemini\antigravity\brain\e5836229-fea2-4ef5-91c5-16ee4b71dfaa\runway_image_post_23_1776010953197.png",
    r"c:\Users\Awinda\MisProyectos\facebook_post_assistant\fb_images\post_23.png",
    64, 64, 64+440, 64+440
)

# Post 22
crop_image(
    r"C:\Users\Awinda\.gemini\antigravity\brain\e5836229-fea2-4ef5-91c5-16ee4b71dfaa\studio_image_post_22_1776010964825.png",
    r"c:\Users\Awinda\MisProyectos\facebook_post_assistant\fb_images\post_22.png",
    64, 130, 64+440, 130+440
)
