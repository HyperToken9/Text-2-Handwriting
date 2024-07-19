import React, { useState } from 'react';
import axios from 'axios';

import "./App.css";

import NavBar from "./navbar/NavBar";
import TextArea from "./textarea/TextArea";
import Button from "./button/Button";
import Output from "./output/Output";



const App = () => {
    
    const [text, setText] = useState(""); // State to store text area value
    const [isAutoGen, setIsAutoGen] = useState(false);

    const baseUrl  = "/api/get-page?index=";

    // var pages = [];
    const [numPages, setNumPages] = useState(0);
    const [forceUpdate, setForceUpdate] = useState(0);

    const handleGeneratePage = async () => {
        try {
        // console.log("Text Submitted:", text);    
        const result = await axios.post('/api/generate-pages', {
            text: text
        });

            // console.log("Result:", result.data);
            // console.log("Number of Pages:", result.data.num_pages);
            setNumPages(result.data.num_pages);
            setForceUpdate(prev => prev + 1);
            
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleDownloadPDF = async () => {
        try {
            const response = await axios.get('/api/get-pdf', {
                responseType: 'blob'  // Ensure the response is treated as binary data
            });

            // Create a URL for the blob object
            const url = window.URL.createObjectURL(new Blob([response.data]));

            // Create a temporary link element to download the blob
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'testing.pdf');  // Specify the filename to download as

            // Append link to the body
            document.body.appendChild(link);

            // Force download
            link.click();

            // Clean up and remove the link
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);  // Free up memory by revoking the blob URL
        } catch (error) {
            console.error('Error downloading the PDF:', error);
        }
    };

    // Handler to update text from TextArea
    const handleTextChange = (event) => {
        setText(event.target.value);
        
        if (isAutoGen) 
            handleGeneratePage();
    };

    // Handler for Button click
    const handleButtonClick = async() => {
        // console.log("Text Submitted:", text);
        // Here you can also send the text to an API or another component
        await handleGeneratePage();
        

    };

    const handleAutoGenChange = (event) => {
        setIsAutoGen(event.target.checked);
    };

    return (
        <div className="App w-full mb-10">
            <NavBar />

            <div className="app-container">
                <div className="flex flex-col items-center md:items-start md:flex-row justify-around">
                    <div className="w-8/12 md:w-5/12 mt-7">
                        <div className="app-section-label uppercase text-2xl">
                            Text
                        </div>

                        <TextArea onChange={handleTextChange} value={text}/>

                        <div className="mt-4 w-full flex items-center gap-3">
                            <Button text="Generate" onClick={handleButtonClick} />
                            
                            <div className="flex items-center gap-1">
                                <label htmlFor="auto-gen">
                                    Auto Generate
                                </label>
                                <input 
                                    type="checkbox" 
                                    id="auto-gen"
                                    checked={isAutoGen}
                                    onChange={handleAutoGenChange}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Pass numPages and baseUrl as a prop to output */}
                    <Output numPages={numPages} 
                            baseUrl={baseUrl} 
                            update={forceUpdate}
                            handleDownloadPDF={handleDownloadPDF}
                            
                        />

                </div>
            </div>
        </div>
    );
}

export default App;
