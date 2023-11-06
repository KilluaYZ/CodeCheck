import request from '@/utils/request'
export function login(email: string, password: string){
    const data = {
        email,
        password
    }
    return request({
        url: 'auth/login',
        headers: {
            isToken: false
        },
        method: 'post',
        data: data
    })
}

export function register(userName: string, email: string, password: string, checkCode: string, sessionKey: string){
    let data = {
        userName,
        email,
        password,
        checkCode,
        sessionKey
    }
    return request({
        url: 'auth/register',
        headers: {
            isToken: false
        },
        method: 'post',
        data: data
    })
}

export function updatePwd(email: string, password: string, checkCode: string, sessionKey: string){
    let data = {
        email,
        password,
        checkCode,
        sessionKey
    }
    return request({
        url: 'auth/updatePwd',
        headers: {
            isToken: false
        },
        method: 'post',
        data: data
    })
}

export function getRegisterSessionKeyCheckCode(userName: string, email: string){
    let data = {
        userName, email,
        "type":"register"
    }
    return request({
        url: 'auth/getSessionKeyCheckCode',
        headers: {
            isToken: false
        },
        method: 'post',
        data: data
    })
}

export function getChangePwdSessionKeyCheckCode(email: string){
    let data = {
        email,
        "type":"changePasswd"
    }
    return request({
        url: 'auth/getSessionKeyCheckCode',
        headers: {
            isToken: false
        },
        method: 'post',
        data: data
    })
}

export function checkIfEmailIsRegisted(email: string){
    let data = {
        email
    }
    return request({
        url: 'auth/register/check',
        headers:{
            isToken: false
        },
        method: 'post',
        data: data
    })
}

export function userProfile(){
    return request({
        url: 'auth/profile',
        method: 'get'
    })
}

