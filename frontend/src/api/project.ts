import request from '@/utils/request'
export function addProject(projectName: string, containerId: string){
    const data = {
        name: projectName,
        container_id: containerId
    }
    return request({
        url: 'project/add',
        method: 'post',
        data: data
    })
}

export function getProjectDetail(projectId: string){
    const data = {
        project_id: projectId
    }
    return request({
        url: 'project/list',
        method: 'post',
        data: data
    })
}

export function getProjectList(){
    return request({
        url: 'project/list',
        method: 'post'
    })
}

export function delProject(projectId: string){
    let data = {
        project_id: projectId
    }

    return request({
        url: 'project/del',
        method: 'post',
        data: data
    })
}

