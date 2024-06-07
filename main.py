from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import stock_data  # Assuming `stock_data` is your router module

# Create a FastAPI instance
app = FastAPI(
    title="First Project",
    version="1.0",
)

# Define CORS origins (update with your frontend URL)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Add other methods as needed
    allow_headers=["*"],
)

# Include your router(s)
app.include_router(stock_data)

# Run the app if this script is executed directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
