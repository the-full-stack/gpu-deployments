from pathlib import Path

from fastapi import FastAPI
import modal

import text_recognizer

# create a modal "Stub" on which everything runs
stub = modal.Stub(name="fsdl-text-recognizer")

# production requirements, copied from 2022 course repo
requirements = [
  "h5py",
  "importlib-metadata>=4.4",
  "numpy",
  "pyngrok",
  "requests",
  "smart_open[s3]",
  "tqdm",
  "gradio~=3.10",
  "Jinja2>=2.11,<2.12",
  "pillow",
  "torch>=1.13,<1.14",
  "torchvision>=0.14,<0.15",
  "markupsafe<2.1",
]

# define the container image we're running in
image = modal.Image.debian_slim().pip_install(requirements)

# define the local path of the model weights
model_path = Path("text_recognizer") / "artifacts"
local_path = Path(__file__).parent / model_path
remote_path = Path("/") / "root" / model_path

# set up our app with FastAPI
web_app = FastAPI()


# make a debugging Modal function
@stub.function(image=image, interactive=True, gpu="any",
    mounts=[
      *modal.create_package_mounts(["text_recognizer"]),
      modal.Mount(local_dir=local_path, remote_dir=remote_path)
    ]
)
def debug():
  """Use this with modal run app::stub.debug to get a debugging environment."""
  import IPython
  IPython.embed()


# run an Asynchronous Server Gateway Interface for our FastAPI app
@stub.asgi(
    image=image,  # use our existing image
    gpu="any",  # get a GPU so we can run faster
    mounts=[  # mount the library and the model weights
      *modal.create_package_mounts(["text_recognizer"]),
      modal.Mount(local_dir=local_path, remote_dir=remote_path)
    ],
    label="fsdl-text-recognizer",  # simplify the URL
)
def fastapi_app():
    import gradio as gr

    from text_recognizer.paragraph_text_recognizer import ParagraphTextRecognizer

    model = ParagraphTextRecognizer()  # load model

    # add a gradio UI around inference
    interface = gr.Interface(
        fn=model.predict,
        inputs=gr.components.Image(type="pil", label="Handwritten Text"),
        outputs=gr.components.Textbox(),
        title=f"📝 Text Recognizer",
        allow_flagging="never",
        cache_examples=False,
    )

    # mount for execution on Modal
    return gr.mount_gradio_app(
        app=web_app,
        blocks=interface,
        path="/",
    )
