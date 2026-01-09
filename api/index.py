from app import app

# Vercel serverless handler - this is the correct way to handle Flask apps on Vercel
def handler(environ, start_response):
    return app(environ, start_response)

# For local testing
if __name__ == "__main__":
    app.run(debug=True)
