package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type Request struct {
	Message string `json:"message"`
}

type Response struct {
	Reply string `json:"reply"`
}

func chatHandler(w http.ResponseWriter, r *http.Request) {
	enableCors(&w)

	if r.Method != "POST" {
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
		return
	}

	var req Request
	json.NewDecoder(r.Body).Decode(&req)

	// RESPUESTA (puedes cambiar esto por IA después)
	reply := "Hola 👋 soy el bot de NICA-CREATOR. Dijiste: " + req.Message

	res := Response{Reply: reply}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(res)
}

func enableCors(w *http.ResponseWriter) {
	(*w).Header().Set("Access-Control-Allow-Origin", "*")
	(*w).Header().Set("Access-Control-Allow-Headers", "Content-Type")
}

func main() {
	http.HandleFunc("/chat", chatHandler)

	log.Println("Servidor corriendo en puerto 8080")
	http.ListenAndServe(":8080", nil)
}
