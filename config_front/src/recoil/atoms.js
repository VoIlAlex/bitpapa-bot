import {atom} from "recoil";


export const userAtom = atom({
    key: "user",
    default: null
})


export const errorAtom = atom({
    key: "error",
    default: null
})
