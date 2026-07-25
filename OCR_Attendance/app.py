import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- DATABASE (Mock Data) ---
qr_items_db = {
    "demo-wallet": {
        "status": "registered",
        "item_name": "Black Leather Wallet",
        "owner": "Mohamed",
        "contact": "+20 100 555 1234 (Hidden)",
        "color": "Black",
        "reward": "Coffee on me! ☕"
    }
}

lost_reports_db = [
    {
        "id": "lost-001",
        "item_name": "Red Nike Backpack",
        "description": "Lost near the Tech Stage. My laptop is inside!",
        "tags": ["red", "backpack", "bag", "nike"],
        "owner_contact": "Sarah (Hidden)"
    }
]

# --- DESIGN (Safe Mode) ---
base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkIt | RiseUp Rescue</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .loader {
            border-top-color: #7e22ce;
            -webkit-animation: spinner 1.5s linear infinite;
            animation: spinner 1.5s linear infinite;
        }
        @keyframes spinner {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen text-gray-800 flex flex-col">
    <nav class="bg-white shadow-sm px-6 py-4 flex justify-between items-center sticky top-0 z-50">
        <div class="font-extrabold text-xl text-purple-700 flex items-center gap-2">
            <i class="fa-solid fa-circle-nodes"></i> LinkIt
        </div>
        <div class="text-xs font-bold bg-purple-100 text-purple-800 px-3 py-1 rounded-full">
            RISEUP LIVE
        </div>
    </nav>

    <main class="flex-grow max-w-md mx-auto mt-6 px-4 w-full pb-20">
        {{ content|safe }}
    </main>
    
    <div class="text-center py-4 text-xs text-gray-400">
        Built for RiseUp Summit 2026
    </div>
</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def home():
    content = """
    <div class="text-center py-6">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-2 tracking-tight">Lost Less.<br>Found Fast.</h1>
        <p class="text-gray-500 mb-8 text-lg">The smart recovery network.</p>
        
        <div class="space-y-4">
            <a href="/scan/demo-wallet" class="group block bg-white border-2 border-transparent p-6 rounded-2xl shadow-lg hover:border-purple-500 transition text-left flex items-center gap-5 relative overflow-hidden">
                <div class="absolute right-0 top-0 p-2 opacity-10">
                    <i class="fa-solid fa-qrcode text-8xl"></i>
                </div>
                <div class="w-14 h-14 bg-purple-100 rounded-2xl flex items-center justify-center text-purple-600 shadow-sm">
                    <i class="fa-solid fa-qrcode text-2xl"></i>
                </div>
                <div>
                    <h3 class="font-bold text-xl text-gray-900">Scan a Sticker</h3>
                    <p class="text-sm text-gray-500">I found an item with a QR</p>
                </div>
            </a>

            <a href="/finder_upload" class="group block bg-gradient-to-r from-purple-600 to-indigo-600 p-6 rounded-2xl shadow-lg text-left flex items-center gap-5 text-white relative overflow-hidden">
                 <div class="absolute right-0 top-0 p-2 opacity-20">
                    <i class="fa-solid fa-wand-magic-sparkles text-8xl"></i>
                </div>
                <div class="w-14 h-14 bg-white/20 rounded-2xl flex items-center justify-center text-white backdrop-blur-sm">
                    <i class="fa-solid fa-camera text-2xl"></i>
                </div>
                <div>
                    <h3 class="font-bold text-xl">Identify with AI</h3>
                    <p class="text-sm text-purple-100">No sticker? Snap a photo.</p>
                </div>
            </a>

            <a href="/scan/new-sticker" class="group block bg-white border border-gray-200 p-5 rounded-2xl shadow-sm hover:bg-gray-50 transition text-left flex items-center gap-4 mt-6">
                <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center text-green-600">
                    <i class="fa-solid fa-plus text-lg"></i>
                </div>
                <div>
                    <h3 class="font-bold text-gray-800">Secure New Item</h3>
                    <p class="text-xs text-gray-500">Link a fresh sticker</p>
                </div>
            </a>
        </div>
    </div>
    """
    return render_template_string(base_html, content=content)

# --- SCENARIO 1: QR CODE SCAN ---
@app.route('/scan/<item_id>')
def scan_qr(item_id):
    if item_id == "new-sticker":
        # Register View
        content = """
        <div class="bg-white p-8 rounded-3xl shadow-xl">
            <div class="text-center mb-8">
                <div class="inline-block p-4 bg-green-50 rounded-full text-green-600 mb-4 ring-4 ring-green-50">
                    <i class="fa-solid fa-shield-check text-3xl"></i>
                </div>
                <h2 class="text-2xl font-extrabold text-gray-900">Secure This Item</h2>
                <p class="text-gray-500">Link this QR code to you instantly.</p>
            </div>
            <form action="/" class="space-y-5">
                <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-2">What are you securing?</label>
                    <input type="text" placeholder="e.g. MacBook Pro M3" class="w-full bg-gray-50 border border-gray-200 p-4 rounded-xl focus:ring-2 focus:ring-green-500 outline-none font-bold text-gray-800 placeholder-gray-300">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-2">Your Contact (Hidden)</label>
                    <input type="text" placeholder="+20 1XX XXX XXXX" class="w-full bg-gray-50 border border-gray-200 p-4 rounded-xl focus:ring-2 focus:ring-green-500 outline-none font-bold text-gray-800 placeholder-gray-300">
                </div>
                <button type="button" onclick="alert('Protection Active! You are all set.'); window.location.href='/';" class="w-full bg-green-600 text-white font-bold text-lg py-4 rounded-xl shadow-lg hover:bg-green-700 transition transform active:scale-95">
                    Activate Shield
                </button>
            </form>
            <div class="mt-6 text-center">
                <a href="/" class="text-gray-400 text-sm hover:text-gray-600">Cancel</a>
            </div>
        </div>
        """
        return render_template_string(base_html, content=content)
    
    item = qr_items_db.get(item_id)
    if item:
        # FOUND REGISTERED ITEM
        content = f"""
        <div class="bg-gradient-to-b from-green-50 to-white p-6 rounded-3xl shadow-lg text-center border border-green-100">
            <div class="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center text-white mx-auto mb-4 shadow-green-200 shadow-xl ring-4 ring-white">
                <i class="fa-solid fa-check text-4xl"></i>
            </div>
            <h2 class="text-green-700 font-bold uppercase tracking-widest text-xs mb-2">Secure Match Found</h2>
            <h1 class="text-3xl font-extrabold text-gray-900 mb-2">{item['item_name']}</h1>
            
            <div class="bg-yellow-50 text-yellow-800 px-4 py-3 rounded-xl font-bold text-sm mb-8 inline-block border border-yellow-200">
                <i class="fa-solid fa-mug-hot mr-1"></i> Reward: {item['reward']}
            </div>

            <div class="space-y-3">
                <button onclick="alert('Calling Owner via Privacy Proxy...')" class="w-full bg-gray-900 text-white font-bold py-4 rounded-xl shadow-lg hover:bg-black transition flex items-center justify-center gap-3">
                    <i class="fa-solid fa-phone"></i> Call Owner Securely
                </button>
                <button onclick="alert('Location Sent anonymously!')" class="w-full bg-white border-2 border-gray-200 text-gray-700 font-bold py-4 rounded-xl hover:bg-gray-50 transition flex items-center justify-center gap-3">
                    <i class="fa-solid fa-location-dot text-gray-400"></i> Send Location
                </button>
            </div>
            <div class="mt-6">
                <a href="/" class="text-gray-400 text-sm hover:text-gray-600">Return Home</a>
            </div>
            <p class="text-xs text-gray-400 mt-6"><i class="fa-solid fa-lock"></i> Your number is never shared.</p>
        </div>
        """
        return render_template_string(base_html, content=content)
    return "Item not found"

# --- SCENARIO 2: AI MATCHING ---
@app.route('/finder_upload')
def finder_upload():
    content = """
    <div class="bg-white p-6 rounded-3xl shadow-xl">
        <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center text-purple-600">
                <i class="fa-solid fa-robot"></i>
            </div>
            <h2 class="text-xl font-bold text-gray-900">AI Visual Search</h2>
        </div>
        
        <p class="text-gray-500 text-sm mb-6 leading-relaxed">
            Found something without a sticker? Our <strong>Computer Vision</strong> engine will analyze the object and check lost reports instantly.
        </p>
        
        <form action="/processing" method="POST" enctype="multipart/form-data">
            <label class="block border-2 border-dashed border-purple-200 bg-purple-50 rounded-2xl p-10 text-center cursor-pointer hover:bg-purple-100 transition relative overflow-hidden group">
                <input type="file" name="photo" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full">
                <div class="transform group-hover:scale-110 transition duration-300">
                    <i class="fa-solid fa-camera text-4xl text-purple-400 mb-3"></i>
                    <p class="font-bold text-purple-700">Tap to Take Photo</p>
                </div>
            </label>
            
            <div class="mt-6">
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-2">Any details? (Optional)</label>
                <input type="text" name="desc" placeholder="e.g. Red Nike bag" class="w-full bg-gray-50 border border-gray-200 p-4 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none font-medium">
            </div>

            <button type="submit" class="w-full bg-purple-600 text-white font-bold text-lg py-4 rounded-xl shadow-lg hover:bg-purple-700 transition mt-6 flex justify-center items-center gap-2">
                <i class="fa-solid fa-bolt"></i> Start AI Scan
            </button>
        </form>
        <div class="mt-4 text-center">
            <a href="/" class="text-gray-400 text-sm hover:text-gray-600">Cancel</a>
        </div>
    </div>
    """
    return render_template_string(base_html, content=content)

@app.route('/processing', methods=['POST'])
def processing():
    desc = request.form.get('desc', '')
    
    # FAKE LOADING SCREEN (The "AI" Effect)
    content = f"""
    <div class="flex flex-col items-center justify-center py-24 text-center">
        <div class="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-20 w-20 mb-8 shadow-sm"></div>
        <h2 class="text-2xl font-extrabold text-gray-800 mb-2">Scanning Object...</h2>
        <div class="h-8">
            <p class="text-purple-600 font-mono text-sm font-bold animate-pulse" id="tags">Initializing Vision Model...</p>
        </div>
        
        <script>
            const tags = [
                'Detecting edges...', 
                'Analyzing color: #FF0000...', 
                'Identifying brand: Nike...', 
                'Object Class: Backpack...',
                'Querying Database...'
            ];
            let i = 0;
            setInterval(() => {{
                if(i < tags.length) {{
                    document.getElementById('tags').innerText = tags[i];
                    i++;
                }}
            }}, 600);
            
            setTimeout(() => {{
                window.location.href = "/ai_result?desc={desc}"; 
            }}, 3200);
        </script>
    </div>
    """
    return render_template_string(base_html, content=content)

@app.route('/ai_result')
def ai_result():
    desc = request.args.get('desc', '').lower()
    
    # Logic: "red" or "bag" triggers success
    if "red" in desc or "bag" in desc or "backpack" in desc:
        match = lost_reports_db[0]
        content = f"""
        <div class="bg-green-500 text-white p-8 rounded-b-3xl text-center -mx-4 -mt-6 mb-8 shadow-lg relative overflow-hidden">
             <div class="absolute inset-0 bg-white opacity-10" style="background-image: radial-gradient(#fff 1px, transparent 1px); background-size: 20px 20px;"></div>
            <div class="relative z-10">
                <div class="w-16 h-16 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center text-white mx-auto mb-3 border-2 border-white/50">
                    <i class="fa-solid fa-check text-3xl"></i>
                </div>
                <h1 class="text-3xl font-extrabold">We Found It!</h1>
                <p class="text-green-100 font-medium mt-1">AI Confidence Score: 98%</p>
            </div>
        </div>
        
        <div class="bg-white border border-gray-100 rounded-2xl p-5 flex gap-5 mb-6 shadow-sm">
            <div class="w-24 h-24 bg-gray-100 rounded-xl flex items-center justify-center text-xs text-gray-400 font-bold shrink-0">
                <i class="fa-solid fa-image text-3xl"></i>
            </div>
            <div>
                <h3 class="font-bold text-xl text-gray-900 leading-tight">{match['item_name']}</h3>
                <p class="text-sm text-gray-500 mt-1">{match['description']}</p>
                <div class="flex flex-wrap gap-2 mt-3">
                    <span class="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded-md font-bold">Red</span>
                    <span class="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded-md font-bold">Nike</span>
                    <span class="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded-md font-bold">Backpack</span>
                </div>
            </div>
        </div>
        
        <button onclick="alert('Great job! The owner has been notified.')" class="w-full bg-gray-900 text-white font-bold py-4 rounded-xl shadow-lg hover:bg-black transition mb-4">
            Notify Owner ({match['owner_contact']})
        </button>
        <div class="text-center">
            <a href="/" class="text-gray-400 text-sm font-medium hover:text-gray-600">Scan another item</a>
        </div>
        """
    else:
        content = """
        <div class="text-center py-12 px-6">
            <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center text-gray-400 mx-auto mb-6">
                <i class="fa-solid fa-magnifying-glass text-3xl"></i>
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">No Match Yet</h2>
            <p class="text-gray-500 leading-relaxed mb-8">We haven't seen a report for this item yet. We've saved your photo to the database and will alert you if the owner claims it.</p>
            <a href="/" class="inline-block bg-purple-600 text-white font-bold py-3 px-8 rounded-full shadow hover:bg-purple-700 transition">Return Home</a>
        </div>
        """
    return render_template_string(base_html, content=content)

if __name__ == '__main__':
    app.run(debug=True, port=5000)