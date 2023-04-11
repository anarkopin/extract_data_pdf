import { useState } from 'react';
import PDFService from '../services/pdf.services';
import ErrorAlert from './alert/Error.alert';
import SuccessAlert from '../components/alert/Succes.alert';

function UploadFile({ handleChangeProduct }) {
    const [file, setFile] = useState(null);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [message, setMessage] = useState('');

    
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        //validar si el campo tiene un archivo pdf

        if (file !== null) {
            if (file.type === 'application/pdf') {
                PDFService.extract_data(file).then(
                    (response) => {
                        setError(false);
                        setMessage("Success in processing pdf");
                        setSuccess(true);
                        //limpiar formulario
                        setFile(null);
                        event.target.reset();
                        handleChangeProduct(response);
                        
                    },
                    (error) => {
                        setMessage("Error processing file");
                        setFile(null);
                        event.target.reset();
                        setError(true);
                    }
                );
            } else {
                setMessage('The file must be a PDF');
                event.target.reset();
                setFile(null);
                setError(true);
            }
        } else {
            setMessage('You have not uploaded a file');
            event.target.reset();
            setError(true);
        }
        

    }

    const handleChangeError = () => {
        setError(false);
        setMessage('');
    }

    const handleChangeSuccess = () => {
        setSuccess(false);
        setMessage('');
    }

    return (
        <form onSubmit={handleSubmit}>
        <div className='absolute mt-32'>
        <ErrorAlert active={error} message={message} handleChangeError={handleChangeError } />
        <SuccessAlert active={success} message={message} handleChangeSuccess={handleChangeSuccess} />
        </div>
        <label htmlFor="large-file-input" className="sr-only">Choose file</label>
        <input type="file" name="large-file-input" id="large-file-input" className="block w-full border border-gray-200 shadow-sm rounded-md text-sm focus:z-10 focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400
            file:bg-transparent file:border-0
            file:bg-gray-100 file:mr-4
            file:py-3 file:px-4 file:sm:py-5
            dark:file:bg-gray-700 dark:file:text-gray-400"
            onChange={handleFileChange}
        />
        <div className='flex justify-center'>
        <button type='submit' className="mt-2 bg-slate-900 text-white font-bold py-2 px-4 border border-blue-700 rounded">
        Procesar
        </button>       
        
        </div>
       
    </form>
    );
}

export default UploadFile;