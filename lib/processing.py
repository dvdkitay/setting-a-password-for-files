import os
import uuid

class Processing():
    def __init__(self):
        pass
    
    def save_file(self, file):
        try:

            UPLOAD_FOLDER = '/root/setting-a-password-for-files/static/files'

            filename, file_extension = os.path.splitext(file.filename)
            filename = str(uuid.uuid4())[:12] + str(file_extension)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            path_to_the_picture = '/static/files/' + filename

        except Exception as e:
            return False
        
        return path_to_the_picture