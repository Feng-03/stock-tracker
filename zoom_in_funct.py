import matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [0, 1, 0, 1])
ax.set_title("Scroll to Zoom")

base_scale = 1.2  # zoom factor

def zoom(event):
    # Only zoom if the mouse is over the axes
    if event.inaxes != ax:
        return
    
    # Zoom in
    if event.button == 'up':
        scale_factor = 1 / base_scale
    # Zoom out
    elif event.button == 'down':
        scale_factor = base_scale
    else:
        return

    # Current limits
    x_left, x_right = ax.get_xlim()
    y_bottom, y_top = ax.get_ylim()

    # Mouse position in data coords
    xdata = event.xdata
    ydata = event.ydata

    # Calculate new limits
    new_width = (x_right - x_left) * scale_factor
    new_height = (y_top - y_bottom) * scale_factor

    ax.set_xlim([
        xdata - (xdata - x_left) * scale_factor,
        xdata + (x_right - xdata) * scale_factor
    ])
    ax.set_ylim([
        ydata - (ydata - y_bottom) * scale_factor,
        ydata + (y_top - ydata) * scale_factor
    ])

    fig.canvas.draw_idle()

# Connect the scroll event
fig.canvas.mpl_connect('scroll_event', zoom)

plt.show()