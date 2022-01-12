import uvicorn

if __name__ == "__main__":
    uvicorn.run('misApps.huge-app:app', reload=True)