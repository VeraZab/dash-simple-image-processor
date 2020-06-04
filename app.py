import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import skimage.io
import skimage.transform
import io_utils

app = dash.Dash(__name__)

app.layout = html.Div(
    id="main",
    children=[
        html.H1("Image Processing Template"),
        html.H2("Made with Dash and scikit-image"),
        html.P(children=[
            "This shows how an app for processing images can be made in ~100 lines of code with Dash and scikit-image. You can add your image processing algorithm by cloning this app: ",
            html.A("https://github.com/plotly/dash-simple-image-processor",
                    href="https://github.com/plotly/dash-simple-image-processor"),
            ". Learn more about ",
            html.A("Dash",href='https://plotly.com/dash/'),
            " and ",
            html.A("scikit-image",href="https://scikit-image.org/"),
            "."]),
        dcc.Upload(id="uploader", children=html.Button("Load Image"), multiple=False),
        html.A(
            id="downloader", download="image.png", children=[html.Button("Save Image")]
        ),
        html.H6("Rotation (degrees)", id="rotation-display"),
        dcc.Slider(id="rotation-slider", min=0, max=360, step=0.01, value=0,),
        html.Img(id="image-display", alt="The transformed image"),
        dcc.Store(id="input-image", data=None),
    ],
)


@app.callback(Output("input-image", "data"), [Input("uploader", "contents")])
def store_uploader_contents(uploader_contents):
    if uploader_contents is None:
        return dash.no_update
    return uploader_contents


@app.callback(
    [
        Output("image-display", "src"),
        Output("downloader", "href"),
        Output("rotation-display", "children"),
    ],
    [Input("input-image", "data"), Input("rotation-slider", "value")],
)
def process_image(input_image_data, rotation_slider_value):
    if input_image_data is None or rotation_slider_value is None:
        return dash.no_update
    print(input_image_data)
    im = io_utils.img_from_mime(input_image_data)

    # process the image here...
    im = skimage.transform.rotate(im, rotation_slider_value, resize=True)

    mimestr = io_utils.mime_from_img(im)
    return (mimestr, mimestr, "Rotation: %.2f\u00B0" % rotation_slider_value)


if __name__ == "__main__":
    app.run_server(debug=True)
