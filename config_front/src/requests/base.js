

export const compileRequest = (requestObj, outputHandler, errorHandler) => {
    requestObj.then(res => {
        if (res.ok) {
            return res.json()
        } else {
            throw Error("Error handling request.")
        }
    }).then(
        data => outputHandler(data)
    ).catch(err => {
        if (errorHandler) {
            errorHandler(err);
        }
        console.log(err)
    })
}