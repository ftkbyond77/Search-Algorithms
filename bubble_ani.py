import pyglet
from pyglet import shapes
from random import sample

# Function to perform bubble sort and generate animation frames
def bubble_sort_animation_frames(arr):
    frames = []
    n = len(arr)

    for i in range(n):
        for j in range(0, n-i-1):
            # Create a frame for the current state of the array
            frames.append(arr.copy())

            # If the element found is greater than the next element, swap them
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    # Create a frame for the final sorted state
    frames.append(arr.copy())

    return frames

# Create a window for the animation
window = pyglet.window.Window(width=1300, height=600)

# Set up an initial random array for sorting
array_to_sort = sample(range(1, 101), 60)

# Generate animation frames for bubble sort
animation_frames = bubble_sort_animation_frames(array_to_sort.copy())

# Set up the drawing
batch = pyglet.graphics.Batch()

# Colors
compared_color = (123, 104, 238)  # MediumSlateBlue
normal_color = (135, 206, 250)     # Sky Blue

@window.event
def on_draw():
    window.clear()

    # Draw the current state of the array
    for i, value in enumerate(array_to_sort):
        color = compared_color if animation_frames and animation_frames[0][i] == value else normal_color
        shapes.Rectangle(i * 20 + 50, 50, 10, value * 3, color=color, batch=batch).draw()

# Function to update the animation frames
def update(dt):
    global array_to_sort, animation_frames

    # If there are frames left in the animation, update the array
    if animation_frames:
        array_to_sort = animation_frames.pop(0)
    else:
        pyglet.app.exit()

# Schedule the update function
pyglet.clock.schedule_interval(update, 0.2)  # Reduced interval for faster animation

# Start the Pyglet event loop
pyglet.app.run()


