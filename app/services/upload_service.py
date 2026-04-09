import os
from werkzeug.utils import secure_filename
from app.utils.file_handler import allowed_file

UPLOAD_FOLDER = "app/static/uploads"

def upload_image(file):
    if not allowed_file(file.filename):
        raise Exception("Invalid file type")
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER,filename)

    file.save(filepath)

    return f"/static/uploads/{filename}"