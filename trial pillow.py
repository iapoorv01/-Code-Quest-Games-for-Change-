from PIL import Image

# Load the image (replace 'your_image.png' with the path to your image)
image_path = 'pillowtrial.jpg'
image = Image.open(image_path)

# Set the number of frames and calculate the width of each frame
num_frames = 4  # Adjust this based on how many frames there are in your sequence
frame_width = image.width // num_frames  # Assuming frames are evenly spaced

# Loop through and crop each frame
for i in range(num_frames):
    left = i * frame_width
    right = (i + 1) * frame_width
    cropped_frame = image.crop((left, 0, right, image.height))

    # Save each frame
    cropped_frame.save(f'frame_{i + 1}.png')

print("Frames saved successfully!")