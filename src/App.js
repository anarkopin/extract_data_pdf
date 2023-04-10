import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Error404 from "./containers/errors/Error404";
import Home from "./containers/pages/Home";
import Login from "./components/Login";
import Register from "./components/Register";
import store from "./store";
import { Provider } from "react-redux";
import { ProtectedRoute } from "./guard/Protectedrouter";

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          {/*Error display */}
          <Route path="*" element={<Error404 />} />

          <Route path="/" element={<Register />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/taxes" element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>} />
        </Routes>
    </Router>
    </Provider>
  );
}

export default App;
