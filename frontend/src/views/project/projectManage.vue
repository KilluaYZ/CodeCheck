<template>

    <el-row>
        <el-card shadow='hover' style='width: 100%'>
            <template #header>
                <h1>项目概览</h1>
            </template>
            <el-row style='width: 100%' justify='start'>
                <el-col span=20>
                    <el-button type='success' @click='onClickAddProjectBtn'>新建项目</el-button>
                </el-col>
            </el-row>
        </el-card>
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
                <el-form-item label="项目类型" prop="projectType">
                    <el-radio-group v-model="form.projectType">
                        <el-radio label="json" size="large">Json</el-radio>
                        <el-radio label="other" size="large">其他</el-radio>
                    </el-radio-group>
                    <el-text type="danger">json类型项目需要上传json格式解析文件，其他类型项目需要上传对应的解析文件</el-text>
                </el-form-item>
                <el-form-item label='分析结果文件'>
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
<!--                        <template #tip>-->
<!--                            <div class="el-upload__tip text-red">-->
<!--                                支持后缀名为json的文件-->
<!--                            </div>-->
<!--                        </template>-->
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
import { ElLoading, ElMessage} from 'element-plus'
import { types } from 'sass'
import List = types.List
import { addProject, delProject, getProjectList } from '@/api/project'

const dialogVisible = ref(false);

const onClickAddProjectBtn = () => {
    dialogVisible.value = true;
}

const form = ref({
    projectName: "",
    isPublic: false,
    projectType: "other"
})

const resetForm = () => {
    form.value.projectName = "";
    form.value.isPublic = false;
    form.value.projectType = "other"
}

// const data = ref([
//     {
//         projectId: "1",
//         projectName: '项目1',
//         projectStatus: "success",
//         isPublic: true
//     },
// ])
type ProjectType = {
    projectId: number,
    projectName: string,
    projectStatus: string,
    isPublic: boolean,
    createTime: string,
    problemNum: number,
    projectType: string
}
const data = ref<ProjectType[]>([])

const handleJsonExceed: UploadProps['onExceed'] = (files) => {
    uploadJson.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    uploadJson.value!.handleStart(file)
}

const onClickCancelBtn = () => {
    resetForm();
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