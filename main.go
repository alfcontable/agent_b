package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
)

type Request struct {
	Message string `json:"message"`
}

type Response struct {
	Reply string `json:"reply"`
}

func main() {

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Servidor OK - Nica-creator Chat Bot")
	})

	http.HandleFunc("/chat", func(w http.ResponseWriter, r *http.Request) {

		// CORS
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

		if r.Method == http.MethodOptions {
			return
		}

		if r.Method != http.MethodPost {
			http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
			return
		}

		var req Request

		err := json.NewDecoder(r.Body).Decode(&req)
		if err != nil {
			http.Error(w, "Error leyendo JSON", http.StatusBadRequest)
			return
		}

		res := Response{
			Reply: "Recibido: " + req.Message,
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Fatal(http.ListenAndServe(":"+port, nil))
}