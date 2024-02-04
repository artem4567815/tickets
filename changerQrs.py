from PIL import Image, ImageDraw, ImageFont

def filingTemplate(name, num, userName, userCorpus):
    im1 = Image.open(name)
    im2 = Image.open('static/images/template.png')
    im2.paste(im1, (508, 98))

    font = ImageFont.truetype("times.ttf", 20)
    draw_text = ImageDraw.Draw(im2)
    draw_text.text((165, 350), userName, (0, 0, 0), font=font)

    draw_text = ImageDraw.Draw(im2)
    draw_text.text((180, 373), userCorpus, (0, 0, 0), font=font)

    im2.save(f'qrs/{num}.png', quality=95)
    im1.close()
    im2.close()
