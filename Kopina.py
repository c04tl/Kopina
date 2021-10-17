#Kopina significa extraer una cosa de otra
#!/usr/bin/python3
"""
Este programa depende de python3-pil
"""

from PIL import Image
import os, sys, random, string

def ayuda():
	#imprime la forma de utilizar la herramienta
	print ('\n[*] Para usar ejecuta:\n\t\t{} <archivos y/o carpetas>\n'.format(sys.argv[0]))

def copiar_pixeles(archivo_imagen, es_solo_imagen=False):
	imagen = Image.open(archivo_imagen)

	print("[*] Copiando pixeles...")
	#datos contine los valores de los pixeles (no imprimir)
	datos = list(imagen.getdata())

	imagen_sin_metadatos = Image.new(imagen.mode, imagen.size)
	imagen_sin_metadatos.putdata(datos)

	nombre_archivo = os.path.basename(archivo_imagen)
	nombre_archivo, extension = os.path.splitext(nombre_archivo)
	ruta = os.path.split(archivo_imagen)[0]
	nombre_archivo = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

	#para preservar calidad se puede agregar quality=95 al final, por dfecto guarda con calidad del 75%
	if es_solo_imagen:
		ruta = os.path.join(ruta,nombre_archivo+extension)
	else:
		dir_nuevo = os.path.join(ruta,"sin_metas")
		if not os.path.exists(dir_nuevo):
			try:
				os.makedirs(dir_nuevo)
				print("[!] Se creó el directorio exitosamente ;)")
			except OSError as e:
				print("[X] No se pudo crear el directorio :(")
		ruta = os.path.join(ruta,dir_nuevo,nombre_archivo+extension)
	
	imagen_sin_metadatos.save(ruta, quality=90)

	print("[*] Archivo final: %s\n" % ruta)

def directorio(ruta):
	for raiz,directorios,archivos in os.walk(ruta):
		for imagen in archivos:
			if imagen.endswith("png") or imagen.endswith("jpg") or imagen.endswith("jpeg") or imagen.endswith("PNG") or imagen.endswith("JPG") or imagen.endswith("JPEG"):
				copiar_pixeles(os.path.abspath(os.path.join(raiz,imagen)))
		

if __name__ == '__main__':
	#argumentos de linea de comandos
	argumentos=sys.argv[1:]

	if argumentos != []:
		if '-h' in argumentos:
			ayuda()
		else:
			for item in argumentos:
				if os.path.isfile(item) and (item.endswith("png") or item.endswith("jpg") or item.endswith("jpeg") or item.endswith("PNG") or item.endswith("JPG") or item.endswith("JPEG")):
					copiar_pixeles(item,True)
				elif os.path.exists(item):
					directorio(item)
		sys.exit(0)
	else:
		ayuda()