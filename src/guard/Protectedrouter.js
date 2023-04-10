import { Navigate } from "react-router-dom";
import Cookies from "universal-cookie";

const cookies = new Cookies();

export const ProtectedRoute = ({ children}) => {
    const login = localStorage.getItem("token");

    return (
        login ? children : <Navigate to="/login" />
    )
}