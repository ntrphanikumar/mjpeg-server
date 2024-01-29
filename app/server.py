import time
import traceback

from sanic import response, Sanic
import asyncio
import requests

frame_absolute_path = 'publicly accessible image url'

app = Sanic(__name__)

def package_mjpeg(img_bytes):
    return (b'--frame\r\n'
            b'Content-Type: image/jpg\r\n\r\n' + img_bytes + b'\r\n')

# @app.route('/')
@app.route('/<path:path>')  # catchall
async def mjpeg_server(request, path=''):
    async def stream_mjpeg(response):
        while True:
            await asyncio.sleep(1)
            try:
                image_bytes: bytes = requests.get(frame_absolute_path).content
                await response.send(package_mjpeg(image_bytes))
                print(time.time())
            except Exception as e:
                print(repr(e))
            
    response = await request.respond(content_type='multipart/x-mixed-replace; boundary=frame')
    await stream_mjpeg(response)


if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt, exiting")
    except Exception as e:
        print(traceback.format_exc())
        print(f'EXCEPTION in get_instance_info: {repr(e)}')