import { Storage } from '@/utils/cache'

function logout(){
    Storage.removeItem('userInfo')
    Storage.removeItem('token')
    location.reload()
}

function getToken(): string{
    let token: string = Storage.getItem("token");
    return token;
}

function setToken(token: string){
    Storage.setItem('token', token);
}

function removeToken(){
    Storage.removeItem('token');
}

export {
    logout, getToken, setToken, removeToken
}