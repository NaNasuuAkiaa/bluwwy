from PIL import Image
import sys
import numpy as np

def gaussian_kernel(size, sigma=1.0):
    ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sigma))
    kernel = np.outer(gauss, gauss)
    return kernel / kernel.sum()

kernels_sigma = {3: 0.8, 5: 1.1, 7: 1.4, 9: 1.7}

def argerror():
    print("Usage: py bluwwy.py <image.png> <size (3,5,7,9)> <output.png>")
    sys.exit(1)

def getcolor(x, y, img_array, kernel, size):
    radio = size // 2
    alto, ancho, _ = img_array.shape
    
    # clamping
    y_min, y_max = max(0, y - radio), min(alto, y + radio + 1)
    x_min, x_max = max(0, x - radio), min(ancho, x + radio + 1)
    
    neighboring = img_array[y_min:y_max, x_min:x_max]
    
    # bordes
    k_y_min = radio - (y - y_min)
    k_y_max = k_y_min + (y_max - y_min)
    k_x_min = radio - (x - x_min)
    k_x_max = k_x_min + (x_max - x_min)
    
    sub_kernel = kernel[k_y_min:k_y_max, k_x_min:k_x_max]
    
    # normalizar kernel
    suma_kernel = np.sum(sub_kernel)
    kernel_normalizado = sub_kernel / suma_kernel
    
    # aplicar kernel a los 4 canales (RGBA)
    resultado = np.sum(neighboring * kernel_normalizado[:, :, np.newaxis], axis=(0, 1))
    
    return tuple(np.round(resultado).astype(int))

def main():
    if len(sys.argv) != 4:
        argerror()

    input_file = sys.argv[1]
    try:
        kernel_size = int(sys.argv[2])
    except ValueError:
        argerror()
        
    output_file = sys.argv[3]

    if kernel_size not in [3, 5, 7, 9]:
        argerror()
        
    # Cargar como RGBA para conservar transparencia
    imagen = Image.open(input_file).convert("RGBA")
    ancho, alto = imagen.size
    img_array = np.array(imagen, dtype=float) 
    
    # Generamos el kernel
    sigma = kernels_sigma[kernel_size]
    kernel = gaussian_kernel(kernel_size, sigma)
    
    # Crear imagen de salida RGBA
    output_img = Image.new("RGBA", (ancho, alto))
    pixels_output = output_img.load()

    print(f"Procesando imagen de {ancho}x{alto} con kernel {kernel_size}...")

    for x in range(ancho):
        for y in range(alto):
            pixels_output[x, y] = getcolor(x, y, img_array, kernel, kernel_size)

    output_img.save(output_file)
    print(f"¡Listo! Imagen guardada en {output_file}")

if __name__ == "__main__":    
    main()
