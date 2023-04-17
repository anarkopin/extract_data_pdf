import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom'
import Error404 from '../../containers/errors/Error404';
import Home from '../../containers/pages/Home';

import { AnimatePresence } from 'framer-motion'


function AnimatedRoutes(){

    const location = useLocation()

    return(
        <AnimatePresence>
            <Routes location={location} key={location.pathname}>
                    {/* Error Display */}
                    <Route path="*" element={<Error404 />} />
                    {/* Home Display */}
                    <Route path="/" element={<Home />} />
                </Routes>
        </AnimatePresence>
    )
}
export default AnimatedRoutes