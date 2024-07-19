import React, { useState, useEffect } from 'react';

import Button from "../button/Button";

function Output(props) {

    const baseUrl = props.baseUrl;
    const numPages = props.numPages;
    const update = props.update;
    const [pageIndex, setPageIndex] = useState(-1); 

    useEffect(() => {

        // console.log("Update prop has changed:", update);
        
        if (numPages !== 0 && pageIndex === -1)
            setPageIndex(0);
        else if (numPages < pageIndex + 1)
            setPageIndex(numPages-1);
        

    }, [update]); 



    const nextPage = () => {
        setPageIndex((prevIndex) => (prevIndex + 1) % numPages);
    };

    const previousPage = () => {
        setPageIndex((prevIndex) => (prevIndex - 1 + numPages) % numPages);
    };

  return (
    <div className="w-8/12 md:w-5/12 mt-7">
        <div className="app-section-label uppercase text-2xl">
            Handwriting
        </div>
        
        <div className="w-full aspect-[100/141] mb-2 border-black border-2">
            {numPages!==0 &&
            <img className="w-full h-full" 
                 src={`${baseUrl}${pageIndex}&update=${update}`}
                 alt="Handwritten Page"/>}
        </div>
        
        {numPages !== 0 &&
            <div className="mt-4 flex justify-between items-center">
                <div>
                    <button type="button" id="back-btn"  className="w-10 h-7 mr-4 rounded" onClick={previousPage}>
                        <i className="fas fa-arrow-left"/>
                    </button>

                    <strong>{pageIndex + 1}</strong> / {numPages}

                    <button type="button" id="forwd-btn" className="w-10 h-7 mx-4 rounded" onClick={nextPage}>
                        <i className="fas fa-arrow-right"/>
                    </button>
                </div>

                <Button text="Download" onClick={props.handleDownloadPDF}/>
            </div>
        }
        
    </div>
  );
}

export default Output;