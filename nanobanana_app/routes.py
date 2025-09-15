from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import current_user, login_required
from . import db
from .models import Image
from volcenginesdkarkruntime import Ark

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/generate', methods=['POST'])
@login_required
def generate():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=current_app.config['ARK_API_KEY'],
        )
        imagesResponse = client.images.generate(
            model="doubao-seedream-4-0-250828",
            prompt=prompt,
            size="1024x1024",
            response_format="url",
            watermark=False
        )
        
        image_url = imagesResponse.data[0].url

        new_image = Image(
            prompt=prompt,
            image_url=image_url,
            user_id=current_user.id
        )
        db.session.add(new_image)
        db.session.commit()

        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/gallery')
@login_required
def gallery():
    images = Image.query.filter_by(user_id=current_user.id).order_by(Image.created_at.desc()).all()
    return render_template('gallery.html', images=images)