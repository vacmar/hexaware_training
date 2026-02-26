from fastapi import FastAPI, Depends, Header, HTTPException, status

app = FastAPI()

def verify_token(x_api_key: str = Header()):
    if x_api_key != "secret123":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    
@app.get("/hello")
def hello(token:str = Depends(verify_token)):
    return {"message": "Hello, you are authorized!"}
