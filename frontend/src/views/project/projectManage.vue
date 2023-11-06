<template>

    <el-row>
        <el-card shadow='hover' style='width: 100%'>
            <template #header>
                <h1>项目概览</h1>
            </template>
            <el-row style='width: 100%' justify='start'>
                <el-col span=20>
                    <el-button type='success' @click='onClickAddProjectBtn'>新建项目</el-button>
<!--                    <el-button type='danger'>删除项目</el-button>-->
                </el-col>
            </el-row>
        </el-card>
    </el-row>


<!--    <el-row>-->
<!--        <h1 style='font-size: 50px'>项目管理</h1>-->
<!--    </el-row>-->
    <el-row justify='space-evenly'>
        <ProjectCard
            v-for='item in data'
            :id='Number(item.projectId)'
            :name='item.projectName'
            :stage='item.projectStatus'
            :is-public='item.isPublic'
            :create-time='item.createTime'
            :delete-func='onClickDelBtn'
            :problem-num='item.problemNum'
        />
    </el-row>

    <el-dialog
        v-model='dialogVisible'
        title='新建项目'
        width='40%'>

        <el-row style='width: 100%'>
            <el-form
                :model='form'
                label-width='120px'
            >
                <el-form-item label='项目名' prop='projectName'>
                    <el-input v-model='form.projectName' placeholder='请输入项目名' clearable />
                </el-form-item>
                <el-form-item label='是否公开' prop='isPublic'>
                    <el-switch
                        v-model="form.isPublic"
                        active-text="公开"
                        inactive-text="私有"
                    />
                </el-form-item>

                <el-form-item label='json分析结果'>
                    <el-upload
                        ref="uploadJson"
                        action=""
                        :limit="1"
                        :on-exceed="handleJsonExceed"
                        :auto-upload="false"
                        name='file'
                        :on-change='handleJsonUploadChanged'
                    >
                        <template #trigger>
                            <el-button type="primary">选择文件</el-button>
                        </template>
<!--                        <el-button class="ml-3" type="success" @click="submitUpload">-->
<!--                            upload to server-->
<!--                        </el-button>-->
                        <template #tip>
                            <div class="el-upload__tip text-red">
                                支持后缀名为json的文件
                            </div>
                        </template>
                    </el-upload>
                </el-form-item>

                <el-form-item label='源码压缩包'>
                    <el-upload
                        ref="uploadSrc"
                        action=""
                        :limit="1"
                        :on-exceed="handleSrcExceed"
                        :auto-upload="false"
                        name='file'
                        :on-change='handleSrcUploadChanged'
                    >
                        <template #trigger>
                            <el-button type="primary">选择文件</el-button>
                        </template>
                        <template #tip>
                            <div class="el-upload__tip text-red">
                                支持后缀名为zip, tar, gz, rar, 7z的压缩包
                            </div>
                        </template>
                    </el-upload>
                </el-form-item>

            </el-form>

        </el-row>

        <template #footer>
          <span class="dialog-footer">
            <el-button @click="onClickCancelBtn">取消</el-button>
            <el-button type="primary" @click="onClickCommitBtn">确认</el-button>
          </span>
        </template>
    </el-dialog>
</template>

<script setup lang='ts'>
import { onMounted, ref } from 'vue'
import ProjectCard  from '@/components/ProjectCard.vue'
import { ElLoading, ElMessage, genFileId, UploadFile, UploadFiles } from 'element-plus'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { types } from 'sass'
import List = types.List
import { addProject, delProject, getProjectList } from '@/api/project'
import { uploadFile } from '@/api/file'

const dialogVisible = ref(false);

const onClickAddProjectBtn = () => {
    dialogVisible.value = true;
}

const form = ref({
    projectName: "",
    isPublic: false
})

const resetForm = () => {
    form.value.projectName = "";
    form.value.isPublic = false;
}

// const data = ref([
//     {
//         projectId: "1",
//         projectName: '项目1',
//         projectStatus: "success",
//         isPublic: true
//     },
// ])

const data = ref([])
const uploadJson = ref<UploadInstance>()
const uploadSrc = ref<UploadInstance>()
const currentJsonFile = ref<UploadFile>()
const currentSrcFile = ref<UploadFile>()

const handleJsonExceed: UploadProps['onExceed'] = (files) => {
    uploadJson.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    uploadJson.value!.handleStart(file)
}

const handleSrcExceed: UploadProps['onExceed'] = (files) => {
    uploadSrc.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    uploadSrc.value!.handleStart(file)
}

