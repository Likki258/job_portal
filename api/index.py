from app import app

# Vercel serverless handler
def handler(request):
    return app(request.environ, lambda status, headers: {'status': status, 'headers': dict(headers)})

# For local testing
if __name__ == "__main__":
    app.run()
