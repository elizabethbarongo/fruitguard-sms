
from flask import Flask, request
app = Flask(__name__)

@app.post("/dr")
def delivery_report():
    print("=== Delivery Report Callback ===")
    print("Headers:", dict(request.headers))   
    payload = request.get_json(silent=True)   
    print("JSON:", payload)                
    return ("", 204)  
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)






