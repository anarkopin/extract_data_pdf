import AuthService from "../services/auth.services";
import { ArrowLeftOnRectangleIcon } from "@heroicons/react/20/solid";

export const Logout = () => {

    const handleLogout = () => {
        AuthService.logout();
        window.location.href = "/";
    }

    
    return (
        <div>
            <button onClick={handleLogout}><ArrowLeftOnRectangleIcon /></button>
        </div>
    );


}
