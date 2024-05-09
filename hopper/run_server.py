
# Run the app locally, usually for development purposes

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(
            "fapi:app",
            reload=True,
        )
    except ImportError as e:
        print("Unable to run as uvicorn is not available.")
        print(e)
