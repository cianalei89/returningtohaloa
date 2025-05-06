
from flask import Flask, request, jsonify, render_template_string, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import json
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# ----------------- Initialize DB -----------------
# ----------------- Model -----------------
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(255))

with app.app_context():
    db.create_all()

# ----------------- Routes -----------------
@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            image_url = random.choice([
                "https://i.postimg.cc/G2TbnCRp/00-F48097-DE78-4-EE1-947-B-50-C115-FF5-B90.png",
                "https://i.postimg.cc/CxwMBXGv/0-F574900-382-C-44-ED-BAD7-7-D2-D27-C30-D72.png"
            ])
            entry = Entry(name=name, image=image_url)
            db.session.add(entry)
            db.session.commit()
        return redirect("/thanks")


@app.route("/names")
def names():
    entries = Entry.query.all()
    return jsonify([{"name": e.name, "image": e.image} for e in entries])

# Preset image URLs (replace these with your own if desired)
IMAGE_URLS = [
    "https://i.postimg.cc/G2TbnCRp/00-F48097-DE78-4-EE1-947-B-50-C115-FF5-B90.png",
    "https://i.postimg.cc/CxwMBXGv/0-F574900-382-C-44-ED-BAD7-7-D2-D27-C30-D72.png",
]

# --- FORM PAGE ---
FORM_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Submit Name</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      font-size: 16px;
      align-items: center;
      font-family: monospace;
    }
    .form-box {
      position: absolute;
      top: 10%;
      padding: 40px;
      border-radius: 12px;
      text-align: center;
    }
    input {
      display: block;
      width: 100%;
      margin: 12px 0;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 16px;
      font-family: monospace;
    }
    button {
      padding: 10px 20px;
      font-size: 16px;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-family: monospace;
    }
    button:hover {
      background-color: #45a049;
    }
    #background-container img,
    #static-background {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    #static-background {
      display: block;
      background-size: cover;
      background-position: center;
      transition: background-image 0.8s ease-in-out;
      z-index: -1;
    }
  </style>
</head>
<body>
  <div class="form-box">
    <h2>Enter your name:</h2>
    <form method="POST" action="/submit">
      <input name="name" placeholder="Your name" required>
      <button type="submit">Enter</button>
    </form>
  </div>
  <div id="background-container">
  <img id="static-background" src="https://i.postimg.cc/hjh9mgQg/C660152-F-7643-4576-B38-C-356-B2-D6-DF6-E4.png"></div>
  </div>
