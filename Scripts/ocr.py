import os
import uuid
import json
import tempfile
from io import BytesIO
from PIL import Image, ImageFilter, ImageOps
from winrt.windows.graphics.imaging import BitmapDecoder
from winrt.windows.storage.streams import InMemoryRandomAccessStream, DataWriter
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.globalization import Language
from .encrypt import Encrypt
from .https import AsyncPost

# CONFIG
FLEX = 20
AUTHFILE = os.path.expanduser("~/scamsight.auth.json")

def otsu(gray: Image.Image) -> int:
    hist = gray.histogram()
    total = sum(hist)
    sumb = 0
    wb = 0
    maximum = 0.0
    sum1 = sum(i * hist[i] for i in range(256))
    for t in range(256):
        wb += hist[t]
        if wb == 0:
            continue
        wf = total - wb
        if wf == 0:
            break
        sumb += t * hist[t]
        mb = sumb / wb
        mf = (sum1 - sumb) / wf
        between = wb * wf * (mb - mf) ** 2
        if between > maximum:
            threshold = t
            maximum = between
    return threshold

def binarize(img: Image.Image) -> Image.Image:
    img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
    gray = img.convert("L")
    gray = ImageOps.autocontrast(gray, cutoff=2)
    gray = gray.filter(ImageFilter.SHARPEN)
    t = otsu(gray) - FLEX
    binary = gray.point(lambda p: 0 if p <= t else 255)
    return binary

async def OCR(img: Image.Image) -> str | int:
    img = binarize(img)
    lut = [min(255, max(0, int((p - 128) * 2 + 128))) for p in range(256)]
    img = img.point(lut)

    bytestream = BytesIO()
    img.save(bytestream, format="BMP")
    bytestream.seek(0)
    data = bytestream.read()

    stream = InMemoryRandomAccessStream()
    writer = DataWriter(stream)
    writer.write_bytes(data)
    await writer.store_async()
    await writer.flush_async()
    writer.detach_stream()
    stream.seek(0)

    decoder = await BitmapDecoder.create_async(stream)
    frame = await decoder.get_frame_async(0)
    swb = await frame.get_software_bitmap_async()
    engine = OcrEngine.try_create_from_language(Language("en"))
    ocrresult = await engine.recognize_async(swb)

    result = []
    result.append({
        "type": "fulltext",
        "text": ocrresult.text
    })

    filenamesha256 = f"{str(uuid.uuid4())}.json.xz"
    tempdir = tempfile.gettempdir()
    sha256path = os.path.join(tempdir, filenamesha256)

    result.append({
            "type": "sha256'd",  
            "path":  sha256path,
        })

    jsondata = json.dumps(result, ensure_ascii=False).encode()

    with open(sha256path, "wb") as f:
        encrypted = Encrypt(jsondata)
        f.write(encrypted)

    with open(sha256path, "rb") as f:
        data = f.read()

    try:
        token = ""

        try:
            with open(AUTHFILE) as f:
                authdata = json.load(f)

            token = authdata.get("token")
        except Exception:
            pass

        if not token:
            return

        token = authdata.get("token")
        userid = authdata.get("userid")
    except Exception:
        return

    response = await AsyncPost(
        "https://api.scamsight.app/scamsight",
        data=data,
        headers={"Content-Type": "application/x-xz", "Authorization": token, "userid": userid},
        stream=True
    )
    
    if response.status_code != 200:
        return response.status_code

    response.raise_for_status()
    respjson = json.loads(response.content.decode())

    choices = respjson.get("choices", [])
    if choices and "message" in choices[0]:
        reasoning = choices[0]["message"]["content"]
        return reasoning
