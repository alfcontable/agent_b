package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"strings"
)

// Estructuras para JSON
type Request struct {
	Message string `json:"message"`
}

type Response struct {
	Reply string `json:"reply"`
}

func main() {
	// Ruta principal para verificar que el servidor vive
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Servidor NICA CREATOR - Activo"))
	})

	// Ruta del Chat
	http.HandleFunc("/chat", func(w http.ResponseWriter, r *http.Request) {
		// --- CONFIGURACIÓN DE CORS ---
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		if r.Method != http.MethodPost {
			http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
			return
		}

		// Decodificar el mensaje del usuario
		var req Request
		err := json.NewDecoder(r.Body).Decode(&req)
		if err != nil {
			http.Error(w, "Error leyendo JSON", http.StatusBadRequest)
			return
		}

		// --- LÓGICA DE NEGOCIO DEL BOT ---
		input := strings.ToLower(strings.TrimSpace(req.Message))
		var botReply string

		switch {
		case input == "hola" || input == "buenos dias" || input == "inicio":
			botReply = "¡Hola! Bienvenido a NICA CREATOR. Soy el asistente de negocio. ¿Qué estás buscando hoy?\n\n" +
				"1. Chat box\n" +
				"2. Sistemas para negocios (ERP/CONTANOR)\n" +
				"3. Diseño de página web"

		case input == "1":
			botReply = "Has seleccionado: Chat box. Puedo ayudarte a integrar un chat inteligente como este en tu sitio web para atender clientes 24/7."

		case input == "2":
			botReply = "Has seleccionado: Sistemas para negocios. Estamos desarrollando CONTANOR, un sistema contable y ERP ideal para el régimen de cuotas fijas en Nicaragua."

		case input == "3":
			botReply = "Has seleccionado: Diseño de página web. Creamos sitios profesionales, rápidos y optimizados para celulares para que tu negocio destaque."

		default:
			botReply = "Entendido. Para ver las opciones principales, escribe 'Hola'. Si necesitas algo específico sobre '" + req.Message + "', dime y te ayudo."
		}

		// Enviar respuesta
		res := Response{
			Reply: botReply,
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	// Configuración del puerto para Render
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Servidor corriendo en el puerto %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
