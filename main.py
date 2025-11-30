from flask import Flask, request, jsonify, render_template
from tpblite import TPB
from player import Player
from torrent import tr   # replace with actual filename
from config import Config
import subprocess
import socket

# Init Flask
app = Flask(__name__)

cf = Config("config.yaml")

# Init Pirate Bay
tpb = TPB(base_url=cf.get("tbp_url"))

player = Player()

# Init qBittorrent wrapper (API v4 by default)
qb = tr(url=cf.get("qb_url"))   # qBittorrent default WebUI port is 8080

def get_local_ip():

    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.5)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except: 
            return "127.0.0.1"

@app.route("/")
def index():    
    return render_template("index.html")

@app.route("/mydownloads")
def downloads_page():
    return render_template("downloads.html")

@app.route("/controller")
def remote():
    return render_template("controller.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    torrents = tpb.search(query)
    results = [{
        "title": t.title,
        "seeds": t.seeds,
        "leeches": t.leeches,
        "upload_date": t.upload_date,
        "uploader": t.uploader,
        "filesize": t.filesize,
        "byte_size": t.byte_size,
        "magnetlink": t.magnetlink,
        "url": t.url,
        "is_trusted": t.is_trusted,
        "is_vip": t.is_vip,
        "infohash": t.infohash,
        "category": t.category
    } for t in torrents]
    return jsonify(results)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    magnet = data.get("magnetlink")
    if not magnet:
        return jsonify({"error": "No magnetlink"}), 400
    
    success = qb.download_torrent(magnet)
    if success:
        return jsonify({"status": "added"})
    return jsonify({"status": "failed"}), 500

@app.route("/downloads")
def downloads():
    try:
        tasks = qb.torrent_status()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    results = [{
        "hash": d["hash"],
        "name": d["name"],
        "status": d["state"],
        "progress": f"{d['progress']*100:.2f}%",
        "speed": f"{d['dlspeed']/1024:.1f} KiB/s",
        "eta": tr.format_eta(d["eta"])
    } for d in tasks]
    return jsonify(results)

@app.route('/watch/<name>')
def watch(name):
    file = qb.get_file_path(name)
    if not file:
        return jsonify({"error": "File not found"}), 404
    
    player.set_media(file)
    player.play()
    
    return jsonify({'error': None, 'file': file}), 200

@app.route('/remove/<hash>', methods=['DELETE'])
def remove(hash):
    success = qb.delete(hash)
    if success:
        return jsonify({'error': None}), 200
    return jsonify({'error': 'Failed to remove torrent'}), 500

@app.route("/pause/<hash>", methods=["POST"])
def pause(hash):
    if not hash:
        return jsonify({"error": "No hash"}), 400
    qb.pause(hash)
    return jsonify({"status": "paused"})

@app.route("/resume/<hash>", methods=["POST"])
def resume(hash):
    if not hash:
        return jsonify({"error": "No hash"}), 400
    qb.resume(hash)
    return jsonify({"status": "resumed"})

@app.route('/command/<cmd>', methods=['POST'])
def command(cmd):
    if cmd == "plp":
        player.pause()
    if cmd == "stp":
        print("STOPPING")
        player.stop_and_close()
    if cmd == "rrw":
        player.rewind(60)
    if cmd == "ffw":
        player.fast_forward(60)
    if cmd == "ccy":
        player.enable_subtitles()
    if cmd == "ccn":
        player.disable_subtitles()
        
        
    return jsonify({"status": "success"})

def setup():
    qb.set_torrent_download_location(cf.get("download_folder"), create=cf.get("create_folder", True))

    if not qb.check_connection():
        raise Exception("Failed to connect to QBittorrent. Please check your settings and ensure QBittorrent is running.")

if __name__ == "__main__":
    setup()
    subprocess.Popen(["python3", "overlay.py", f"http://{get_local_ip()}"])
    app.run(debug=False, host=cf.get("host"), port=cf.get("port"))