</body>
</html>
"""


THANKS_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Enter</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      font-family: monospace;
    }

    #background-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -1;
    }

    #background-container img,
    #static-background {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    #static-background {
      display: none;
      background-size: cover;
      background-position: center;
      transition: background-image 0.8s ease-in-out;
      z-index: -1;
    }

    #mid-background {
      background-size: cover;
      background-position: center;
      transition: background-image 0.8s ease-in-out;
      z-index: -1;
    }

    #hawaiian-text {
      position: absolute;
      top: 10%;
      width: 100%;
      text-align: center;
      font-size: 2em;
      color: white;
      z-index: 5;
      text-shadow: 2px 2px 6px black;
      white-space: pre-wrap;
    }

    #english-text {
      position: absolute;
      top: 80%;
      width: 100%;
      text-align: center;
      font-size: 2em;
      color: white;
      z-index: 5;
      text-shadow: 2px 2px 6px black;
      white-space: pre-wrap;
    }

    #object-container img {
      opacity: 0;
      animation: fadeIn 1s forwards;
      width: 80px;
      position: absolute;
    }

    #object-container span {
      position: absolute;
      background: rgba(0,0,0,0.5);
      color: white;
      padding: 4px 8px;
      border-radius: 5px;
    }

    @keyframes fadeIn {
      to { opacity: 1; }
    }

    #draggable-object {
      display: none;
      position: absolute;
      top: 50%;
      left: 50%;
      width: 315px;
      cursor: grab;
      z-index: 10;
      transform: translate(-26%, -54.3%);
    }

    #reveal-image {
      position: absolute;
      top: 50%;
      left: 50%;
      z-index: 20;
      display: none;
      width: 250px;
    }
    #drop-zone {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 200px;
        height: 100px;
        z-index: 5;
        transform: translate(-25.9%, -140%);
    }
  </style>
</head>
<body>

<div id="background-container">
    <img id="mid-background" src="https://i.postimg.cc/1R6p221y/A3489180-0427-49-FA-A6-D9-9-F7189-FE00-C2.png">
  <img id="gif1" src="https://i.postimg.cc/tRMB2v92/79-CE5-EBE-D53-B-44-BD-80-C7-513128-C8-B575.gif" style="display: none;">
  <img id="gif2" src="https://i.postimg.cc/FHZcn1jN/CEB3-BCBF-E1-D4-45-ED-A427-77842321-BBAC.gif" style="display: none;">
  <div id="static-background"></div>
</div>

<div id="hawaiian-text" class="hawaiian"></div>
<div id="english-text" class="english"></div>
<div id="object-container"></div>

<img id="draggable-object" src="https://i.postimg.cc/tC0p855N/DC649-BBD-C6-C2-42-E4-842-A-285-A59-C738-E0.png" alt="Draggable Object">
<img id="reveal-image" src="https://i.postimg.cc/T3DkFVtg/6931-E938-2683-40-EA-98-A1-3840918-F373-F.png">
<div id="drop-zone"></div>
<script>
  window.addEventListener('DOMContentLoaded', () => {
    const messages = [
      {
        english: "When the world was first being made, there existed only a few beings."
      },
      {
        hawaiian: "Wākea o’ia ka lani. Hoʻohōkūkalani o’ia nā hōkū. ‘O Wākea noho iā Hoʻohōkūkalani. Hānau ke keiki. He pēpē ʻeʻepa kāna; he keiki ʻaluʻalu.",
        english: "Wākea, the heavens, and Hoʻohōkūkalani, the stars, were two of them. Together, Hoʻohōkūkalani and Wākea had a child. But the baby was born prematurely."
      },
      {
        hawaiian: "ʻŌlelo ʻia ʻo ia e kanu i ia pēpē.", 
        english: "They were told to bury the baby."
      },
      {
        hawaiian: "I ia kanu ʻana a ma hope, kupu mai kekahi meakanu mai ke kino mai o kēia pēpē. ʻO kēia meakanu ke kalo mua loa. Ua kapa nā mākua i ka inoa o ia pēpē kalo ʻo Hāloanakalaukapalili.",
        english: "After the baby was buried, a plant grew from its body. This plant was the first taro plant. They called this taro baby Hāloanakalaukapalili."
      },
      {
        hawaiian: "Hāpai hou ʻo Hoʻohōkūkalani. I kēia hānau ʻana, puka mai he keikikāne. Ua kapa ʻo Hoʻohōkūkalani mā i kona inoa ʻo Hāloa ma muli o kona kaikuʻana kalo.", 
        english: "Hoʻohōkūkalani became pregnant once more. This time she gave birth to a human. They named him Hāloa in honor of his older sibling."
      },
      {
        english: "Welcome to the world, Hāloa."
      },
      {
        english: "You are feeling hungry. It’s time to harvest some food…"
      }
    ];

    const backg1Duration = 5000;
    const gif1Duration = 20000;
    const backgDuration = 5000;
    const gif2Duration = 11000;
    const backg3Duration = 15000;
    const intro = 5000

  function typeWriterDual(hawText, engText, callback) {
    const hawEl = document.getElementById('hawaiian-text');
    const engEl = document.getElementById('english-text');

    hawEl.innerText = "";
    engEl.innerText = "";

    // If there is no Hawaiian text, just show English at the top
    if (!hawText) {
      hawEl.innerText = ""; // clear hawaiian
      engEl.style.top = "10%"; // move English to the top
      engEl.style.bottom = ""; // reset bottom if previously set
      let i = 0;
      const speed = 50;
      function typeChar() {
        if (i < engText.length) {
          engEl.innerText += engText.charAt(i);
          i++;
          setTimeout(typeChar, speed);
        } else if (callback) {
          setTimeout(callback, 1000);
        }
      }
      typeChar();
    } else {
      // Bilingual mode
      hawEl.style.display = "block";
      engEl.style.bottom = "10%";
      engEl.style.top = ""; // clear top

      let i = 0, j = 0;
      const speed = 50;
      function typeChar() {
        let done = true;
        if (i < hawText.length) {
          hawEl.innerText += hawText.charAt(i);
          i++;
          done = false;
        }
        if (j < engText.length) {
          engEl.innerText += engText.charAt(j);
          j++;
          done = false;
        }
        if (!done) {
          setTimeout(typeChar, speed);
        } else if (callback) {
          setTimeout(callback, 1000);
        }
      }
      typeChar();
    }
  }

    typeWriterDual(messages[0].hawaiian,messages[0].english);

    setTimeout(() => {
      document.getElementById('mid-background').style.display = 'none';
      document.getElementById('gif1').style.display = 'block';
      typeWriterDual(messages[1].hawaiian, messages[1].english);
    }, backg1Duration);

    setTimeout(() => {
      document.getElementById('gif1').style.display = 'none';
      document.getElementById('mid-background').style.display = 'block';
      typeWriterDual(messages[2].hawaiian, messages[2].english);
    }, backg1Duration + gif1Duration);

    setTimeout(() => {
      document.getElementById('mid-background').style.display = 'none';
      document.getElementById('gif2').style.display = 'block';
      typeWriterDual(messages[3].hawaiian, messages[3].english);
    }, backg1Duration + gif1Duration + backgDuration);

    setTimeout(() => {
      document.getElementById('gif2').style.display = 'none';
      document.getElementById('mid-background').style.display = 'block';
      typeWriterDual(messages[4].hawaiian, messages[4].english);
    }, backg1Duration + gif1Duration + backgDuration + gif2Duration);

    setTimeout(() => {
      document.getElementById('mid-background').style.display = 'none';
      document.getElementById('static-background').style.display = 'block';
      updateBackground();
      typeWriterDual(messages[5].hawaiian,messages[5].english);
    }, backg1Duration + gif1Duration + backgDuration + gif2Duration + backg3Duration);

    setTimeout(() => {
      updateBackground();
      typeWriterDual(messages[6].hawaiian,messages[6].english);
    }, backg1Duration + gif1Duration + backgDuration + gif2Duration + backg3Duration + intro);

    const draggable = document.getElementById('draggable-object');
    const reveal = document.getElementById('reveal-image');
    const backgroundEl = document.getElementById('static-background');
    const dropZone = document.getElementById('drop-zone');

    let isDragging = false;
    let offsetX, offsetY;

    draggable.addEventListener('mousedown', (e) => {
      isDragging = true;
      offsetX = e.clientX - draggable.offsetLeft;
      offsetY = e.clientY - draggable.offsetTop;
      draggable.style.cursor = 'grabbing';
    });

    document.addEventListener('mousemove', (e) => {
      if (isDragging) {
        const x = e.clientX - offsetX;
        const y = e.clientY - offsetY;
        draggable.style.left = x + 'px';
        draggable.style.top = y + 'px';

        const zoneRect = dropZone.getBoundingClientRect();
        const objRect = draggable.getBoundingClientRect();

        if (
            objRect.top < zoneRect.bottom &&
            objRect.bottom > zoneRect.top &&
            objRect.left < zoneRect.right &&
            objRect.right > zoneRect.left
            ) {
            window.location.href = "/harvest"; 
        }

      }
    });

    document.addEventListener('mouseup', () => {
      isDragging = false;
      draggable.style.cursor = 'grab';
    });

    const backgrounds = [
      'url(https://i.postimg.cc/hjh9mgQg/C660152-F-7643-4576-B38-C-356-B2-D6-DF6-E4.png)',
      'url(https://i.postimg.cc/qq3ymLG5/82-D45-E59-14-F5-4-AF8-9981-08-E7-AC6-F323-C.png)',
      'url(https://i.postimg.cc/G38FhL1x/AEBF1-C5-F-975-D-40-A9-8008-B5-BBB6288-FE2.png)'
    ];

    let currentBackgroundIndex = 0;
    let targetIndexForDraggable = 1;
    let backgroundCycleInterval = 5000;

    function updateBackground() {
      backgroundEl.style.backgroundImage = backgrounds[currentBackgroundIndex];

      if (currentBackgroundIndex === targetIndexForDraggable) {
        draggable.style.display = 'block';
      } else {
        draggable.style.display = 'none';
      }

      currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;
      setTimeout(updateBackground, backgroundCycleInterval);
    }
  });
</script>
</body>
</html>
"""


