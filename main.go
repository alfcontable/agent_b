http.HandleFunc("/chat", func(w http.ResponseWriter, r *http.Request) {

    // CORS Headers
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
    w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

    // IMPORTANTE: El navegador necesita un 200 OK en el método OPTIONS
    if r.Method == http.MethodOptions {
        w.WriteHeader(http.StatusOK) // <--- AÑADE ESTA LÍNEA
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

    // Tu lógica de respuesta
    res := Response{
        Reply: "Nica Creator dice: " + req.Message,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(res)
})
