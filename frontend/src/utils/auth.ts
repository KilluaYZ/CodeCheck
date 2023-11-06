import { Storage } from '@/utils/cache'

function logout(){
    Storage.removeItem('userInfo')
    // Storage.removeItem('token')
    removeUserInfo();
    removeToken();
    location.reload();
}

function setUserInfo(userInfo: any){
    Storage.setItem('userInfo', userInfo);
}

function getUserInfo(): any{
    let userInfo: any = Storage.getItem('userInfo');
    return userInfo;
}

function removeUserInfo(){
    Storage.removeItem('userInfo');
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
    logout, getToken, setToken, removeToken, setUserInfo, getUserInfo, removeUserInfo
}