import glob
import os
from typing import Any
from typing_extensions import Annotated
from fastapi import FastAPI, Form, Request
from starlette.responses import FileResponse, JSONResponse

app = FastAPI()

@app.get("/")
def index():
    return FileResponse("index.html")

@app.get("/editor")
def editor():
    return FileResponse("weltmeister.html")

@app.post("/lib/weltmeister/api/save.php")
def api_save(data: Annotated[Any, Form()], path: Annotated[str, Form()]):
    if path == "":
      return JSONResponse({'error': 1, "msg": "No Data or Path specified"})

    if not path.endswith('.js'):
      return JSONResponse({'error': 3, "msg": "File must have a .js suffix"})

    try:
      with open(path, "w") as file:
        file.write(data)
        return JSONResponse({'error': 0})
    except:
      return JSONResponse({'error': 2, "msg": "Couldn't write to file %d" % path})

@app.get("/lib/weltmeister/api/browse.php")
def api_browse(request: Request):
    dir = "**"
    if 'dir' in request.query_params:
        if request.query_params['dir'] != "":
          dir = request.query_params['dir'].replace("%2F", "/")
  
    files = glob.glob(dir + '*.*')

    if 'type' in request.query_params:
        types = request.query_params['type']
        files = []
        if 'images' in types:
            for ext in [".png", ".jpg", ".gif", ".jpeg"]:
              files.extend(glob.glob(f"{dir}/*{ext}"))
        elif 'scripts' in types:
            files.extend(glob.glob(f"{dir}/*.js"))

    dirs = [*set([os.path.dirname(file) for file in files])]

    response = {
        'files': files,
        'dirs': dirs,
        'parent': False if dir == '**' else os.path.dirname(os.path.dirname(dir))
    }
    return JSONResponse(response)

@app.get("/lib/weltmeister/api/glob.php")
def api_glob(request: Request):
    globs = request.query_params["glob[]"]
    files = glob.glob(globs)
    return JSONResponse(files)

@app.get("/{catchall:path}", response_class=FileResponse)
def read_index(request: Request):
    filepath = request.path_params["catchall"]

    if os.path.exists(filepath):
        return FileResponse(filepath)

    raise Exception(f"{filepath} requested but could not be found")