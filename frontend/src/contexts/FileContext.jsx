import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const FileContext = createContext();

export function FileProvider({ children }) {
  const [files, setFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [collection] = useState("default");

  const fetchFiles = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/listCollectionFiles?collectionName=${collection}`);
      setFiles(res.data.files || []);
    } catch (err) {
      console.error("Failed to fetch files", err);
    }
  };

  useEffect(() => { fetchFiles(); }, [collection]);

  return (
    <FileContext.Provider value={{ 
      files, setFiles, 
      selectedFiles, setSelectedFiles, 
      collection, fetchFiles 
    }}>
      {children}
    </FileContext.Provider>
  );
}

export const useFiles = () => useContext(FileContext);