loi_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Lo`i</title>
  <style>
    body {
      margin: 0;
      overflow-x: hidden;
      overflow-y: auto;
      font-family: monospace;
      background-size: cover;
      background-repeat: repeat-y; /* scrolls vertically */
      background-attachment: scroll; /* makes it scroll with the page */
      background-position: center top;
    }

    #background-container {
      position: relative;
      z-index: 2;
    }


    #message {
      position: absolute;
      top: 20%;
      width: 100%;
      text-align: center;
      font-size: 2em;
      color: white;
      z-index: 5;
      text-shadow: 2px 2px 6px black;
      white-space: pre-wrap;
    }

    #hero-wrapper {
        position: relative;
        width: 100%;
        height: auto;
    }

    #hero-image {
        width: 100%;
        display: block;
    }

    #hero-section::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        height: 100px;
        width: 100%;
        background: linear-gradient(to bottom, transparent, #572a0d);
    }
    
    #fade-bg {
        height: 300vh;
        background-color: #572a0d; 
    }
    #object-grid {
        position: absolute;
        top: 55%;
        left: 0;
        width: 90%;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        column-gap: 30px;
        row-gap: 20px;
        justify-items: center;
        padding: 20px 40px;
    }
    .grid-item {
        position: relative;
        width: auto;
    }
    .grid-item img {
        width: 200px;
        height: auto;
        display: block;
    }
    .grid-item span {
        bottom: -1.5em;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    .grid-item:hover span {
        opacity: 1;
    }

    @keyframes fadeIn {
      to { opacity: 1; }
    }
  </style>
</head>
<body>
<div id="hero-wrapper">
  <img id="hero-image" src="https://i.postimg.cc/x1wMM0dv/5-C7-A8-D32-F351-4072-B0-A6-91-C0-E22-B76-E7.png" alt="Background">
  <div id="object-grid"></div>
</div>
<div id="fade-bg"></div>
<div id="message"></div>

<script>
  window.addEventListener('DOMContentLoaded', () => {
    function showObjects() {
        fetch('/names')
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById('object-grid');
                data.forEach(entry => {
                    const wrapper = document.createElement('div');
                    wrapper.className = 'grid-item';

                    const img = document.createElement('img');
                    img.src = entry.image;

                    const label = document.createElement('span');
                    label.textContent = entry.name;

                    wrapper.appendChild(img);
                    wrapper.appendChild(label);
                    container.appendChild(wrapper);
                });
            });
    }
    showObjects();

    const messages = [
      "Hāloa was the first Hawaiian, and Hāloanakalaukapalili his closest sibling.",
      "Hāloa's older siblings all took good care of him, and he took good care of them.",
      "We are all descendants of Hāloa. Kalo, Hāloanakalaukapalili, is our elder along with the rest of the natural world.",
      "And like all good moʻolelo, the story continues through us. To care for Kalo is to care for Hāloa. To cultivate Kalo is to remember who we are. This is not the end, but a return.",
      "Thank you for visiting.",
      "Credits: Thank you to the Kanaka ʻŌiwi wahine who have come before me, whose scholarship has guided me in the creation of this website and everything I do. Inspiration for this page comes from writings of Mary Kawena Pukui, Manulani Aluli Meyer, and Joyce Pualani Warren. The initial story and some illustrations have been adapted from William Wilson's Hāloa, the First Hawaiian."
    ];

    const text1 = 5000;
    const text2 = 8000;
    const text3 = 12000;
    const text4 = 20500;
    const text5 = 5000;

    function typeWriter(text, callback) {
      const messageEl = document.getElementById('message');
      messageEl.innerText = "";
      let i = 0;
      const speed = 50;

      function typeChar() {
        if (i < text.length) {
          messageEl.innerText += text.charAt(i);
          i++;
          setTimeout(typeChar, speed);
        } else if (callback) {
          setTimeout(callback, 1000);
        }
      }

      typeChar();
    }

    typeWriter(messages[0]);

    setTimeout(() => {
      typeWriter(messages[1]);
    }, text1);
    setTimeout(() => {
      typeWriter(messages[2]);
    }, text1 + text2);
    setTimeout(() => {
      typeWriter(messages[3]);
    }, text1 + text2 + text3);
    setTimeout(() => {
      typeWriter(messages[4]);
    }, text1 + text2 + text3 + text4);
    setTimeout(() => {
      typeWriter(messages[5]);
    }, text1 + text2 + text3 + text4 + text5);
  });             
</script>

</body>
</html>
"""

harvest_html = """
<!DOCTYPE html>
    <html>
    <head>
        <title>Reveal</title>
        <style>
            body {
                margin: 0;
                background: #56a3b8;
                display: flex;
                flex-direction: column;     /* stack items vertically */
                align-items: center;        /* center horizontally */
                min-height: 100vh;
                padding-top: 40px;  
                font-family: monospace;
            }
            #initial-image {
                max-width: 80%;
                position: absolute;
                top: 25%;
                left: 50%
                transform: translate(0%, 50%);
            }
            .new-images {
                display: none;
                opacity: 0;
                transition: opacity 0.5s ease;
            }

            #image-container {
                display: flex;
                gap: 40px;
                justify-content: center;
                align-items: center;
            }

            #initial-text {
                position: absolute;
                top: 15%;
                width: 80%;
                text-align: center;
                font-size: 20px;
                color: white;
                z-index: 5;
                text-shadow: 2px 2px 6px black;
                white-space: pre-wrap;
            }
            
            #txtpoi {
                color: white;
            }
            .imgtxt {
                position: relative;
                display: inline-block;
            }
            .image-button {
                background: none;
                border: none;
                padding: 0;
                cursor: pointer;
            }
            .image-button img {
                display: block;
                max-width: 100%;
            }

            .imgtxt span {
                position: absolute;
                top: 60%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 20px;
                color: white;
                opacity: 0;
                transition: opacity 0.3s ease;
                pointer-events: none;
                text-shadow: 2px 2px 4px black;
                font-family: monospace;
            }
            .imgtxt:hover span, .imgtxt:focus span {
                opacity: 1;
            }
            .imgtxt:hover img, .imgtxt:focus img {
                /* add hover effects like transform or filter to your images here! */
                z-index: 3;
                cursor:pointer;
        </style>
    </head>
    <body>
        <div id="initial-text"></div>
        <img id="initial-image" src="https://i.postimg.cc/T3DkFVtg/6931-E938-2683-40-EA-98-A1-3840918-F373-F.png">
        <div id="image-container">
            <img class="new-images" src="https://i.postimg.cc/YCXmkZjW/EA1-B9-D7-B-B5-D4-4-AAB-B320-5-E5-FE8-EED3-DA.png">

            <div class="imgtxt new-images" id="poi-object">
                <form method="GET" action="/pound">
                    <button type="submit" class="image-button">
                        <img src="https://i.postimg.cc/43mH3PhF/CA0-C1-CE9-6-CB7-4-DEC-A2-D4-1-F17-CF888863.png" alt="Clickable Kalo">
                        <span>Poi</span>
                    </button>
                </form>
            </div>
        </div>

        <div id="txtpoi" style="display: none;">
            <h2>Now click on the corm to make some poi!</h2>
        </div>
        <div id="poi" class="imgtxt">
            <img src="https://via.placeholder.com/200x200?text=Kalo" alt="">
            <span>Poi</span>
        </div>

        <script>
            window.addEventListener('DOMContentLoaded', () => {
                const messageText =
                    "Great job. Now its time to replant and eat. Click your harvested Kalo to slice off the corm.";

                const initial = document.getElementById('initial-image');
                const txt = document.getElementById('initial-text');
                const newImages = document.querySelectorAll('.new-images');
                const butt = document.getElementById('txtpoi');

                function typeWriter(text, callback) {
                    const messageE1 = document.getElementById('initial-text');
                    messageE1.innerText = "";
                    let i = 0;
                    const speed = 50;

                    function typeChar() {
                        if (i < text.length) {
                        messageE1.innerText += text.charAt(i);
                        i++;
                        setTimeout(typeChar, speed);
                        } else if (callback) {
                        setTimeout(callback, 1000);
                        }
                    }

                    typeChar();
                }

                typeWriter(messageText);

                initial.addEventListener('click', () => {
                    initial.style.display = 'none';
                    txt.style.display = 'none';
                    newImages.forEach(img => {
                        img.style.display = 'block';
                        img.style.opacity = 1;
                    });
                    butt.style.display = 'block';
                });
            });
        </script>

    </body>
    </html>
    """

prep_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Making Poi</title>
    <style>
        body {
            margin: 0;
            background: #56a3b8;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding-top: 20px;
            font-family: monospace;
            color: white;
        }

        #message {
            position: absolute;
            top: 10%;
            width: 100%;
            text-align: center;
            font-size: 18px;
            color: white;
            z-index: 5;
            text-shadow: 2px 2px 6px black;
            white-space: pre-wrap;
        }

        @keyframes blink-caret {
            from, to { border-color: transparent; }
            50% { border-color: white; }
        }

        .video-wrapper, .form-box {
            display: none;
            flex-direction: column;
            align-items: center;
        }

        .video-wrapper {
            margin-top: 150px;
        }

        iframe {
            border: 4px solid white;
            border-radius: 12px;
        }

        .form-box {
            position: absolute;
            top: 40%;
        }

        button {
            padding: 10px 20px;
            font-size: 18px;
            border: none;
            border-radius: 6px;
            background-color: white;
            color: #56a3b8;
            cursor: pointer;
            font-family: monospace;
        }

        button:hover {
            background-color: #e6e6e6;
        }

        #continue-button {
            position : absolute;
            top: 90%
        }
        #boil{
          display: none;
          position : absolute;
          width: 47%;         
        }
        #clean{
          display: none;
          position : absolute;
          width: 60%;         
        }        
    </style>
</head>
<body>

    <div id="message"></div>
    <img id="boil" src = "https://i.postimg.cc/mkQC9zyP/66-FBABDC-188-C-4-CCB-A454-56135639-D5-FD.gif">
    <img id="clean" src = "https://i.postimg.cc/hvFVhbTF/346-C066-B-0242-49-FB-B7-BD-5-FE464-D68852.gif">

    <div class="video-wrapper" id="video-container">
        <iframe
            width="800"
            height="500"
            src="https://www.youtube.com/embed/9eyL4q6lAWY"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
    </div>

    <button id="continue-button" style="display: none;">Continue</button>

    <div class="form-box" id="form-container">
        <h2>Eat your poi</h2>
        <form method="GET" action="/bowl">
            <button type="submit">Poi</button>
        </form>
    </div>

    <script>
        function typeWriter(text, callback) {
            const messageEl = document.getElementById('message');
            messageEl.innerText = "";
            let i = 0;
            const speed = 50;

            function typeChar() {
                if (i < text.length) {
                    messageEl.innerText += text.charAt(i);
                    i++;
                    setTimeout(typeChar, speed);
                } else if (callback) {
                    setTimeout(callback, 5000);
                }
            }

            typeChar();
        }

        window.onload = function() {
            const introText = "Kalo is not edible in its raw form, you must first boil it.";
            const text2 = "After boiling, you must clean the corm by scraping off the skin.";
            const text3 = "Now it’s ready to be pounded. Let’s join ʻanakala to pound our Kalo.";
            const text4 = "Now that your kalo has been pounded it can be moved to the ʻumeke ʻai to be shared by the whole ʻohana.";

            const boiling = document.getElementById('boil');
            const cleaning = document.getElementById('clean');


            const videoContainer = document.getElementById('video-container');
            const continueButton = document.getElementById('continue-button');
            const formContainer = document.getElementById('form-container');

            typeWriter(introText, function () {
                typeWriter(text2, function () {                 
                    typeWriter(text3, function(){
                      cleaning.style.display = 'none';
                      videoContainer.style.display = 'flex';
                      continueButton.style.display = 'inline-block';                         
                    });   
                });
            }); 

            setTimeout(function (){
                boiling.style.display = 'block';
              }, 3000);
            setTimeout(function (){
              boiling.style.display = 'none';
              cleaning.style.display = 'block';
            }, 10000);                

            continueButton.addEventListener('click', function () {
                // Hide video and button
                videoContainer.style.display = 'none';
                continueButton.style.display = 'none';  

            typeWriter(text4, function () {
                setTimeout(function () {
                    formContainer.style.display = 'flex';
                }, 3000);
                });
            });
        };
    </script>

</body>
</html>
"""

poi_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      background: url("https://i.postimg.cc/1R6p221y/A3489180-0427-49-FA-A6-D9-9-F7189-FE00-C2.png");
      overflow: hidden;
      font-family: monospace;
      color: white;
      background-size: cover;
    }

    #intro-text {
      position: absolute;
      top: 10%;
      width: 100%;
      text-align: center;
      font-size: 1.5em;
    }

    #poi-bowl {
      max-width: 80%;
      position: absolute;
      top: 10%;
      left: 50%;
      transform: translateX(-50%);
      display: none;
    }

    .name {
      position: absolute;
      font-size: 1.2em;
      white-space: nowrap;
      pointer-events: none;
    }

    button {
      padding: 10px 20px;
      font-size: 18px;
      border: none;
      border-radius: 6px;
      background-color: white;
      color: #56a3b8;
      cursor: pointer;
      font-family: monospace;
    }

    button:hover {
            background-color: #e6e6e6;
    }

    .form-box {
        display: none;
        position: absolute;
        top: 85%;
        left: 46.5%;
    }
  </style>
</head>
<body>

<div id="intro-text"></div>
<img id="poi-bowl" src="https://i.postimg.cc/76S3fvRN/6960-DE74-0-BF8-468-E-A7-D8-AE51874-FE1-DF.png" style="display: none">
<div class="form-box" id="button">
  <form method="GET" action="/next">
    <button type="submit">Replant</button>
  </form>
</div>
<div id="intro-text"></div>

<script>
  const introMessage = "Itʻs finally time to eat.";
  const introTextEl = document.getElementById('intro-text');
  const bowlImg = document.getElementById('poi-bowl');
  const butt = document.getElementById('button');
  const manners = "Gathered around the poi bowl are all of the members who have entered this site before you. Eating poi is a time to connect and reconnect. Remember that when eating, thoughts and conversations should only reflect joyful conversation. Through poi, you are connected back to Hāloa and to the many generations that have sustained and been sustained by this plant. You are not eating alone, you are part of a shared genealogy.";
  const replant = "But donʻt forget to replant your kalo. Through it, Haloanakalaukapili lives on, and so do you.";

  function typeWriter(text, i = 0, callback) {
    if (i < text.length) {
      introTextEl.innerHTML += text.charAt(i);
      setTimeout(() => typeWriter(text, i + 1, callback), 50);
    } else if (callback) {
      setTimeout(callback, 500);
    }
  }

  function showBowlAndNames() {
    bowlImg.style.display = 'block';

    setTimeout(() => {
      introTextEl.innerText = "";
      typeWriter(manners, 0, () => {
        fetch('/names')
          .then(res => res.json())
          .then(data => {
            data.forEach((entry, index) => {
              setTimeout(() => {
                createFloatingName(entry.name);
              }, index * 1000);
            });
          });
      });
      setTimeout(() => {
        introTextEl.innerText = "";
        typeWriter(replant, 0, () => {
        });
        setTimeout(() => {
          butt.style.display = 'block';
        },3000);
      }, 33000);
    }, 3000);
        
  }

  function createFloatingName(nameText) {
    const el = document.createElement('div');
    el.className = 'name';
    el.textContent = nameText;

    let x = Math.random() * (window.innerWidth - 100);
    let y = Math.random() * (window.innerHeight - 50);
    let dx = (Math.random() - 0.5) * 2;
    let dy = (Math.random() - 0.5) * 2;

    el.style.left = x + 'px';
    el.style.top = y + 'px';
    el.style.position = 'absolute';

    document.body.appendChild(el);

    function move() {
      const rect = el.getBoundingClientRect();
      if (rect.left + dx < 0 || rect.right + dx > window.innerWidth) dx *= -1;
      if (rect.top + dy < 0 || rect.bottom + dy > window.innerHeight) dy *= -1;
      x += dx;
      y += dy;
      el.style.left = x + 'px';
      el.style.top = y + 'px';
      requestAnimationFrame(move);
    }

    move();
  }

  // Start animation
  typeWriter(introMessage, 0, showBowlAndNames);
</script>


</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def index():
    return render_template_string(FORM_PAGE)


@app.route('/thanks')
def thanks():
    return render_template_string(THANKS_PAGE)

@app.route('/harvest')
def harvest():
    return render_template_string(harvest_html)

@app.route('/prep')
def prep():
    return render_template_string(prep_html)

@app.route('/pound', methods=['GET'])
def pound():
    return redirect('/prep')

@app.route('/bowl', methods=['GET'])
def bowl():
    return redirect('/poi')

@app.route('/poi')
def poi():
    return render_template_string(poi_html)


@app.route('/next', methods=['GET'])
def next():
    return redirect('/loi')

@app.route('/loi')
def loi():
    return render_template_string(loi_html)

if __name__ == '__main__':
    app.run(debug=True)











