import "../styles/UploadPage.css";
import React, { useState } from "react";
import axios from "axios";
const UploadPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);

      try {
        // Replace with your upload API endpoint
        const response = await axios.post(
          "http://44.228.29.165:8000/api/upload",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        alert("File uploaded successfully");
        // Handle the response as needed
      } catch (error) {
        console.error("Upload Error: ", error);
        alert("Upload failed");
      }
    } else {
      alert("Please select a file to upload");
    }
  };

  return (
    <div className="uploadBox">
      <div>
        <h1>Upload File</h1>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
      </div>
      <div className="emergencyTrackInfo">
        Emergency Track is a comprehensive crisis management solution
        meticulously engineered by SFSU software engineering students to deliver
        real-time, accurate information and foster a safer, more informed
        California.
      </div>
    </div>
  );
};

export default UploadPage;
