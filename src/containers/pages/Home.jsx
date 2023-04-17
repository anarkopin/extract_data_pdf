import { connect } from "react-redux";
import Layout from "../../hocs/layouts/Layout";

function Home() {
    return (
        <Layout>
            <h1>Home</h1>
     
        </Layout>
    );
}

const mapStateToProps=state =>({

})

export default connect(mapStateToProps,{
    
})(Home)