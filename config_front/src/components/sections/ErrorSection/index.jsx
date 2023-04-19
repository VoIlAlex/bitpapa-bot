import React, {useEffect} from "react";
import "./index.scss";
import {useRecoilState} from "recoil";
import {errorAtom} from "../../../recoil/atoms";


export default () => {
    const [error, setError] = useRecoilState(errorAtom);
    useEffect(() => {
        console.log(error)
    }, [error])
    return error ? (
        <div className="error-section">
            <h1 className="error-section__header">Error occurred during initialization.</h1>
            <p className="error-section__text">{error}</p>
        </div>
    ) : null
}