const clearFiles = () => {
    uploadJson.value!.clearFiles();
    uploadSrc.value!.clearFiles();
}
const onClickCancelBtn = () => {
    resetForm();
    clearFiles();
}

const onClickCommitBtn = () => {
    // 先检验一下
    if(form.value.projectName === undefined || form.value.projectName.length === 0){
        ElMessage({
            type: 'error',
            message: '请填写项目名称'
        })
        return ;
    }

    if(form.value.isPublic === undefined){
        ElMessage({
            type: 'error',
            message: '请选择是否公开'
        })
        return ;
    }

    const uploadFileLoading = ElLoading.service({
        lock: true,
        text: '正在上传文件，请稍候',
        background: 'rgba(0, 0, 0, 0.7)'
    });
    addProject(form.value.projectName, form.value.isPublic).then((res) => {
        let projectId = res.data.projectId;
        readinFile(currentJsonFile.value).then((jsonResult) => {
            let jsonFileName = jsonResult.name;
            let jsonFileContent = jsonResult.content;
            uploadFile(projectId, jsonFileName, jsonFileContent).then((res) => {
                readinFile(currentSrcFile.value).then((srcResult) => {
                    let srcFileName = srcResult.name;
                    let srcFileContent = srcResult.content;
                    setTimeout(()=> {
                        uploadFile(projectId, srcFileName, srcFileContent).then((res) => {
                            uploadFileLoading.close()
                            getList();
                            dialogVisible.value = false;
                        }).catch(() => {uploadFileLoading.close()})
                    }, 1000)
                }).catch(() => {uploadFileLoading.close()})
            }).catch(() => {uploadFileLoading.close()})
        }).catch(() => {uploadFileLoading.close()})
    }).catch(() => {uploadFileLoading.close()})

}

const checkIfFileTypeInList = (file: UploadFile, fileList: string[]): boolean => {
    let fileName = file.name;
    let fileType = fileName.slice(fileName.lastIndexOf(".")+1);
    fileType = fileType.toLowerCase();
    return fileList.some((item) => {
        return item === fileType;
    })
}

var globalProjectId = '';

const handleUploadFile = (param: any) => {
    const uploadFileLoading = ElLoading.service({
        lock: true,
        text: '正在上传文件，请稍候',
        background: 'rgba(0, 0, 0, 0.7)'
    });
    uploadFile(globalProjectId, param.file).then((res) => {
        console.log(res)
        uploadFileLoading.close();
    }).catch(() => {
        uploadFileLoading.close();
    })
}

const handleJsonUploadChanged = (currentUploadFile: UploadFile, currentUploadFiles: UploadFiles) => {
    console.log("当前file")
    console.log(currentUploadFile)
    if(!checkIfFileTypeInList(currentUploadFile, ['json'])){
        ElMessage({
            type: 'error',
            message: '请选择格式正确的JSON文件，注意：文件一定要以.json为后缀'
        })
        currentJsonFile.value = undefined;
        return ;
    }else{
        currentJsonFile.value = currentUploadFile;
    }
}

const handleSrcUploadChanged = (currentUploadFile: UploadFile, currentUploadFiles: UploadFiles) => {
    console.log("当前file")
    console.log(currentUploadFile)
    if(!checkIfFileTypeInList(currentUploadFile, ['zip', '7z', 'tar', 'rar', 'gz'])){
        ElMessage({
            type: 'error',
            message: '请选择格式正确的压缩文件，注意：文件一定要以.7z, .zip, .rar, .tar, .gz为后缀'
        })
        currentSrcFile.value = undefined;
        return ;
    }else{
        currentSrcFile.value = currentUploadFile;
    }
}

const readinFile = (binaryFile: UploadFile) => {
    return new Promise((resolve, reject) => {
        let reader = new FileReader();
        reader.readAsDataURL(binaryFile.raw);
        reader.onload = (e) => {
            let content = e.target.result;
            content = content.slice(content.indexOf(','))
            let result = {
                content: content,
                name: binaryFile.name
            }
            resolve(result);
        }
        reader.onerror = reject;
    })
}

const getList = () => {
    getProjectList().then(res => {
        data.value = res.data;
    }).catch(() => {

    })
}

const onClickDelBtn = (projectId: string) => {
    const delProjectLoading = ElLoading.service({
        lock: true,
        text: '正在删除',
        background: 'rgba(0, 0, 0, 0.7)'
    });
    delProject(projectId).then(res => {
        getList();
        delProjectLoading.close()
    }).catch(() => {
        delProjectLoading.close()
    })
}

onMounted(getList)

</script>


<style scoped>
.text-red{
    color: red;
}
</style>