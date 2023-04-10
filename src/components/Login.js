import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AuthService from "../services/auth.services";
import getCookie from "../services/utils";
import ErrorAlert from "./alert/Error.alert";
import SuccessAlert from "./alert/Succes.alert";
import Cookies from "universal-cookie";

const cookies = new Cookies();


function Login() {
    const [error, setError] = useState(false);
    const [success, setSuccess] = useState(false);
    const [message, setMessage] = useState("");


    const handleSubmit = (e) => {
        e.preventDefault();
        //acceder a los valores del formulario
        const email = e.target[0].value;
        const password = e.target[1].value;

        console.log(email, password)

        if (email === "" || password === "") {
            setMessage("All fields are required");
            setError(true);
            return
        }


        AuthService.login(email, password)
        .then((response) => {
            localStorage.setItem('token', response.data.token);
            setMessage("Loggin successfully")
            setSuccess(true);
            window.location.href = "/taxes";


        })
        .catch((error) => {
            setMessage("An error has occurred, try again.");
            setError(true);
            console.error(error);
        });
        

    }

    useEffect(() => {
        console.log("error", error)
    }, [error])

    const handleChangeError = () => {
        setError(false);
    }

    const handleChangeSuccess = () => {
        setSuccess(false);
    }


    return (
        <>
            <section class="min-h-screen flex flex-col">
            <div class="flex flex-1 items-center justify-center">
            <div className="w-96 flex justify-center absolute">
                    <SuccessAlert message={message} active={success} handleChangeSuccess={handleChangeSuccess} />
                    </div>
                    <div className="w-96 flex justify-center absolute">
                    <ErrorAlert message={message} active={error} handleChangeError={handleChangeError} />

                    </div>
                <div class="rounded-lg sm:border-2 px-4 lg:px-24 py-16 lg:max-w-xl sm:max-w-md w-full text-center">
                    
                    <form class="text-center" onSubmit={handleSubmit}>
                    
                        <h1 class="font-bold tracking-wider text-3xl mb-8 w-full text-gray-600">
                            Sign in
                        </h1>
                        <div class="py-2 text-left">
                            <input type="email" class="bg-gray-200 border-2 border-gray-100 focus:outline-none bg-gray-100 block w-full py-2 px-4 rounded-lg focus:border-gray-700 " placeholder="Email" />
                        </div>
                        <div class="py-2 text-left">
                            <input type="password" class="bg-gray-200 border-2 border-gray-100 focus:outline-none bg-gray-100 block w-full py-2 px-4 rounded-lg focus:border-gray-700 " placeholder="Password" />
                        </div>
                        <div class="py-2">
                            <button type="submit" class="border-2 shrink-0 rounded-md border border-blue-600 bg-blue-600 px-12 py-3 text-sm font-medium text-white transition hover:bg-transparent hover:text-blue-600 focus:outline-none focus:ring active:text-blue-500">
                                Sign In
                            </button>
                        </div>
                    </form>
                    <div class="text-center mt-12">
                        <span>
                            Don't have an account?
                        </span>
                        <Link to="/register" class="font-light text-md text-indigo-600 underline font-semibold hover:text-indigo-800">Create One</Link>
                    </div>
                </div>
            </div>
        </section>



        </>
    );
}

export default Login;