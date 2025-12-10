// create a header component using React and TypeScript
// the header should display the title of the application
// it should also have a navigation bar with links to Home, Devices, and Login

import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header>
      <nav style={{ display: 'flex', gap: '5rem', paddingLeft: '5rem', padding: '1rem', backgroundColor: '#475c85ff' }}>
        
            <Link style={{ color: 'white' }} to="/">Home</Link>
         
            {/* <Link style={{ color: 'white' }} to="/devices">Devices</Link> */}
          
            <Link style={{ color: 'white' }} to="/login">Login</Link>
          
      </nav>
    </header>
  );
};

export default Header;