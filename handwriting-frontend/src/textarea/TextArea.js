import React  from 'react';

import "./TextArea.css";

function TextArea({onChange, value}) {
    return (
        <div className="TextArea">
            <textarea 
                placeholder="Start typing here..."
                className='min-w-' 
                value={value} 
                onChange={onChange}
            />
        </div>
    );
}

export default TextArea;