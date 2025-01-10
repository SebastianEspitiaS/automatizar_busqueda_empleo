from configuraciones.configuraciones_computrabajo import login, buscar_ofertas
from configuraciones.configuracion_driver import configurar_navegador
from paginas.computrabajo import realizar_proceso_computrabajo

def main():
    print("Bienvenido al programa de búsqueda de empleo")
    print("Los portales de empleo disponibles son: ")
    print("1. Computrabajo")
    print("2. Indeed")
    print("3. LinkedIn")
    print("4. Glassdoor")
    print("0. Salir")
    portal = input("Elige el portal de empleo que deseas utilizar: ")
    
    if portal == "1":
        try:
            driver = configurar_navegador()
            login(driver)
            buscar_ofertas(driver)
            realizar_proceso_computrabajo(driver)
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        finally:
            driver.quit()
    elif portal == "2":
        print("Por implementar")
    elif portal == "3":
        print("Por implementar")
    elif portal == "4":
        print("Por implementar")
    elif portal == "0":
        print("Gracias por usar el programa. Hasta luego.")
    else:
        print("Opción no válida. Inténtalo de nuevo.")
        main()

if __name__ == "__main__":
    main()
