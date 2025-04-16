from dash import Dash, html, dcc, Input, Output, State
import requests
import os

# Initialize Dash app
dash_app = Dash(__name__)
server = dash_app.server  # Share Flask server with Dash

UPLOAD_FOLDER = 'uploads'

# Dash layout
dash_app.layout = html.Div([
    html.H1("Test Steps Optimization Dashboard"),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload File'),
            multiple=False
        ),
    ], style={'marginBottom': '20px'}),

    html.Div(id='file-upload-msg'),
    html.Br(),

    html.Button('Optimize Test Steps', id='optimize-button', n_clicks=0),
    html.Div(id='optimization-msg'),
    html.Br(),

    html.A("Download Optimized File", id='download-link', href='', target='_blank', style={'display': 'none'})
])

# Callbacks
@dash_app.callback(
    Output('file-upload-msg', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def upload_file(contents, filename):
    if contents is None:
        return "No file uploaded yet."

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(contents.split(',')[1].encode('utf-8'))
    return f"File '{filename}' uploaded successfully."

@dash_app.callback(
    [Output('optimization-msg', 'children'),
     Output('download-link', 'href'),
     Output('download-link', 'style')],
    Input('optimize-button', 'n_clicks'),
    State('upload-data', 'filename')
)
def optimize_file(n_clicks, filename):
    if n_clicks == 0 or filename is None:
        return "Click the button to optimize the file.", '', {'display': 'none'}

    # Call Flask API to process the file
    response = requests.post('http://localhost:5000/upload', files={'file': open(os.path.join(UPLOAD_FOLDER, filename), 'rb')})

    if response.status_code == 200:
        optimized_file = response.json()['optimized_file']
        download_url = f'/download/{optimized_file}'
        return "File optimized successfully.", download_url, {'display': 'inline'}

    return f"Error: {response.json()['error']}", '', {'display': 'none'}

# Run Dash app
if __name__ == '__main__':
    dash_app.run(debug=True)