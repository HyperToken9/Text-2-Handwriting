import React  from 'react';

import "./NavBar.css";

import NavLogo from "../assets/nav-logo.png";
// import Credits from "../assets/credits.png";
// import LinkedInLogo from "../assets/linkedIn-icon.png";
// import MailLogo from "../assets/mail-icon.png";
// import GitHubLogo from "../assets/github-icon.png";

function NavBar() {
    return (
        <nav className="nav-wrapper w-screen flex justify-center md:justify-start items-center">
            <img className="nav-logo" src= {NavLogo} alt='Text to Handwriting logo'/>
            
           

        </nav>
    );
}
export default NavBar;