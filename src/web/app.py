from flask import Flask
from config.settings import get_settings
from src.web.routes import main_bp
from src.orchestration.orchestrator import ConversationOrchestrator

settings = get_settings()

def create_app():
    app = Flask(__name__, 
                template_folder="templates",
                static_folder="static")
    
    app.config["SECRET_KEY"] = settings.FLASK_SECRET_KEY
    
    # Initialize Core Services
    # We attach the orchestrator to the app so routes can access it
    # Note: Orchestrator init is sync, but its methods are async
    app.orchestrator = ConversationOrchestrator()
    
    # Register Blueprints
    app.register_blueprint(main_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=settings.PORT, debug=settings.DEBUG)
