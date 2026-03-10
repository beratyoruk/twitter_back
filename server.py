from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse
import os
import uvicorn

app = FastAPI()

@app.get("/script.js")
def get_script():
    # Eklenti sürekli burayı dinleyip kodu alır ve execute eder
    if os.path.exists("current_script.js"):
        with open("current_script.js", "r", encoding="utf-8") as f:
            script_content = f.read()
        return PlainTextResponse(script_content)
    return PlainTextResponse("// Betik hazir degil")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090)
