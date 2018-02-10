from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from PIL import Image

#initial setup
depth = get_depth()
rgb = get_video()
height = len(depth[0])
width = len(depth[0][0])
my_list = []

print("---------------------------------------")

#read the data from the kinnect
for i in depth[0]:
    for k in i:
        my_list.append((int((float(k) / 2048.0)*255), int((float(k) / 2048.0)*255), int((float(k) / 2048.0)*255)))


#generates the image
img = Image.new('RGB', (width, height))
img.putdata(my_list)
img.save('image.png')
