import React  from 'react';

import "./Button.css";


function Button(props) {
    // console.log(props);
    const text = props.text ? props.text : "Button";
    const icon = props.icon ? props.icon : null;
    return <button className="button" onClick={props.onClick}>
            <div className="button-text">
                {text}
            </div>
            
            {icon && 
                <div className="button-icon">

                </div>    
            }
     

            
        </button>;
}

export default Button;