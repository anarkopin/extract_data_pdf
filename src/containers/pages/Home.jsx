import { useState } from "react";
import ListData from "../../components/ListData";
import Navbar from "../../components/navigation/Navbar";
import UploadFile from "../../components/UploadFile";
import Layout from "../../hocs/layouts/Layout";

function Home() {

    const [data, setData] = useState([]);

    const handleChangeProduct = (objectData) => {
        setData(objectData);
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