# Kopina
Kopina es un compresor de imágenes con eliminación de metadatos. "kopina" viene del nahuatl y signifca sacar o extraer una cosa de otra

## Que hace

- Comprime imágenes JPG, JPEG, PNG y WEBP.
- Elimina metadatos EXIF para privacidad.
- Permite decidir qué hacer con la orientación EXIF mediante argumentos de CLI:
    - keep: aplica visualmente la orientación antes de borrar EXIF.
    - strip: borra EXIF sin corregir orientación.

- Permite decidir que hacer con el nombre del archivo final:
	- keep: mantiene el nombre original del archivo
	- strip <X>: genera un nombre aleatorio alfanumerico en minusculas de longitud *X* con random.choice


## Que no hace
- Proteger fotos fotos contra reconocimiento ni identificación facial
- Proteger fotos contra el entrenamiento de modelos de IA
- Comprime el archivo original en formatos como .zip, .7z, rar, etc.

## Requisitos
El script usa la libería PIL de python, para instalarla podemos hacerlo con pip
```powershell
python -m pip install pillow
```


## Comandos basicos
```powershell
# Por defecto comprime la foto de entrada con una calidad del 70% y mantiene la orientación original
python Kopina.py --input "Foto.jpg" --output "Foto_comprimida.jpg"

# Comprime la foto de entrada con una calidad del 30% y elimina los datos de rotación
python Kopina.py --input "Foto.jpg" --output "Foto_comprimida.jpg" --quality 30 --orientation strip

# Comprime las fotos en las subcarpetas
python Kopina.py --input "Fotos de viaje" --recursive
```

## Mejoras y/o actualizaciones a futuro

- Interfaz gráfica
- Hacer ejecutable
- Perfiles de compresión según el tipo de imagen
- Reducir dimensiones de imágen