import streamlit as st
import io
import requests
from PIL import ImageDraw
from PIL import Image  # 画像扱う

SUBSCRIPTION_KEY = 'c14d5ee38adc4f04b447e182202c11cc'
assert SUBSCRIPTION_KEY
face_api_url = 'https://20210505gaku.cognitiveservices.azure.com/face/v1.0/detect'

# タイトル
st.title('顔認識アプリ')

# ファイルアップローダー
uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()  # バイナリ取得

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    params = {
        'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses,emotion,hair',
        'returnFaceId': 'true'
    }

    res = requests.post(face_api_url, params=params,
                        headers=headers, data=binary_img)

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left'] + rect['width']), (rect['top'] + rect['height'])],
                       fill=None, outline='green', width=5)
    st.image(img, caption='Uploaded Image.', use_column_width=True)



