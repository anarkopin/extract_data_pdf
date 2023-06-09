import axios from "axios";

const API_URL = "https://extract-data-pdf.onrender.com/operations/";



const instance = axios.create({
  baseURL: API_URL,
});

// Interceptor de solicitud para incluir la cookie en las solicitudes
instance.interceptors.request.use(
    (config) => {
      // Excluye la solicitud de la cookie si la URL es la de inicio de sesión
      if (config.url !== "login/" && config.url !== "/login/") {
        const token = localStorage.getItem("token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

const PDFService = {
    getData: async () => {
        try {
            const response = await instance.get("get_data/");
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },
    extract_data: async (pdf_file) => {
        try {
            const formData = new FormData();
            formData.append('pdf_file', pdf_file);
            const response = await instance.post("extract_data/", formData);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
        
    
    }
}

export default PDFService;