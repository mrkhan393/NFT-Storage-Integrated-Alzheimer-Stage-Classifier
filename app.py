from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from web3 import Web3
import os
import json
from dotenv import load_dotenv
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from PIL import Image
import imagehash

load_dotenv()

app = Flask(__name__)

# Blockchain setup
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider("http://localhost:8545"))
# w3 = Web3(HTTPProvider("http://host.docker.internal:8545"))


# Confirm connection
if not w3.is_connected():
    raise Exception("Web3 not connected to local blockchain")

private_key = os.getenv("PRIVATE_KEY")
account_address = os.getenv("ACCOUNT_ADDRESS")
contract_address = os.getenv("CONTRACT_ADDRESS")

# Load contract ABI
def load_contract_abi(path='artifacts/contracts/NFTStorage.sol/NFTStorage.json'):
    with open(path) as f:
        contract_json = json.load(f)
        return contract_json["abi"]

abi = load_contract_abi()
contract = w3.eth.contract(address=contract_address, abi=abi)

# Load trained Keras model (.keras format)
model = tf.keras.models.load_model('model.keras')

# Class label mapping
CLASS_NAMES = {
    0: 'MildDemented',
    1: 'ModerateDemented',
    2: 'NonDemented',
    3: 'VeryMildDemented'
}

def is_mri_like_uploaded_image(upload_path, reference_folder="reference_mri", threshold=10):
    try:
        uploaded_hash = imagehash.average_hash(Image.open(upload_path).convert('L'))

        for ref_file in os.listdir(reference_folder):
            if ref_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                ref_path = os.path.join(reference_folder, ref_file)
                ref_hash = imagehash.average_hash(Image.open(ref_path).convert('L'))
                diff = abs(uploaded_hash - ref_hash)
                if diff < threshold:
                    print(f"Matched with {ref_file} (difference: {diff})")
                    return True
        return False
    except Exception as e:
        print(f"Error during MRI matching: {e}")
        return False

# Image classification function
def classify_image(image_path):
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image = image.resize((128, 128))
    image = img_to_array(image) / 255.0
    
     # Validate MRI likeness
    if not is_mri_like_uploaded_image(image_path):
        return None, None, "Uploaded image doesn't appear to be an MRI scan."

    image = np.expand_dims(image, axis=-1)  # Add channel dim: (128, 128, 1)
    image = np.expand_dims(image, axis=0)   # Add batch dim: (1, 128, 128, 1)
    prediction = model.predict(image)
    predicted_class = int(np.argmax(prediction[0]))
    return predicted_class, prediction[0]

# Store metadata on blockchain
def store_nft(metadata):
    try:
        # Get nonce for the account
        nonce = w3.eth.get_transaction_count(account_address)  # Correct way to get nonce
        print(f"Nonce: {nonce}")

        # Build the transaction
        tx = contract.functions.createNFT(metadata).build_transaction({
            'chainId':  w3.eth.chain_id,  # Hardhat local chain ID
            'gas': 2000000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': nonce,
        })
        print(f"Transaction: {tx}")

        # Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction Hash: {tx_hash.hex()}")

        return tx_hash.hex()

    except Exception as e:
        print(f"Error during NFT transaction: {str(e)}")
        return str(e)


# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the uploaded image
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Log file path to verify image is saved
        print(f"File saved at: {file_path}")

        # Classify the image
        
        predicted_class, probabilities = classify_image(file_path)

        # Log predicted class and probabilities
        print(f"Predicted Class: {predicted_class}, Probabilities: {probabilities}")

        # Ensure the predicted class is in the CLASS_NAMES dictionary
        predicted_label = CLASS_NAMES.get(predicted_class, "Unknown Class")
        print(f"Predicted Label: {predicted_label}")

        # Create metadata for the NFT
        metadata = f"Predicted Stage: {predicted_label} | Probabilities: {probabilities.tolist()}"
        tx_hash = store_nft(metadata)

        # If the hash is bytes (i.e., transaction succeeded), convert to hex
        if hasattr(tx_hash, "hex"):
            tx_hash = tx_hash.hex()

        return jsonify({
            'predicted_class': predicted_label,
            'probabilities': probabilities.tolist(),
            'transaction_hash': tx_hash
        })

    except Exception as e:
        # Log error details
        print(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Ensure uploads folder exists
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
