import uvicorn

if __name__ == "__main__":
    uvicorn.run("application.api.main:app", reload=True, host="0.0.0.0", port=8000)
