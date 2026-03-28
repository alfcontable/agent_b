package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {

	// Ruta principal (evita el error 404)
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Servidor OK - Nica-creator Chat Bot")
	})

	// Endpoint de prueba para chat
	http.HandleFunc("/chat", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
			return
		}

		// Aquí puedes leer el mensaje del cliente
		message := r.FormValue("message")

		// Respuesta simple (luego aquí conectas IA o lógica)
		response := "Recibido: " + message

		fmt.Fprintln(w, response)
	})

	// Obtener el puerto que Render asigna
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // fallback local
	}

	fmt.Println("Servidor corriendo en puerto:", port)

	// Iniciar servidor
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Fatal("Error al iniciar servidor:", err)
	}
}