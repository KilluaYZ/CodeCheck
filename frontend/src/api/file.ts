import request from '@/utils/request'
import axios from 'axios'
import { getToken } from '@/utils/auth'

export function uploadFile(projectId: string, fileName: string, fileContent: string){
    const data = {
        projectId,
        fileName,
        fileContent
    }
    return request({
        url: 'file/upload',
        method: 'post',
        data: data
    })

    // let formData = new FormData();
    // formData.append('fileContent', fileContent);
    // formData.append('projectId', projectId);
    // formData.append('fileName', fileName);
    // return axios.post('url/upload', formData, {
    //     headers: {
    //         "Content-Type": "multipart/form-data",
    //         "Authorization": getToken()
    //     }
    // })

    // return request({
    //     url: 'file/upload',
    //     method: 'post',
    //     data: formData,
    //     headers:{
    //         'Content-Type': 'multipart/form-data'
    //     }
    // })
}

export function getFile(projectId: number, filePath: string, fileName: string){
    let data = {
        projectId,
        filePath,
        fileName
    }

    return request({
        url: 'file/getFile',
        method: 'post',
        data: data
    })
}