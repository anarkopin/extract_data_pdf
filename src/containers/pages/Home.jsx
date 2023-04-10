import { useEffect, useState } from "react";
import ListData from "../../components/ListData";
import Footer from "../../components/navigation/Footer";
import Navbar from "../../components/navigation/Navbar";
import UploadFile from "../../components/UploadFile";
import Layout from "../../hocs/layouts/Layout";
import PDFService from "../../services/pdf.services";

function Home() {

    const [data, setData] = useState([]);

    useEffect(() => {
        getInitialData();
    },[])

    const getInitialData = async () => {
        try {
            PDFService.getData().then((response) => {
                setData(response);
            } ).catch((error) => {
                console.log(error);
            }
            )
        } catch (error) {
            console.log(error);
        }
    }


    const handleChangeProduct = () => {
        getInitialData();
    }

    
    return (
        <Layout>
            <Navbar />
            <div className="pt-96 w-full flex justify-center">
                <UploadFile handleChangeProduct={handleChangeProduct}/>
            </div>
            <div className="mt-10">
                <ListData data={data} />

            </div>
     
        </Layout>
    );
}

export default  Home;