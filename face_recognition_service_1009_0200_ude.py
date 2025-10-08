# 代码生成时间: 2025-10-09 02:00:23
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import face_recognition
import io
import PIL.Image
import numpy as np
import logging

log = logging.getLogger(__name__)

"""
A Pyramid view configuration for a simple face recognition service.
"""

# Define a function to handle the face recognition
@view_config(route_name='recognize_face', renderer='json')
def recognize_face(request):
    # Get the image from the request
    image_file = request.POST.get('image', None)
    if not image_file:
        return Response(json_body={'error': 'No image provided.'}, status=400)

    # Convert image file to an image object
    image = PIL.Image.open(image_file)
    image.verify()  # Verify that it's actually an image
    
    # Convert image to numpy array for face_recognition
    image_array = np.array(image)
    
    # Recognize faces using face_recognition library
    try:
        # Try to locate faces in the image
        face_locations = face_recognition.face_locations(image_array)
        if not face_locations:
            return Response(json_body={'error': 'No faces found in the image.'}, status=404)
        
        # Process each face and return their encodings
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        return Response(json_body={'face_encodings': face_encodings.tolist()}, status=200)
    except Exception as e:
        # Handle errors that occurred during face recognition
        log.error('Error during face recognition: %s', e)
        return Response(json_body={'error': 'An error occurred during face recognition.'}, status=500)

# Function to configure the Pyramid application
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # Add the view
        config.add_route('recognize_face', '/recognize_face')
        config.scan()

# For standalone testing
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(None, {})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()