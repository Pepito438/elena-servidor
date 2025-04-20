
import requests

print("Tú:", end=" ")
while True:
    texto = input()
    print("Elena: Procesando:", texto)

    try:
        respuesta = requests.post(
            "http://127.0.0.1:8000/api/responder",
            json={"texto": texto}
        )
        if respuesta.status_code == 200:
            data = respuesta.json()
            print("🔍 Respuesta cruda:", data)
            print("Elena:", data["respuesta"])
        else:
            print("Elena: Error del servidor:", respuesta.status_code)
    except Exception as e:
        print("Elena: Error al comunicarse con el servidor:", e)

    print("Tú:", end=" ")
