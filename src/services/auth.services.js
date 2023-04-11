import axios from "axios";
import getCookie from "./utils";
import Cookies from 'universal-cookie';


const API_URL = "https://c58d-190-234-75-104.ngrok-free.app/api/user/";
const cookies = new Cookies();


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
  

const AuthService = {
    login: async (email, password) => {
      try {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);
  
        const response = await instance.post("login/", formData);
      
        return response;
      } catch (error) {
        throw error.response.data;
      }
    },
  
    register: async (first_name, last_name, email, password, password_confirmation) => {
      try {
        const formData = new FormData();
        formData.append('first_name', first_name);
        formData.append('last_name', last_name);
        formData.append('email', email);
        formData.append('password', password);
        formData.append('password_confirmation', password_confirmation);
        const response = await instance.post("register/", formData);
        return response.data;
      } catch (error) {
        throw error.response.data;
      }
    },
  
    logout: async () => {
      try {
        const response = await instance.post("logout/");
        return response.data;
      } catch (error) {
        throw error.response.data;
      }
    },
  };
  
  export default AuthService;

