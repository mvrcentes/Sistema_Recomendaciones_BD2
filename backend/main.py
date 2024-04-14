# main.py (actualización)

from crud import *
from nodes_relationships import *

def main():
    print("Bienvenido al sistema de recomendaciones de videojuegos!")
    
    # Iniciar sesión
    user_email = input("Por favor, introduzca su correo electrónico para iniciar sesión: ")
    user_node = graph.nodes.match("USUARIO", email=user_email).first()
    
    if user_node:
        print(f"Bienvenido de nuevo, {user_node['nombre']}!")
    else:
        print("Usuario no encontrado.")
        create_new_user = input("¿Desea crear un nuevo usuario? (yes/no): ")
        if create_new_user.lower() == "yes":
            create_user()
            print("Usuario creado exitosamente. Por favor, inicie sesión nuevamente.")
            main()
        else:
            print("Saliendo del sistema.")
            return
    
    # Menú principal
    while True:
        print("\nMenú principal:")
        print("1. Recomendar juegos")
        print("2. Buscar juegos por género")
        print("3. Jugar un juego")
        print("4. Escribir una reseña")
        print("5. Salir")
        
        choice = input("Por favor, seleccione una opción: ")
        
        if choice == "1":
            print("Recomendaciones basadas en sus preferencias:")
            print(recommend_games_for_user(user_node['id']))
        elif choice == "2":
            genre = input("Introduzca el género que desea buscar: ")
            games_by_genre = find_games_by_genre(genre)
            games_list = list(games_by_genre)

            if games_list:
                print("Recomendaciones basadas en el género seleccionado:\n")
                headers = ["Título", "Plataformas", "Fecha_de_Lanzamiento"]
                header_format = "{:<30} | {:<50} | {:<20}"

                print(header_format.format(*headers))
                print("-" * 30 + "|" + "-" * 50 + "|" + "-" * 20)

                for record in games_list:
                    titulo = record['Titulo'][:30].ljust(30)
                    plataformas = str(record['Plataformas'])[:50].ljust(50)
                    fecha = str(record['Fecha_de_Lanzamiento'])[:20].ljust(20)

                    print(f"{titulo} | {plataformas} | {fecha}")
            else:
                print(f"No se encontraron juegos para el género {genre}.")
        elif choice == "3":
            # Funcionalidad para jugar un juego
            pass
        elif choice == "4":
            review_properties = {
                "titulo": input("Introduzca el título de la reseña: "),
                "contenido": input("Escriba su reseña: "),
                "calificacion": int(input("Califique el juego (1-5): ")),
                "fecha": input("Introduzca la fecha de la reseña (YYYY-MM-DD): "),
                "util": input("¿Recomienda este juego? (True/False): ").lower() == "true"
            }
            review_node = create_review(review_properties)
            
            if review_node:
                user_reviewed_game(user_node['nombre'], review_properties["titulo"], review_properties["fecha"], review_properties["calificacion"], review_properties["util"])
                print("Reseña creada exitosamente y relación establecida.")
            else:
                print("Error al crear la reseña.")
            pass
        elif choice == "5":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()