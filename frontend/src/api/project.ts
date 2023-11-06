import request from '@/utils/request'
export function addProject(projectName: string, isPublic: boolean){
    const data = {
        projectName,
        isPublic
    }
    return request({
        url: 'project/add',
        method: 'post',
        data: data
    })
}

export function getProjectList(){
    return request({
        url: 'project/get/list',
        method: 'get'
    })
}

export function delProject(projectId: string){
    let data = {
        projectId
    }

    return request({
        url: 'project/del',
        method: 'post',
        data: data
    })
}

export function getProjectProblems(projectId: string){
    let data = {
        projectId
    }

    return request({
        url: 'project/problem/get',
        method: 'post',
        data: data
    })
}

export function submitProject(projectId: number){
    let data = {
        projectId
    }

    return request({
        url: 'project/submit',
        method: 'post',
        data: data
    })
}