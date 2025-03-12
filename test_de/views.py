from django.shortcuts import render
from django.http import HttpResponse

import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# Create your views here.

# def index(request):

#     context = {"message": "Hello dopey!"}

#     return render(request, "test_de/index.html", context)

def index(request):
    # --- Fractal Generation (Mandelbrot Set) ---
    # Set the image dimensions and iteration parameters
    width, height = 900, 600
    max_iter = 100

    # Create a grid of complex numbers (each point in the plane)
    # xmin = -2.0
    # xmax = 1.0
    # ymin = -1.0
    # ymax = 1.0
    xmin = 0.3
    xmax = 0.4
    ymin = 0.55
    ymax = 0.6
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    c = X + 1j * Y

    # Initialize the array for the fractal and the iteration variable
    z = np.zeros_like(c)
    fractal = np.full(c.shape, max_iter, dtype=int)

    # Compute the Mandelbrot set
    for i in range(max_iter):
        mask = np.less(np.abs(z), 2.0)
        z[mask] = z[mask] ** 2 + c[mask]
        # Update fractal values at positions where the escape happens in this iteration.
        fractal[mask & (np.abs(z) >= 2.0)] = i

    # --- Plotting the Fractal with Matplotlib ---
    plt.figure(figsize=(16,12))
    plt.imshow(fractal, cmap='hot', extent=[xmin, xmax, ymin, ymax], origin='lower')

    # plt.axis('off')  # Hide axes for a cleaner image
    # Turn on the grid with desired style.
    plt.grid(True, which='both', color='white', linestyle='--', linewidth=0.5)
    
    # Optionally, you can label the axes.
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.title('Mandelbrot Set with a Fine Grid')
    
    # Save the plot to a BytesIO buffer in PNG format.
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()  # Close the figure to free memory
    buf.seek(0)

    # Encode the image to base64 so it can be embedded directly in HTML.
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # Pass the encoded image to your template via the context.
    context = {'fractal_image': image_base64}

    return render(request, 'test_de/index.html', context)


def search(render):
    return HttpResponse("<h1>Search page</h1")

