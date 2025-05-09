# 🧠 MRI Brain Scan Classifier + NFT Minting on Blockchain

This project is a smart mix of **AI** and **blockchain** it can predict the stage of Alzheimer’s from an **MRI image** using a trained deep learning model and stores the result as an **NFT** on a local Ethereum blockchain.

It’s like a brain scan doctor that gives you a prediction and saves it on the blockchain!

---

## What It Does

1. You upload a brain MRI image.
2. The system checks if it really looks like an MRI (not a random cat photo).
3. If valid, it predicts the Alzheimer's stage using a deep learning model.
4. The prediction and confidence scores are stored on the blockchain as NFT metadata.
5. You get back the result and the blockchain transaction hash.

---

## Technologies Used

### AI & Image Processing
- **Python**
- **TensorFlow / Keras** – to load the trained model.
- **Pillow** – to handle images (convert to grayscale, resize, etc).
- **NumPy** – to prepare image arrays.
- **imagehash** – to compare the uploaded image with real MRI examples.

### Backend & Web Server
- **Flask** – the backend server for prediction and blockchain interaction.
- **dotenv** – to load private keys and secrets safely.

### Blockchain
- **Solidity** – smart contract (`NFTStorage.sol`) to store prediction NFTs.
- **Web3.py** – to talk to the Ethereum blockchain from Python.
- **Hardhat** – to run a local Ethereum network and deploy the contract.

### Frontend
- **HTML + JavaScript** – minimal UI to upload images and view results.

---

## Folder Structure

├── app.py # Main Flask backend
├── model.keras # Trained MRI classification model
├── reference_mri/ # Real MRI examples for image validation
├── uploads/ # Temporarily stores uploaded images
├── artifacts/contracts/... # Smart contract ABI and build files
├── templates/index.html # Web frontend
├── static/scripts.js # JS to connect frontend to backend
├── .env # Private blockchain credentials (not shared)

---

## How to Run This Locally

> Make sure you have Python and Node.js installed.

### 1. Clone this repository
git clone https://github.com/your-username/mri-nft-classifier.git
cd mri-nft-classifier

### 2. Set up Python environment
pip install -r requirements.txt
Create a .env file and add:
PRIVATE_KEY=your_private_key
ACCOUNT_ADDRESS=your_account_address
CONTRACT_ADDRESS=your_deployed_contract_address

### 4. Start the blockchain (Hardhat)
In a separate terminal:
npx hardhat node

And deploy the smart contract:
npx hardhat run scripts/deploy.js --network localhost
Update .env with the contract address you get after deployment.

### 5. Run the Flask server
python app.py

### 6. Open the app
Visit http://localhost:5000 in your browser.
Testing
Try uploading:

A real MRI image → Should give prediction + NFT hash.
A random image → Should tell you it's not a MRI image.

Fun Fact
This project was built to show how AI and blockchain can work together, combining health predictions with the trust and transparency of decentralized storage.

Feel free to reach out if you have questions or ideas!
