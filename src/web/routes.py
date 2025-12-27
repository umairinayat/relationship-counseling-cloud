import logging
import uuid
import markdown
from flask import Blueprint, render_template, request, jsonify, current_app

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    """Render the main chat interface."""
    # Generate a fresh session ID if not present (simplified for demo)
    return render_template('index.html')

@main_bp.route('/chat', methods=['POST'])
async def chat():
    """
    Handle chat messages.
    Expected JSON: {"message": "user text", "user_id": "uuid", "session_id": "uuid"}
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data['message']
        
        # Validate or Generate UUIDs
        try:
            user_id = uuid.UUID(data.get('user_id'))
        except (ValueError, TypeError):
            # For demo, if invalid UUID, generate one (in prod, require auth)
            user_id = uuid.uuid4()
            
        session_id = data.get('session_id', str(uuid.uuid4()))

        # Access Orchestrator from app context
        # Note: current_app is a proxy, but we attached orchestrator to the real app object
        orchestrator = current_app.orchestrator
        
        # Process Message (ASYNC)
        response_text = await orchestrator.process_message(
            user_id=user_id,
            message=user_message,
            session_id=session_id
        )
        
        # Convert Markdown to HTML for the frontend
        # allowed_tags can be strict for safety
        response_html = markdown.markdown(response_text)
        
        return jsonify({
            "response": response_html,
            "raw_response": response_text,
            "user_id": str(user_id),
            "session_id": session_id
        })

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({"error": "Internal Processing Error"}), 500
