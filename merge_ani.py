import pyglet
from pyglet import shapes
from random import sample

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def generate_frames(arr):
    frames = []
    merge_sort_frames(arr, 0, len(arr), frames)
    return frames

def merge_sort_frames(arr, start, end, frames):
    if end - start > 1:
        mid = (start + end) // 2
        merge_sort_frames(arr, start, mid, frames)
        merge_sort_frames(arr, mid, end, frames)

        merged_array = merge(arr[start:mid], arr[mid:end])
        frames.append((start, end, merged_array.copy()))

        for i in range(len(merged_array)):
            arr[start + i] = merged_array[i]

def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged

# Create a window for the animation
window = pyglet.window.Window(width=1300, height=600)

# Set up an initial random array for sorting
array_to_sort = sample(range(1, 101), 60)

# Generate animation frames for merge sort
animation_frames = generate_frames(array_to_sort.copy())

# Set up the drawing
batch = pyglet.graphics.Batch()

# Colors
normal_color = (128, 128, 128)    # Gray

# Define a range of violet colors
violet_range = [(148, 73, 255), (138, 43, 226), (128, 0, 196)]

@window.event
def on_draw():
    window.clear()

    # Draw the current state of the array
    for i, value in enumerate(array_to_sort):
        color = normal_color
        if animation_frames and animation_frames[0][0] <= i < animation_frames[0][1]:
            # Shade of violet based on position in the array
            progress = (i - animation_frames[0][0]) / (animation_frames[0][1] - animation_frames[0][0])
            color = tuple(int(c + progress * (v - c)) for c, v in zip(normal_color, violet_range[1]))
        shapes.Rectangle(i * 20 + 50, 50, 10, value * 3, color=color, batch=batch).draw()

# Function to update the animation frames
def update(dt):
    global array_to_sort, animation_frames

    # If there are frames left in the animation, update the array
    if animation_frames:
        start, end, merged_array = animation_frames.pop(0)
        array_to_sort[start:end] = merged_array
    else:
        pyglet.app.exit()

# Schedule the update function
pyglet.clock.schedule_interval(update, 0.5)  # Adjusted speed

# Start the Pyglet event loop
pyglet.app.run()