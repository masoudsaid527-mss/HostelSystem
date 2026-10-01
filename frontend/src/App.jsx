import React, {Component} from 'react';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/Register';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';

class App extends Component {
  render(){
    return(
      <div>
          <Router>
              <Routes>
                  <Route path="/" element={<LoginPage />} />
                  <Route path="/Register" element={<RegisterPage />} />
              </Routes>
          </Router>
      </div>
    )
  }
}
export default App;