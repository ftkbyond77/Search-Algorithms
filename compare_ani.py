import pyglet
import random
import time

# Create a window, adjust size if needed to better accommodate the layout
window = pyglet.window.Window(width=1000, height=800, caption='Search Algorithms Comparison')
batch = pyglet.graphics.Batch()

def reset_searches():
    global numbers, linear_index, linear_found, binary_left, binary_right, binary_mid, binary_found
    # Generate a list with random numbers and include 42, then sort it for binary search
    numbers = random.sample(range(1, 100), 31) + [42]
    random.shuffle(numbers)  # Shuffle for linear search
    numbers.sort()  # Sort for binary search

    # Reset search variables
    linear_index = 0
    linear_found = False
    binary_left, binary_right = 0, len(numbers) - 1
    binary_mid = (binary_left + binary_right) // 2
    binary_found = False

    # Reset time tracking variables
    global start_time
    start_time = time.time()

reset_searches()  # Initialize searches

def update_searches(dt):
    global linear_index, linear_found, binary_left, binary_right, binary_mid, binary_found, start_time

    # Update linear search
    if not linear_found and linear_index < len(numbers):
        if numbers[linear_index] == 42:
            linear_found = True
            pyglet.clock.unschedule(update_searches)  # Stop updating searches when linear_found is True
        linear_index += 1  # Increment linear_index

    # Update binary search
    if not binary_found and binary_left <= binary_right:
        binary_mid = (binary_left + binary_right) // 2
        if numbers[binary_mid] == 42:
            binary_found = True
        elif numbers[binary_mid] < 42:
            binary_left = binary_mid + 1
        else:
            binary_right = binary_mid - 1

    # Calculate and display time used if either search is finished
    if linear_found or binary_found:
        time_used = round(time.time() - start_time, 2)
        print("Time used:", time_used)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.R:
        reset_searches()

pyglet.clock.schedule_interval(update_searches, 0.5)

@window.event
def on_draw():
    window.clear()
    margin = 5  # Margin between boxes
    box_size = (window.width - margin * (len(numbers) + 1)) // len(numbers)  # Calculate box size based on window width and margin
    topic_label = pyglet.text.Label("Find the target: 42", x=window.width // 2, y=window.height - 50,
                                     anchor_x='center', anchor_y='center', font_size=24, color=(255, 255, 255, 255))
    topic_label.draw()
    
    for i, number in enumerate(numbers):
        x = i * (box_size + margin) + margin  # Calculate x position with margin
        
        # Linear search boxes (top half)
        y_linear = window.height * 3/4 - box_size / 2
        color_linear = (240, 230, 140) if linear_found and i == linear_index - 1 else (238, 130, 238) if i == linear_index else (200, 200, 200)
        pyglet.shapes.Rectangle(x, y_linear, box_size, box_size, color=color_linear, batch=batch).draw()

        # Binary search boxes (bottom half)
        y_binary = window.height / 4 - box_size / 2
        color_binary = (240, 230, 140) if binary_found and i == binary_mid else (238, 130, 238) if binary_left <= i <= binary_right else (200, 200, 200)
        pyglet.shapes.Rectangle(x, y_binary, box_size, box_size, color=color_binary, batch=batch).draw()

        # Draw the number inside each box for both searches, adjust font size for readability
        label = pyglet.text.Label(str(number), x=x + box_size/2, y=y_linear + box_size/2, anchor_x='center', anchor_y='center', color=(255, 0, 0, 255), batch=batch)
        label.draw()
        label = pyglet.text.Label(str(number), x=x + box_size/2, y=y_binary + box_size/2, anchor_x='center', anchor_y='center', color=(255, 0, 0, 255), batch=batch)
        label.draw()

    # Display time used instead of "Get it!"
    if linear_found or binary_found:
        get_it_label = pyglet.text.Label("Binary Search has done!", x=window.width // 2, y=window.height // 2,
                                            anchor_x='center', anchor_y='center', font_size=26, color=(0, 255, 0, 255))
        get_it_label.draw()

pyglet.app.run()